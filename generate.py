"""Generate raw boards.
"""
import json

import pandas as pd

import flags
import utils
import templates.util
import templates.templates

from templates import concepts
import itertools


def main(FLAGS):
    utils.seed_everything(FLAGS.seed)
    filename = flags.generate_filename(FLAGS)

    NEG_EXAMPLE = "RSA_SHUFFLE_ALL"
    board_options = {
        "intrude": [False],
        "owner_to_play": [True, False],
        "connect": [True, False],
    }
    if FLAGS.concept == "edge":
        board_options["connect"] = [True]
    is_negative_concept = concepts.is_negative_concept(FLAGS.concept)
    if is_negative_concept:
        board_options["intrude"] = [False]
    if is_negative_concept:
        board_options["connect"] = [False]
    moves = [m for m in templates.templates.get_base_moves()]
    selectivity_mask = {
        k: list(v)
        for k, v in zip(
            moves,
            templates.util.shuffled(moves),
        )
    }
    conditions = itertools.product(*board_options.values())
    keys = list(board_options.keys())
    conditions = [{k: v for k, v in zip(keys, vals)} for vals in conditions]
    generated_templates = concepts.get_probing(
        FLAGS.concept,
        FLAGS.templates_per_concept,
        conditions,
        NEG_EXAMPLE,
        0,
        selectivity_mask,
    )
    selectivity_mask = {
        "-".join([str(i) for i in k]): "-".join([str(i) for i in v])
        for k, v in selectivity_mask.items()
    }
    with open(f"results/{FLAGS.jobname}/selectivity-{filename}.json", "w") as f:
        json.dump(selectivity_mask, f)
    with open(f"results/{FLAGS.jobname}/{filename}.json", "w") as f:
        json.dump(generated_templates, f)


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
