from rebar import arrdict

import torch as th
import pandas as pd
import os
import tqdm
import copy
from templates import concepts
import boardlaw_utils
import utils
import flags

from scipy import stats
import numpy as np


def combine_actions(decisions, masks):
    actions = th.cat([d.actions for d in decisions.values()])
    for mask, decision in zip(masks.values(), decisions.values()):
        actions[mask] = decision.actions
    return actions


def lines_to_tensor(lines):
    # ENV x LIST OF ACTIONS
    max_actions = max(len(l) for l in lines)
    n_envs = len(lines)
    assert max_actions < n_envs
    x = th.ones((max_actions, n_envs)) * -1
    for i, l in enumerate(lines):
        for j, m in enumerate(l):
            x[j][i] = m
    x = x.int()  # (np.int64)
    return x


def get_n_actions(lines):
    return th.tensor([len(l) for l in lines])


@th.no_grad()
def positive(worlds, agent, lines_forcing, lines_expected):
    assert worlds.seats.shape[0] == len(lines_forcing), (
        worlds.seats.shape[0],
        len(lines_forcing),
    )
    lines_forcing_t = lines_to_tensor(lines_forcing).to("cuda").type(th.int64)
    lines_expected_t = lines_to_tensor(lines_expected).to("cuda").type(th.int64)

    trace, dtrace = [], []

    j = 0
    finished_test = th.zeros(worlds.n_envs, dtype=bool, device="cuda")
    n_steps = lines_forcing_t.shape[0] * 2
    worlds_current = worlds
    for j in range(n_steps):
        is_forcing_step = (j % 2) == 0
        round = j // 2

        if is_forcing_step:
            decisions, masks = {}, {}
            # exclude actions outside the test.

            finished_test = lines_forcing_t[round] < 0
            test_mask = ~finished_test

            i = "forcing"
            if test_mask.any():
                decisions[i] = arrdict.arrdict(
                    actions=lines_forcing_t[round, test_mask], valid=test_mask
                )
                masks[i] = test_mask

            i = "unused"
            if finished_test.any():
                decisions[i] = agent(worlds_current[finished_test], eval=True)
                masks[i] = finished_test
            actions = combine_actions(decisions, masks)
        else:
            actual_decisions = agent(worlds_current, eval=True)
            decisions, masks = {}, {}

            finished_test = lines_expected_t[round] < 0
            test_mask = ~finished_test

            i = "expected"
            if test_mask.any():
                decisions[i] = arrdict.arrdict(
                    actions=lines_expected_t[round, test_mask], valid=test_mask
                )
                masks[i] = test_mask

            i = "unused"
            if finished_test.any():
                decisions[i] = agent(worlds_current[finished_test], eval=True)
                masks[i] = finished_test

            actions = combine_actions(decisions, masks)
            # Capture the decisions the model would have made, including the logits.
            dtrace.append(actual_decisions)

        worlds_current, transitions = worlds_current.step(actions)
        trace.append(
            arrdict.arrdict(
                # Note actions are simply from the test defintion (not the agent).
                actions=actions,
                transitions=transitions,
                worlds_current=worlds_current,
            )
        )

    trace = arrdict.stack(trace)
    trace["decisions"] = arrdict.stack(dtrace)
    return trace


def report(predictions, expected: th.tensor, n_extra_seed, prefix):
    """Preductions is one of logits or prior."""
    output = []
    n_steps, n_envs = expected.shape
    for s in range(n_steps):
        for e in range(n_envs):
            # Although (now) all lines are of the same length,
            # exit early if needed.
            if expected[s, e] < 0:
                continue

            # Collect logit scores.
            data = []
            for i in range(n_extra_seed):
                d = predictions[s][e + i * n_envs]
                data.append(d)
            arr = np.array(data)
            arr[arr == -np.inf] = np.nan
            med = np.nanmedian(arr, 0)

            # Find outliers and compute scores.
            med = (med - np.nanmean(med)) / np.nanstd(med)
            z = stats.zscore(med, nan_policy="omit")

            expected_idx = expected[s, e].item()
            score = z[expected_idx]
            top1 = expected_idx == np.nanargmax(med)
            z_nonan = z[z != np.nan]
            output.append(
                {
                    "top1": top1,
                    "expected_idx": expected_idx,
                    "best_idx": np.nanargmax(z),
                    "best_z": z[np.nanargmax(z)],
                    "z@1": score >= 1,
                    "z@2": score >= 2,
                    "z@3": score >= 3,
                    "#z>1": sum(z_nonan >= 1),
                    "#z>2": sum(z_nonan >= 2),
                    "#z>3": sum(z_nonan >= 3),
                    "z": score,
                    "template_step": s,
                    "env_id": e,
                }
            )
    df = pd.DataFrame(output)
    df = df.add_prefix(prefix)
    return df


def generate_boards(concept: str, num_samples: int, seed: int):
    info = []
    boards = []
    forcing = []
    expected = []
    raw = []

    # Number of (total) random pieces to add to the board.
    templates = concepts.get_positive(concept, num_samples, 0)
    with th.no_grad():
        for template in tqdm.tqdm(templates, desc=f"Generating templates.."):
            try:
                board = boardlaw_utils.from_string(template["template"])
            except:
                print("board filled by chance")
                continue

            # For each forced line test that the agent responds appropriately.
            for test_idx, test in enumerate(template["lines"]):
                forcing_actions = test["forcing"]
                expected_actions = test["expected"]
                record = {
                    # "ckpt_idx": ckpt_idx,
                    "name": template["name"],
                    "seed": seed,
                    "concept": template["concept"],
                    "test_idx": test_idx,
                    "attacker": template["attacker"],
                    "defender": template["defender"],
                    "tested_agent": template["tested_agent"],
                }
                boards.append(board.copy())
                forcing.append(forcing_actions)
                expected.append(expected_actions)
                info.append(record)
                raw.append(template["template"])
    return boards, forcing, expected, info, raw


def main(FLAGS):
    utils.seed_everything(FLAGS.seed)

    # Number of samples per schema.
    boards, forcing, expected, info, raw = generate_boards(
        FLAGS.concept, FLAGS.templates_per_concept, FLAGS.seed
    )
    info = pd.DataFrame(info)
    info["raw"] = raw
    info["expected"] = expected
    info["forcing"] = forcing
    info["env_id"] = np.arange(len(boards))

    NUM_EXTRA_SEED = 32
    _boards = []
    _forcing = []
    _expected = []
    for _ in range(NUM_EXTRA_SEED):
        _boards.extend(copy.deepcopy(boards))
        _forcing.extend(copy.deepcopy(forcing))
        _expected.extend(copy.deepcopy(expected))

    for ckpt_idx in tqdm.trange(flags.get_num_ckpt_idx(FLAGS.run)):
        FLAGS.ckpt_idx = ckpt_idx
        agent = boardlaw_utils.get_agent_args(FLAGS.run, FLAGS.ckpt_idx, 64)
        if agent is None:
            continue
        trace = positive(arrdict.cat(_boards), agent, _forcing, _expected)
        expected_t = lines_to_tensor(expected)
        logits_report = report(
            trace.decisions.logits.cpu().numpy(),
            expected_t,
            NUM_EXTRA_SEED,
            "logits_",
        )
        prior_report = report(
            trace.decisions.prior.cpu().numpy(), expected_t, NUM_EXTRA_SEED, "prior_"
        )

        df = info.copy()
        df = pd.merge(df, logits_report, left_on="env_id", right_on="logits_env_id")
        df = pd.merge(
            df,
            prior_report,
            left_on=["env_id", "logits_template_step"],
            right_on=["prior_env_id", "prior_template_step"],
        )
        df["run"] = FLAGS.run
        df["ckpt_idx"] = FLAGS.ckpt_idx
        filename = flags.filename(FLAGS)
        df.to_csv(f"results/{FLAGS.jobname}/{filename}.tsv", sep="\t", index=False)

    import pickle

    # only save the last trace.
    with open(f"results/{FLAGS.jobname}/{filename}.pkl", "wb") as f:
        pickle.dump(trace, f)


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
