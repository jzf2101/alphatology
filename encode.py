"""Encode board states across layers to be process by `probing.py`.
"""
from typing import List, Tuple

import pandas as pd
import torch as th

import flags
import boardlaw_utils
import utils

from templates import probing

import json
import tqdm
import numpy as np

from detect import ConceptDetector


def encode_templates(templates: List) -> Tuple[List, List, List]:
    """Convert the board strings into Hex boards."""
    info = []
    boards = []
    raw_boards = []
    use_concept_detector = templates[-1]["concept"] in {"bridge"}

    if use_concept_detector:
        concept_detector = ConceptDetector(templates[0]["concept"])
    for _, t in enumerate(tqdm.tqdm(templates, desc="Boards")):
        pos, neg, sel_pos, sel_neg = probing.template_to_board_probing(t)

        t_info = {
            k: v
            for k, v in t.items()
            if k
            not in {
                "positive",
                "negative",
                "selectivity_positive",
                "selectivity_negative",
                "cells_used",
            }
        }
        if pos is None or neg is None or sel_pos is None or sel_neg is None:
            continue
        if use_concept_detector:
            if concept_detector(neg):
                print("skipping board; neg board has concept.")
                continue

        info.append(
            {
                "label": 1,
                "is_selectivity": False,
                **t_info,
            }
        )
        boards.append(pos.obs)
        raw_boards.append(t["positive"])
        info.append(
            {
                "label": 0,
                "is_selectivity": False,
                **t_info,
            }
        )
        boards.append(neg.obs)
        raw_boards.append(t["negative"])
        info.append(
            {
                "label": 1,
                "is_selectivity": True,
                **t_info,
            }
        )
        boards.append(sel_pos.obs)
        raw_boards.append(t["selectivity_positive"])
        info.append(
            {
                "label": 0,
                "is_selectivity": True,
                **t_info,
            }
        )
        boards.append(sel_neg.obs)
        raw_boards.append(t["selectivity_negative"])
    return info, boards, raw_boards


def main(FLAGS):
    utils.seed_everything(FLAGS.seed)
    filename = flags.generate_filename(FLAGS)

    jobname = FLAGS.jobname.replace("encode", "generate")
    with open(f"results/{jobname}/{filename}.json", "r") as f:
        templates = json.load(f)
    info, boards, raw_boards = encode_templates(templates)

    df = pd.DataFrame(info)
    df["key"] = df.index
    df["raw"] = raw_boards
    del raw_boards

    num_ckpt_idx = flags.get_num_ckpt_idx(FLAGS.run)
    batch_size = 512

    filename = flags.encoding_filename(FLAGS)
    df.to_csv(f"results/{FLAGS.jobname}/{filename}.tsv", sep="\t", index=False)

    # Encode raw Hex boards with AlphaZero's NN encoder.
    for ckpt_idx in range(num_ckpt_idx):
        FLAGS.ckpt_idx = ckpt_idx
        agent = boardlaw_utils.get_agent_args(FLAGS.run, FLAGS.ckpt_idx, 64)

        num_layers = len(list(agent.network.body.named_children()))
        X = [[] for _ in range(1 + num_layers)]

        values = []
        logits = []
        for idx in tqdm.tqdm(range(0, len(boards), batch_size), desc="Encoding"):
            batch = th.cat(boards[idx : idx + batch_size])

            for name, layer in [(-1, "__raw__")] + list(
                agent.network.body.named_children()
            ):
                if int(name) > -1:
                    with th.no_grad(), th.cuda.amp.autocast():
                        batch = agent.network.body[int(name)](batch)
                X[int(name) + 1].append(
                    batch.detach().squeeze().flatten(1).cpu().numpy()
                )
            with th.no_grad(), th.cuda.amp.autocast():
                value = th.tanh(agent.network.value.core(batch))
                y = agent.network.policy.core(batch)
                y = th.nn.functional.log_softmax(y, -1)
                logits.append(y.detach().cpu().numpy())
            values.append(value.detach().squeeze().cpu().numpy())
        values = np.concatenate(values)
        df[f"values-{ckpt_idx}"] = values

        logits = np.concatenate(logits)
        np.save(f"results/{FLAGS.jobname}/logits_{filename}_{ckpt_idx}.npy", logits)

        for i, layer in enumerate(X):
            filename_layer = flags.encoding_filename_layer(FLAGS, i)
            L = np.concatenate(layer)
            np.save(f"results/{FLAGS.jobname}/{filename_layer}.npy", L)


import time

if __name__ == "__main__":
    tick = time.perf_counter()
    FLAGS = flags.flags().parse_args()

    main(FLAGS)
    tock = time.perf_counter()

    filename = flags.filename(FLAGS)
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
