"""Checks if a negative concept is played into.
"""
from rebar import arrdict
from typing import List, Tuple

import torch as th
import pandas as pd
import tqdm
import copy
from templates import concepts
import boardlaw_utils
import utils
import flags
import boardlaw

import numpy as np


def main(FLAGS):
    utils.seed_everything(FLAGS.seed)
    filename = flags.filename(FLAGS)

    # Number of samples per schema.
    boards, blackavoid, whiteavoid, info, raw = generate_boards(
        FLAGS.concept, FLAGS.templates_per_concept, FLAGS.ckpt_idx, FLAGS.seed, 64
    )
    info = pd.DataFrame(info)
    info["raw"] = raw
    info["blackavoid"] = blackavoid
    info["whiteavoid"] = whiteavoid
    info["board_id"] = np.arange(len(boards))

    NUM_EXTRA_SEED = 1
    _boards = []
    _forcing = []
    _expected = []
    for _ in range(NUM_EXTRA_SEED):
        _boards.extend(copy.deepcopy(boards))
        _forcing.extend(copy.deepcopy(blackavoid))
        _expected.extend(copy.deepcopy(whiteavoid))

    for ckpt_idx in tqdm.trange(flags.get_num_ckpt_idx(FLAGS.run)):
        FLAGS.ckpt_idx = ckpt_idx
        agent = boardlaw_utils.get_agent_args(FLAGS.run, FLAGS.ckpt_idx, 64)
        if agent is None:
            continue
        trace = boardlaw.analysis.rollout(
            arrdict.cat(_boards), [agent, agent], n_reps=1
        )
        r = report(
            trace,
            blackavoid,
            whiteavoid,
        )
        df = info.copy()
        df = pd.merge(df, r, on="board_id")
        df["run"] = FLAGS.run
        df["ckpt_idx"] = FLAGS.ckpt_idx
        filename = flags.filename(FLAGS)
        df.to_csv(f"results/{FLAGS.jobname}/{filename}.tsv", sep="\t", index=False)


def check_violations(
    blackactions: List[int],
    whiteactions: List[int],
    blackavoid: List[int],
    whiteavoid: List[int],
) -> Tuple[int, int, int]:
    whiteviolations = len(set(whiteactions).intersection(set(blackavoid)))
    blackviolations = len(set(blackactions).intersection(set(whiteavoid)))
    return {
        "violations": blackviolations + whiteviolations,
        "blackviolations": blackviolations,
        "whiteviolations": whiteviolations,
    }


def report(trace, blackavoid, whiteavoid):
    """Preductions is one of logits or prior."""
    output = []
    # n_steps, n_envs = trace.decisions.actions.shape
    n_steps_run = trace.transitions.terminal.int().argmax(0)
    n_envs = len(n_steps_run)
    actions = trace.decisions.actions

    for e in range(n_envs):
        n_steps_run_for_e = n_steps_run[e]
        blackactions = actions["0"][:n_steps_run_for_e, e][
            trace.worlds.seats[:n_steps_run_for_e, e] == 1
        ].tolist()
        whiteactions = actions["1"][:n_steps_run_for_e, e][
            trace.worlds.seats[:n_steps_run_for_e, e] == 0
        ].tolist()
        result = check_violations(
            blackactions, whiteactions, blackavoid[e], whiteavoid[e]
        )
        result["board_id"] = e
        output.append(result)
    df = pd.DataFrame(output)
    return df


def generate_boards(
    concept: str,
    num_samples,
    ckpt_idx,
    seed,
    test_nodes,
):
    info = []
    boards = []
    blackavoid = []
    whiteavoid = []
    raw = []

    # Number of (total) random pieces to add to the board.
    templates = concepts.get_negative(concept, num_samples)

    with th.no_grad():
        for template in tqdm.tqdm(templates, desc=f"Generating templates.."):
            try:
                board = boardlaw_utils.from_string(template["template"])
            except:
                print("board filled by chance")
                continue

            # For each forced line test that the agent responds appropriately.
            _blackavoid = template["blackavoid"]
            _whiteavoid = template["whiteavoid"]
            record = {
                "ckpt_idx": ckpt_idx,
                "name": template["name"],
                "seed": seed,
                "test_nodes": test_nodes,
                "concept": template["concept"],
                "attacker": template["attacker"],
                "defender": template["defender"],
                "tested_agent": template["tested_agent"],
            }
            boards.append(board.copy())
            blackavoid.append(_blackavoid)
            whiteavoid.append(_whiteavoid)
            info.append(record)
            raw.append(template["template"])
    return boards, blackavoid, whiteavoid, info, raw


if __name__ == "__main__":
    import time

    FLAGS = flags.flags().parse_args()
    utils.seed_everything(FLAGS.seed)
    tick = time.perf_counter()
    main(FLAGS)
    tock = time.perf_counter()
    filename = flags.filename(FLAGS)
    pd.DataFrame(
        [
            {
                "id": filename,
                "script": FLAGS.jobname,
                "seconds": tock - tick,
                "concept": FLAGS.concept,
            }
        ]
    ).to_csv(f"times_/{FLAGS.jobname}_{filename}.tsv", index=False, sep="\t")
