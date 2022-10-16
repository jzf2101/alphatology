"""Evaluate probing accuracy of different concepts vs various baselines.
"""
import itertools
import random

import tqdm

import numpy as np
import pandas as pd

import flags
import utils

from sklearn.model_selection import GroupShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

from templates import concepts


def experiment_2(info):
    """Groupby owner to play (true)

    1. No connect.
    2. No intrude.
    3. owner_to_play
    4. owner_filtered mixed
    """
    return info[~info.connect & ~info.intrude & info.owner_to_play], {
        "connect": False,
        "intrude": False,
        "owner_to_play": True,
        "owner_filtered": "mixed",
        "experiment": "2-rand",
    }


def experiment_3(info):
    """Groupby owner to play (false)

    1. No connect.
    2. No intrude.
    3. No owner_to_play
    """
    return info[~info.connect & ~info.intrude & ~info.owner_to_play], {
        "connect": False,
        "intrude": False,
        "owner_to_play": False,
        "owner_filtered": "mixed",
        "experiment": "3-rand",
    }


def experiment_4(info):
    """Connect + Groupby owner to play (true)

    1. No connect.
    2. No intrude.
    3. owner_to_play
    """
    return info[info.connect & ~info.intrude & info.owner_to_play], {
        "connect": True,
        "intrude": False,
        "owner_to_play": True,
        "owner_filtered": "mixed",
        "experiment": "4-rand",
    }


def experiment_5(info):
    """Connect + Groupby owner to play (false)"""
    return info[info.connect & ~info.intrude & ~info.owner_to_play], {
        "connect": True,
        "intrude": False,
        "owner_to_play": False,
        "owner_filtered": "mixed",
        "experiment": "5-rand",
    }


def experiment_6(info):
    """[Intrude] Defensive Connect

    Rationale: Intrude vs not when opponent is connected.
    Though it may still be losing, determines if the player can entirely
    server the concept structure.
    """
    info = info[info.connect & ~info.owner_to_play]
    info = info.copy()
    info = info[info.label == 1]

    info.loc[info.intrude, "label"] = 1
    info.loc[~info.intrude, "label"] = 0

    return info, {
        "connect": True,
        "intrude": True,
        "owner_to_play": False,
        "owner_filtered": "mixed",
        "experiment": "6-defensive-intrude",
    }


def experiment_7(info):
    """Intrude Defensive Connect

    Rationale: Intrude vs not (when opponent is not connected).
    Differs on the ability of the player to entirely sever the concept structure.
    """
    info = info[~info.connect & ~info.owner_to_play]
    info = info.copy()
    info = info[info.label == 1]

    info.loc[info.intrude, "label"] = 1
    info.loc[~info.intrude, "label"] = 0

    return info, {
        "connect": False,
        "intrude": True,
        "owner_to_play": False,
        "owner_filtered": "mixed",
        "experiment": "7-defensive-intrude",
    }


def experiment_8(info):
    """Intrude Offensive No-Connect

    Rationale: If connected, then the intrusion doesn't make a difference, the
    owner can win either way.
    """
    info = info[~info.connect & info.owner_to_play]
    info = info.copy()
    info = info[info.label == 1]

    info.loc[info.intrude, "label"] = 0
    info.loc[~info.intrude, "label"] = 1

    return info, {
        "connect": False,
        "intrude": True,
        "owner_to_play": True,
        "owner_filtered": "mixed",
        "experiment": "8-offensive-intrude",
    }


def experiment_9(info):
    """Intrude Defensive Connect"""
    info = info[info.connect & info.owner_to_play]
    info = info.copy()
    info = info[info.label == 1]

    info.loc[info.intrude, "label"] = 0
    info.loc[~info.intrude, "label"] = 1

    return info, {
        "connect": True,
        "intrude": True,
        "owner_to_play": True,
        "owner_filtered": "mixed",
        "experiment": "9-offensive-intrude",
    }


def experiments(concept):
    is_negative_concept = concepts.is_negative_concept(concept)
    is_positive_concept = concepts.is_positive_concept(concept)

    if is_negative_concept:
        return [
            experiment_2,
            experiment_3,
        ]

    elif is_positive_concept:
        return [
            experiment_2,
            experiment_3,
            experiment_4,
            experiment_5,
            # Initial experiments showed the following not to have a huge impact.
            # experiment_6,
            # experiment_7,
            # experiment_8,
            # experiment_9,
            # experiment_10,
            # experiment_11,
            # experiment_12,
        ]
    else:
        assert False


def get_probe(probe):
    # seeds are set globally
    if probe == "lr":
        clf = LogisticRegression(
            solver="liblinear",
        )
    elif probe == "mlp":
        clf = MLPClassifier(alpha=0.1)
    return clf


def probe_over_pairs(X, info, probe):
    # info_train, info_test = train_test_split(info, stratify=info.label, test_size=0.25)
    # clf = get_probe(probe)
    # clf = clf.fit(X[info_train.key], info_train.label)
    # score = clf.score(X[info_test.key], info_test.label)
    # return score, len(info_train), len(info_test), clf.coef_
    scores = []
    for train_idx, test_idx in GroupShuffleSplit(n_splits=1, train_size=0.75).split(
        info, groups=info.board_id
    ):
        info_train, info_test = info.iloc[train_idx], info.iloc[test_idx]
        clf = get_probe(probe)
        clf = clf.fit(X[info_train.key], info_train.label)
        score = clf.score(X[info_test.key], info_test.label)
        scores.append(score)
    return np.mean(scores), len(info_train), len(info_test)


def probe_iid(X, info, probe):
    info_train, info_test = train_test_split(info, stratify=info.label, test_size=0.25)
    clf = get_probe(probe)
    clf = clf.fit(X[info_train.key], info_train.label)
    score = clf.score(X[info_test.key], info_test.label)
    return score, len(info_train), len(info_test)


def _get_name(name: str) -> str:
    if "-" in name:
        return name.split("-")[0]
    return name


def probe_over_orientation(X, info, probe):
    # Note: This may not work for edge templates and action
    # prediction, as those actions will be unseen.

    info["metaname"] = info.name.apply(_get_name)
    test_name = random.choice(info.metaname.unique())
    info_train = info[info.metaname != test_name]
    info_test = info[info.metaname == test_name]
    clf = get_probe(probe)
    clf = clf.fit(X[info_train.key], info_train.label)
    score = clf.score(X[info_test.key], info_test.label)
    return score, len(info_train), len(info_test)


def probe_over_position(X, info, probe):
    # Note: This may not work for edge templates and action
    # prediction, as those actions will be unseen.
    scores = []
    for train_idx, test_idx in GroupShuffleSplit(n_splits=1, train_size=0.75).split(
        info, groups=info.position
    ):
        info_train, info_test = info.iloc[train_idx], info.iloc[test_idx]
        clf = get_probe(probe)
        clf = clf.fit(X[info_train.key], info_train.label)
        score = clf.score(X[info_test.key], info_test.label)
        scores.append(score)
    return np.mean(scores), len(info_train), len(info_test)


def main(FLAGS, layer, attacker):
    encode_jobname = FLAGS.jobname.replace("probing", "encode")
    encoding_filename = flags.encoding_filename(FLAGS)
    df = pd.read_table(f"results/{encode_jobname}/{encoding_filename}.tsv")
    df = df.query("attacker == @attacker")
    filename_layer = flags.encoding_filename_layer(FLAGS, layer)
    X = np.load(f"results/{encode_jobname}/{filename_layer}.npy")
    out = []
    EXTRA_SEEDS = 5
    for extra_seed in tqdm.trange(EXTRA_SEEDS, desc="Samples"):
        extra_seed += 5
        utils.seed_everything(extra_seed)
        for exp in tqdm.tqdm(experiments(FLAGS.concept), desc="Experiments"):
            info = df.copy()
            info_exp, metadata = exp(info)
            metadata["num_labels"] = info_exp.label.nunique()
            info_selectivity = info_exp.copy()[info_exp.is_selectivity]
            info_exp = info_exp[~info_exp.is_selectivity]

            if len(info_exp) == 0:
                # option skipped.
                continue

            # IID train test.
            iid_accuracy, iid_train_n, iid_test_n = probe_iid(X, info_exp, FLAGS.probe)
            iid_selective_accuracy, _, _ = probe_iid(X, info_selectivity, FLAGS.probe)
            iid_selectivity = iid_accuracy - iid_selective_accuracy

            pos_accuracy, pos_train_n, pos_test_n = probe_over_position(
                X, info_exp, FLAGS.probe
            )
            pos_selective_accuracy, _, _ = probe_over_position(
                X, info_selectivity, FLAGS.probe
            )
            pos_selectivity = pos_accuracy - pos_selective_accuracy

            results = {
                "iid_accuracy": iid_accuracy,
                "iid_selective_accuracy": iid_selective_accuracy,
                "iid_selectivity": iid_selectivity,
                "iid_train_n": iid_train_n,
                "iid_test_n": iid_test_n,
                "pos_accuracy": pos_accuracy,
                "pos_selective_accuracy": pos_selective_accuracy,
                "pos_selectivity": pos_selectivity,
                "pos_train_n": pos_train_n,
                "pos_test_n": pos_test_n,
                "seed": FLAGS.seed,
                "extra_seed": extra_seed,
                "concept": FLAGS.concept,
                "layer": layer,
                "ckpt_idx": FLAGS.ckpt_idx,
                "templates_per_concept": FLAGS.templates_per_concept,
                "probe": FLAGS.probe,
                "tested_attacker": attacker,
                **metadata,
            }
            out.append(results)
            continue
    df = pd.DataFrame(out)
    return df


import time

if __name__ == "__main__":
    FLAGS = flags.probing().parse_args()
    utils.seed_everything(FLAGS.seed)
    tick = time.perf_counter()
    num_ckpt_idx = flags.get_num_ckpt_idx(FLAGS.run)
    if FLAGS.ckpt_idx >= num_ckpt_idx:
        print("Checkpoint index is out of bounds.")
        exit()

    # We moved layer into the script to reduce the number of jobs (while
    # making each job more expensive.)
    out = []

    for attacker in [0, 1]:
        num_layers = flags.get_num_layers(FLAGS.run)
        for layer in tqdm.trange(num_layers, desc="Layers"):
            df = main(FLAGS, layer, attacker)
            out.append(df)

    final = pd.concat(out)

    filename = flags.filename(FLAGS)
    final.to_csv(f"results/{FLAGS.jobname}/{filename}.tsv", sep="\t", index=False)
    tock = time.perf_counter()
    pd.DataFrame(
        [
            {
                "id": filename,
                "script": {FLAGS.jobname},
                "seconds": tock - tick,
                "concept": FLAGS.concept,
            }
        ]
    ).to_csv(f"times/{FLAGS.jobname}_{filename}.tsv", index=False, sep="\t")
