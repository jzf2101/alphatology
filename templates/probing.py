import copy

import itertools
import random

import boardlaw_utils

import templates.util as util
import templates.templates


def get_templates(
    schemas,
    templates_per_concept,
    neg_example,
    num_rand_to_add,
    conditions,
    selectivity_mask,
):
    """Returns data used for probing.

    See `generate_templates_probing` for data structure.
    See `template_to_board_probing` for using this structure.
    """
    return templates.templates.get_templates_generic(
        schemas,
        templates_per_concept,
        num_rand_to_add,
        conditions,
        generate_templates_probing,
        generate_kwargs=dict(
            neg_example=neg_example,
            selectivity_mask=selectivity_mask,
        ),
    )


def template_to_board_probing(template):
    """Generates boards from the template with moves added."""
    try:
        positive = boardlaw_utils.from_string(template["positive"])
    except AssertionError:
        positive = None
    try:
        negative = boardlaw_utils.from_string(template["negative"])
    except AssertionError:
        negative = None
    try:
        selectivity_positive = boardlaw_utils.from_string(
            template["selectivity_positive"]
        )
    except AssertionError:
        selectivity_positive = None
    try:
        selectivity_negative = boardlaw_utils.from_string(
            template["selectivity_negative"]
        )
    except AssertionError:
        selectivity_negative = None
    return (positive, negative, selectivity_positive, selectivity_negative)


def generate_templates_probing(
    schema, num_rand_to_add, conditions, board_id, neg_example, selectivity_mask
):
    """Probing.

    Generates minimal pairs of 1 to @min_diff between concept and not.
    """
    generated_templates = []
    for sample in templates.templates.schema_to_template_conditions(
        schema,
        board_id,
        conditions,
        num_rand_to_add=num_rand_to_add,
        is_probing=True,
    ):
        attacker_c, defender_c = sample["attacker_c"], sample["defender_c"]

        # positive
        board = templates.templates.get_base_board()
        board = util.fill_board(board, sample, attacker_c, defender_c)

        # negative
        neg_board = copy.deepcopy(board)

        is_internal_concept = "edge" not in schema
        if is_internal_concept:
            # NOTE: Change back to 1 in the future.
            padding = 0
        else:
            padding = 0

        # DEFAULT
        if neg_example == "RSA_SHUFFLE_ALL":
            def_cells = definitional_cells_all(sample, attacker_c, defender_c)
            rnd_cells = templates.templates.get_rand_unused_moves_sample(
                neg_board, schema, len(def_cells), padding
            )
            for ((x, y), c), (rx, ry) in zip(def_cells, rnd_cells):
                # remove definitional cell
                assert neg_board[x][y] == c
                neg_board[x][y] = "."

                # add random cell
                neg_board[rx][ry] = c
        elif neg_example == "RSO_SHUFFLE_ONE":
            for ((x, y), c) in definitional_attacking_cells_all(
                sample, attacker_c, defender_c
            ):
                # remove definitional cell
                assert neg_board[x][y] == c
                neg_board[x][y] = "."

                # add random cell
                rx, ry = templates.templates.get_rand_unused_move(
                    neg_board, sample, padding
                )
                neg_board[rx][ry] = c
                break
        else:
            assert False, neg_example

        # selectivity
        if selectivity_mask is not None:
            selectivity_board_pos = util.map_board_given_board(board, selectivity_mask)
            selectivity_board_neg = util.map_board_given_board(
                neg_board, selectivity_mask
            )
        out = {
            "name": schema["name"],
            "concept": schema["concept"],
            "positive": templates.templates.mtx_to_str(board),
            "negative": templates.templates.mtx_to_str(neg_board),
            "neg_example": neg_example,
            "num_rand_to_add": num_rand_to_add,
            "position": f"{sample['c_start']}-{sample['r_start']}",
            "board_id": board_id,
        }
        if "lines" in sample:
            out["lines"] = sample["lines"]

        if selectivity_mask is not None:
            out["selectivity_positive"] = templates.templates.mtx_to_str(
                selectivity_board_pos
            )
            out["selectivity_negative"] = templates.templates.mtx_to_str(
                selectivity_board_neg
            )
        out = {**sample, **out}
        generated_templates.append(out)
    return generated_templates


def definitional_cells_all(sample, attacker_c, defender_c):
    assert len(sample["orig_cells_attacking"]) == len(
        set(sample["orig_cells_attacking"])
    )
    assert len(sample["orig_cells_defending"]) == len(
        set(sample["orig_cells_defending"])
    )
    assert not set(sample["orig_cells_defending"]).intersection(
        set(sample["orig_cells_attacking"])
    )

    return util.shuffled(
        itertools.chain(
            itertools.zip_longest(
                sample["orig_cells_attacking"], [], fillvalue=attacker_c
            ),
            itertools.zip_longest(
                sample["orig_cells_defending"], [], fillvalue=defender_c
            ),
        )
    )


def definitional_attacking_cells_all(sample, attacker_c, defender_c):
    assert len(sample["orig_cells_attacking"]) == len(
        set(sample["orig_cells_attacking"])
    )
    assert len(sample["orig_cells_defending"]) == len(
        set(sample["orig_cells_defending"])
    )
    assert not set(sample["orig_cells_defending"]).intersection(
        set(sample["orig_cells_attacking"])
    )

    return util.shuffled(
        itertools.chain(
            itertools.zip_longest(
                sample["orig_cells_attacking"], [], fillvalue=attacker_c
            ),
        )
    )
