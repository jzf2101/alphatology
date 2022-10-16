import itertools
import random
import boardlaw_utils

from templates import concepts, neighbors, util

CENTER = (4, 4)


def get_templates_generic(
    schemas,
    templates_per_concept,
    num_rand_to_add,
    conditions,
    generate_templates_func,
    generate_kwargs,
):
    """Returns data used for probing.

    See `generate_templates_probing` for data structure.
    See `template_to_board_probing` for using this structure.
    """
    assert num_rand_to_add % 2 == 0
    templates = []

    # Create templates until we have enough for
    # training, dev, test and stratification.
    board_id = 0

    target = templates_per_concept + 50
    if schemas[0]["concept"] == "bridge":
        # 33% of negative boards have bridges; we'll have to filter these out.
        # we'll generate extra, and then filter out in encode.py.
        target = int(templates_per_concept * 1.6)

    while board_id < target:
        for s in schemas:
            if "edge" in s:
                attacker, defender = get_edge_roles(s)
                roles = [(attacker, defender)]
            else:
                roles = [(0, 1), (1, 0)]
            _conditions = list(_add_roles_to_conditions(conditions, roles))
            # This will be either:
            # templates.probing.generate_templates_probing
            # templates.templates.generate_templates
            schema_templates = generate_templates_func(
                s,
                num_rand_to_add,
                _conditions,
                board_id,
                **generate_kwargs,
            )
            templates.extend(schema_templates)
            board_id += 1
    return templates


def _add_roles_to_conditions(conditions, roles):
    for r in roles:
        role = {"attacker": r[0], "defender": r[1]}
        for c in conditions:
            c = {**c}
            c["roles"] = role
            yield c


def generate_templates(schema, num_rand_to_add: int, conditions, board_id):
    """Positive behavioral tests."""
    generated_templates = []

    for sample in schema_to_template_conditions(
        schema,
        board_id,
        conditions,
        num_rand_to_add=num_rand_to_add,
    ):
        board = get_base_board()
        attacker, defender = sample["attacker"], sample["defender"]
        attacker_c, defender_c = sample["attacker_c"], sample["defender_c"]

        board = util.fill_board(board, sample, attacker_c, defender_c)
        out = {
            "name": schema["name"],
            "concept": schema["concept"],
            "template": mtx_to_str(board),
            "attacker": attacker,
            "defender": defender,
            "tested_agent": {True: attacker, False: defender}[
                schema["defender_to_play"]  # forcing move is the defender if True
            ],
            "c_start": sample["c_start"],
            "r_start": sample["r_start"],
            "position": f"{sample['c_start']}-{sample['r_start']}",
        }
        for k in [
            "intrude",
            "owner_to_play",
            "connect",
            "num_rand_to_add",
            "intrude_forcing",
            "intrude_expected",
        ]:
            if k in sample:
                out[k] = sample[k]

        if "lines" in sample:
            out["lines"] = sample["lines"]

        if "avoid_attacking" in sample:
            blackavoid = (
                sample["avoid_attacking"]
                if attacker == 0
                else sample["avoid_defending"]
            )
            whiteavoid = (
                sample["avoid_attacking"]
                if attacker == 1
                else sample["avoid_defending"]
            )
            out = {
                "blackavoid": cells_to_actions(blackavoid, 0),
                "whiteavoid": cells_to_actions(whiteavoid, 1),
                "cells_used": sample["cells_used"],
                "black_skip": cells_to_actions(blackavoid + whiteavoid, 0),
                "white_skip": cells_to_actions(blackavoid + whiteavoid, 1),
                **out,
            }
        generated_templates.append(out)
    return generated_templates


def schema_to_template(
    schema,
    attacker: int,
    defender: int,
    intrude=False,
    owner_to_play=False,
    connect=True,
    boardsize=9,
    num_rand_to_add=0,
    is_probing=False,
):
    raise DeprecationWarning("Use schema_to_template_conditions.py")


def schema_to_template_conditions(
    schema,
    board_id: int,
    conditions,
    boardsize=9,
    num_rand_to_add=0,
    is_probing=False,
):
    if conditions is None:
        conditions = [
            {
                "connect": False,
                "intrude": False,
                "owner_to_play": False,
                "roles": {"attacker": 0, "defender": 1},
            }
        ]

    concept = schema["concept"]
    cells_used = schema["cells_used"]
    cells_attacking = schema["cells_attacking"]
    cells_defending = schema["cells_defending"]
    is_edge_concept = "edge" in schema
    is_negative_concept = concepts.is_negative_concept(concept)
    is_positive_concept = concepts.is_positive_concept(concept)
    is_internal_concept = "edge" not in schema
    r_max, c_max = get_window(cells_used)
    cells_idx_connect = None
    if "cells_idx_connect" in schema:
        cells_idx_connect = schema["cells_idx_connect"]
    else:
        cells_idx_connect = list(range(len(cells_attacking)))
    if is_internal_concept:
        # NOTE: Change back to 1 in the future.
        padding = 0
    else:
        padding = 0

    if is_negative_concept:
        precondition_valid_negative_schema(schema)
        avoid_attacking = schema["avoid_attacking"]
        avoid_defending = schema["avoid_defending"]
        schema["defender_to_play"] = True

    if is_positive_concept:
        lines = schema["lines"]

    if is_edge_concept:
        loop = edge_to_window_and_orientation(
            schema["edge"], boardsize, r_max, c_max, concept=concept
        )
    else:
        loop = {
            "c_start": list(range(padding, boardsize - c_max - padding)),
            "r_start": list(range(padding, boardsize - r_max - padding)),
            "c_direction": 1,
            "r_direction": 1,
        }
    c_start, r_start = sample_location(loop)
    _cells_attacking = translate(
        cells_attacking,
        r_start,
        c_start,
        loop["r_direction"],
        loop["c_direction"],
    )
    orig_cells_attacking = [*_cells_attacking]
    _cells_defending = translate(
        cells_defending,
        r_start,
        c_start,
        loop["r_direction"],
        loop["c_direction"],
    )
    orig_cells_defending = [*_cells_defending]
    if is_negative_concept:
        _avoid_attacking = translate(
            avoid_attacking,
            r_start,
            c_start,
            loop["r_direction"],
            loop["c_direction"],
        )
        _avoid_defending = translate(
            avoid_defending,
            r_start,
            c_start,
            loop["r_direction"],
            loop["c_direction"],
        )
    if is_positive_concept:
        # assume that the attacker is the one who has the concept (bridge)
        # and that the defender is the one who intrudes into the concept.
        _lines = [
            {
                "forcing": translate(
                    line["forcing"],
                    r_start,
                    c_start,
                    loop["r_direction"],
                    loop["c_direction"],
                ),
                "expected": translate(
                    line["expected"],
                    r_start,
                    c_start,
                    loop["r_direction"],
                    loop["c_direction"],
                ),
            }
            for line in lines
        ]

    _cells_used = translate(
        cells_used,
        r_start,
        c_start,
        loop["r_direction"],
        loop["c_direction"],
    )

    if "escape" in concept or "bottleneck" in concept:
        # For probing train/test splits.
        c_start = schema["c_start"]
        r_start = schema["r_start"]

    if is_probing:
        if concept in {"bottleneck"}:
            _cells_attacking.append(_lines[0]["expected"][0])
            _cells_defending.append(_lines[0]["forcing"][0])
        # if "escape" in concept:
        #     _cells_defending.append(_lines[0]["forcing"][0])

    assert len(_cells_attacking) == len(set(_cells_attacking))
    assert len(_cells_defending) == len(set(_cells_defending))

    intrude_forcing, intrude_expected = None, None

    assert len(_cells_attacking) == len(set(_cells_attacking))
    assert len(_cells_defending) == len(set(_cells_defending))

    # Add the base random locations first.
    num_attackers_to_add, num_defenders_to_add = number_to_add(
        True,
        len(_cells_attacking),
        len(_cells_defending),
        attacker=0,
        defender=1,
    )
    num_attackers_to_add += num_rand_to_add // 2
    num_defenders_to_add += num_rand_to_add // 2
    (
        _cells_attacking,
        _cells_defending,
        _cells_used,
    ) = add_random_and_center_and_fix_to_play(
        _cells_attacking,
        _cells_defending,
        _cells_used,
        num_attackers_to_add,
        num_defenders_to_add,
        padding,
    )

    # For each set of settings, add appropriate additional cells.
    for condition in conditions:
        _cells_defending_condition = [*_cells_defending]
        orig_cells_defending_condition = [*orig_cells_defending]
        orig_cells_attacking_condition = [*orig_cells_attacking]
        _cells_used_condition = [*_cells_used]
        _cells_attacking_condition = [*_cells_attacking]
        intrude = condition["intrude"]
        connect = condition["connect"]
        owner_to_play = condition["owner_to_play"]
        attacker = condition["roles"]["attacker"]
        defender = condition["roles"]["defender"]
        defender_to_play = util.get_defender_to_play(
            schema["defender_to_play"], owner_to_play
        )

        if intrude or owner_to_play:
            assert is_probing

        if schema["defender_to_play"]:
            forcing_player = defender
            expected_player = attacker
        else:
            forcing_player = attacker
            expected_player = defender

        if is_positive_concept:
            _lines_condition = [
                {
                    "forcing": cells_to_actions(line["forcing"], forcing_player),
                    "expected": cells_to_actions(line["expected"], expected_player),
                    # For debugging and visualization.
                    "forcing_cells": line["forcing"],
                    "expected_cells": line["expected"],
                }
                for line in _lines
            ]

        if intrude:
            # WARNING: This is not meant for behavioral tests!
            if is_positive_concept:
                (
                    intrude_forcing,
                    intrude_expected,
                    _cells_defending_condition,
                    orig_cells_defending_condition,
                ) = intrude_given_concept(
                    concept,
                    _lines_condition,
                    _cells_defending_condition,
                    orig_cells_defending_condition,
                )
            else:
                assert False, concept
        else:
            intrude_forcing = intrude_expected = None

        try:
            if connect:
                if is_edge_concept:
                    (
                        _cells_defending_condition,
                        _cells_attacking_condition,
                        _cells_used_condition,
                    ) = connect_edge_given_concept(
                        concept,
                        _cells_attacking_condition,
                        _cells_defending_condition,
                        _cells_used_condition,
                        schema,
                        _lines_condition,
                        cells_idx_connect,
                    )
                else:
                    (
                        _cells_attacking_condition,
                        _cells_used_condition,
                    ) = connect_template(
                        _cells_attacking_condition,
                        _cells_used_condition,
                        attacker,
                        cells_idx_connect,
                    )
            if "cells_idx_connect_defender" in schema:
                cells_idx_connect_defender = schema["cells_idx_connect_defender"]
                (_cells_defending_condition, _cells_used_condition,) = connect_template(
                    _cells_defending_condition,
                    _cells_used_condition,
                    defender,
                    cells_idx_connect_defender,
                )
        except AssertionError:
            # Failed to connect. This is expected; occurs some ~15 per 2500 times.
            continue
        # Add the base random locations first.
        num_attackers_to_add, num_defenders_to_add = number_to_add(
            defender_to_play,
            len(_cells_attacking_condition),
            len(_cells_defending_condition),
            attacker=attacker,
            defender=defender,
        )
        (
            _cells_attacking_condition,
            _cells_defending_condition,
            _cells_used_condition,
        ) = add_random_and_center_and_fix_to_play(
            _cells_attacking_condition,
            _cells_defending_condition,
            _cells_used_condition,
            num_attackers_to_add,
            num_defenders_to_add,
            padding,
        )
        precondition_valid_schema(
            len(_cells_attacking_condition),
            len(_cells_defending_condition),
            defender_to_play,
            attacker,
            defender,
        )

        assert attacker != defender
        attacker_c = ["b", "w"][attacker]
        defender_c = ["b", "w"][defender]
        out = {
            "cells_attacking": _cells_attacking_condition,
            "cells_defending": _cells_defending_condition,
            # "lines": _lines,
            "cells_used": _cells_used_condition,
            "attacker": attacker,
            "defender": defender,
            "intrude": intrude,
            "owner_to_play": owner_to_play,
            "connect": connect,
            "num_rand_to_add": num_rand_to_add,
            # used for building probing minimal pairs.
            "orig_cells_attacking": orig_cells_attacking_condition,
            "orig_cells_defending": orig_cells_defending_condition,
            "c_start": c_start,
            "r_start": r_start,
            "board_id": board_id,
            "attacker_c": attacker_c,
            "defender_c": defender_c,
        }
        out["intrude_forcing"] = intrude_forcing
        out["intrude_expected"] = intrude_expected
        if is_negative_concept:
            out["avoid_attacking"] = _avoid_attacking
            out["avoid_defending"] = _avoid_defending
        if is_positive_concept:
            out["lines"] = _lines_condition
            validate_lines(_lines_condition)
        yield out


def validate_lines(lines):
    for line in lines:
        for m in line["forcing"]:
            assert m >= 0 and m <= 80
        for m in line["expected"]:
            assert m >= 0 and m <= 80


def intrude_given_concept(
    concept,
    _lines_condition,
    _cells_defending_condition,
    orig_cells_defending_condition,
):
    # WARNING: Not functional! Mutates last two arguements.
    # NOTE: Best to explicitily over-ride last two arguements cause of impurity.
    _line = random.choice(_lines_condition)

    if "bottleneck" in concept:
        intrude_forcing = _line["forcing_cells"][1]
        intrude_expected = _line["expected_cells"][1]
    elif "escape" in concept:
        # (block the path to the escape)
        intrude_forcing = random.choice(_line["expected_cells"])
        intrude_expected = _line["expected_cells"][0]
    else:
        intrude_forcing = _line["forcing_cells"][0]
        intrude_expected = _line["expected_cells"][0]
    _cells_defending_condition.append(intrude_forcing)
    orig_cells_defending_condition.append(intrude_forcing)
    return (
        intrude_forcing,
        intrude_expected,
        _cells_defending_condition,
        orig_cells_defending_condition,
    )


def connect_edge_given_concept(
    concept,
    _cells_attacking_condition,
    _cells_defending_condition,
    _cells_used_condition,
    schema,
    _lines_condition,
    cells_idx_connect,
):
    if concept in {"bottleneck"}:
        (_cells_defending_condition, _cells_used_condition,) = connect_edge(
            _cells_defending_condition,
            _cells_used_condition,
            schema["edge"],
            start=_lines_condition[0]["forcing_cells"][0],  # intrusion for bottleneck.
            cells_idx_connect=cells_idx_connect,
        )
    elif "escape" in concept:
        (_cells_attacking_condition, _cells_used_condition,) = connect_edge(
            _cells_attacking_condition,
            _cells_used_condition,
            schema["edge"],
            start=_cells_attacking_condition[1],  # intrusion for bottleneck.
            # not implemented yet.
            cells_idx_connect=cells_idx_connect,
        )
    else:
        (_cells_attacking_condition, _cells_used_condition,) = connect_edge(
            _cells_attacking_condition,
            _cells_used_condition,
            schema["edge"],
            # not implemented yet.
            cells_idx_connect=cells_idx_connect,
        )
    return _cells_defending_condition, _cells_attacking_condition, _cells_used_condition


def sample_location(loop):
    return random.choice(loop["c_start"]), random.choice(loop["r_start"])


def translate(cells, r_start, c_start, r_dir=1, c_dir=1):
    return [(r_start + r_dir * r, c_start + c_dir * c) for r, c in cells]


def get_window(cells_used):
    r_max = max([x[0] for x in cells_used])
    c_max = max([x[1] for x in cells_used])
    return r_max, c_max


def edge_to_window_and_orientation(
    edge: str, boardsize: int, r: int, c: int, concept: str = None
):
    assert concept, "Update function call."
    if (
        concept
        in {
            "bottleneck",
        }
        or "escape" in concept
    ):
        if edge == "BOT":
            return {
                "c_start": [0],
                "r_start": [8],
                "c_direction": 1,
                "r_direction": -1,
            }
        elif edge == "TOP":
            return {
                "c_start": [0],
                "r_start": [0],
                "c_direction": 1,
                "r_direction": 1,
            }
        elif edge == "LEFT":
            return {
                "c_start": [0],
                "r_start": [0],
                "c_direction": 1,
                "r_direction": 1,
            }
        elif edge == "RIGHT":
            return {
                "c_start": [8],
                "r_start": [0],
                "c_direction": -1,
                "r_direction": 1,
            }
    else:
        if edge == "BOT":
            return {
                "c_start": list(range(boardsize - c)),
                "r_start": [8],
                "c_direction": 1,
                "r_direction": -1,
            }
        elif edge == "TOP":
            return {
                "c_start": list(range(boardsize - c)),
                "r_start": [0],
                "c_direction": 1,
                "r_direction": 1,
            }
        elif edge == "LEFT":
            return {
                "c_start": [0],
                "r_start": list(range(boardsize - r)),
                "c_direction": 1,
                "r_direction": 1,
            }
        elif edge == "RIGHT":
            return {
                "c_start": [8],
                "r_start": list(range(boardsize - r)),
                "c_direction": -1,
                "r_direction": 1,
            }
    assert False


def connect_template(_cells_attacking, _cells_used, attacker, cells_idx_connect):
    """NOTE: Assumes defender_to_play."""
    if cells_idx_connect is not None:
        cells_to_connect = [_cells_attacking[idx] for idx in cells_idx_connect]
    else:
        cells_to_connect = _cells_attacking
    add = []
    if attacker == 0:
        top = neighbors.get_topmost(cells_to_connect)
        bot = neighbors.get_botmost(cells_to_connect)
        add.extend(neighbors.connect_up(top, _cells_used))
        add.extend(neighbors.connect_down(bot, _cells_used + add))
    else:
        left = neighbors.get_leftmost(cells_to_connect)
        right = neighbors.get_rightmost(cells_to_connect)
        add.extend(neighbors.connect_left(left, _cells_used))
        add.extend(neighbors.connect_right(right, _cells_used + add))

    _cells_attacking += add
    _cells_used += add
    return _cells_attacking, _cells_used


def connect_edge(
    _cells_attacking, _cells_used, edge, start=None, cells_idx_connect=None
):
    if start is None and cells_idx_connect is not None:
        cells_to_connect = [_cells_attacking[idx] for idx in cells_idx_connect]
        start = _get_start(cells_to_connect, edge)
    elif start is None:
        start = _cells_attacking[0]
    path = _connect_edge(
        start,
        _cells_used,
        edge,
    )
    return _cells_attacking + path, _cells_used + path


def _connect_edge(start, _cells_used, edge):
    if edge == "BOT":
        return neighbors.connect_up(start, _cells_used)
    elif edge == "TOP":
        return neighbors.connect_down(start, _cells_used)
    elif edge == "LEFT":
        return neighbors.connect_right(start, _cells_used)
    elif edge == "RIGHT":
        return neighbors.connect_left(start, _cells_used)


def _get_start(cells_to_connect, edge):
    if edge == "BOT":
        return neighbors.get_topmost(cells_to_connect)
    elif edge == "TOP":
        return neighbors.get_botmost(cells_to_connect)
    elif edge == "LEFT":
        return neighbors.get_rightmost(cells_to_connect)
    elif edge == "RIGHT":
        return neighbors.get_leftmost(cells_to_connect)


# def add_random_and_center_and_fix_to_play(ca, cd, cu, na, nd, padding):
#     add_center = CENTER not in cu
#     if add_center:
#         cells = cu + [CENTER]
#     else:
#         cells = cu

#     if add_center:
#         cells_to_add = get_rand_unused_moves(cells, na + nd + 2 - 1, padding)
#     else:
#         cells_to_add = get_rand_unused_moves(cells, na + nd + 2, padding)

#     # We need to make the center not biases towards either player.
#     # Adding that additional 1-random let's us do that.
#     if add_center:
#         center_and_rand, cells_to_add = [CENTER, cells_to_add[0]], cells_to_add[1:]
#         center_and_rand = util.shuffled(center_and_rand)
#         ca = ca + cells_to_add[:na] + center_and_rand[:1]
#         cd = cd + cells_to_add[na:] + center_and_rand[1:]
#         cu = cu + cells_to_add + center_and_rand
#     else:
#         ca = ca + cells_to_add[: na + 1]
#         cd = cd + cells_to_add[1 + na :]
#         cu = cu + cells_to_add
#     return ca, cd, cu


# def add_random_and_center_and_fix_to_play(ca, cd, cu, na, nd):
#     # NOTE: Temp turning this off.
#     cells_to_add = get_rand_unused_moves(cu, na + nd)
#     ca = ca + cells_to_add[:na]
#     cd = cd + cells_to_add[na:]
#     cu = cu + cells_to_add
#     return ca, cd, cu


def add_random_and_center_and_fix_to_play(ca, cd, cu, na, nd, _padding_unused):
    # NOTE: Temp turning this off.
    add_center = CENTER not in cu
    if add_center:
        cu = cu + [CENTER]
        cd = cd + [CENTER]
        if nd <= 0:
            na += 1
        else:
            nd -= 1
    else:
        cu = cu
    cells_to_add = get_rand_unused_moves(cu, na + nd)
    ca = ca + cells_to_add[:na]
    cd = cd + cells_to_add[na:]
    cu = cu + cells_to_add
    return ca, cd, cu


def number_to_add(
    defender_to_play,
    num_attackers,
    num_defenders,
    attacker,
    defender,
):
    """
    `owner_to_play` has to do with probing; `defender_to_play` is a property
    of the schema itself.
    """
    assert defender != attacker, "Precondition: defender and attacker are different."
    num_defenders_to_add, num_attackers_to_add = 0, 0
    if defender_to_play:
        # if b (0) is defending, we want parity.
        if defender == 0:
            if num_attackers > num_defenders:
                num_defenders_to_add = num_attackers - num_defenders
            else:
                num_attackers_to_add = num_defenders - num_attackers

        # if w (1) is defending, we want +1 attackers.
        elif defender == 1:
            if num_attackers > num_defenders + 1:
                # Too many attackers.
                num_defenders_to_add = num_attackers - (num_defenders + 1)
            elif num_defenders + 1 >= num_attackers:
                num_attackers_to_add = num_defenders + 1 - num_attackers

    else:
        # if b (0) is attacking, we want parity
        if attacker == 0:
            if num_attackers > num_defenders:
                num_defenders_to_add = num_attackers - num_defenders
            else:
                num_attackers_to_add = num_defenders - num_attackers

        # if w (0) is attacking, we want +1 defender
        elif attacker == 1:
            if num_attackers < num_defenders - 1:
                num_attackers_to_add = num_defenders - 1 - num_attackers
            elif num_attackers + 1 > num_defenders:
                num_defenders_to_add = num_attackers + 1 - num_defenders
    return num_attackers_to_add, num_defenders_to_add


def precondition_valid_negative_schema(schema):
    cells_used = schema["cells_used"]
    if "avoid_attacking" in schema:
        for m in schema["avoid_attacking"]:
            assert m in cells_used
    if "avoid_defending" in schema:
        for m in schema["avoid_defending"]:
            assert m in cells_used


def precondition_valid_schema(
    num_attackers, num_defenders, defender_to_play, attacker, defender
):
    assert defender in {0, 1}
    assert attacker in {0, 1}
    assert attacker != defender

    if defender_to_play:
        # if b (0) is defending, we want parity.
        if defender == 0:
            assert (
                num_attackers == num_defenders
            ), f"num_attackers == num_defenders, {num_attackers} != {num_defenders}"

        # if w (1) is defending, we want +1 attackers.
        elif defender == 1:
            assert (
                num_attackers == num_defenders + 1
            ), f"num_attackers == num_defenders + 1, {num_attackers} != {num_defenders + 1}"
    else:
        # if b (0) is attacking, we want parity
        if attacker == 0:
            assert (
                num_attackers == num_defenders
            ), f"num_attackers == num_defenders, {num_attackers} != {num_defenders}"

        # if w (0) is attacking first, we want +1 defender
        elif attacker == 1:
            assert (
                num_attackers + 1 == num_defenders
            ), f"num_attackers + 1 == num_defenders, {num_attackers + 1} != {num_defenders}"


def get_base_board():
    # fmt: off
    board = [
        [".",".",".",".",".",".",".",".",".",],
        [".",".",".",".",".",".",".",".",".", ],
        [".",".",".",".",".",".",".",".",".", ],
        [".",".",".",".",".",".",".",".",".",],
        [".",".",".",".",".",".",".",".",".", ],
        [".",".",".",".",".",".",".",".",".", ],
        [".",".",".",".",".",".",".",".",".",],
        [".",".",".",".",".",".",".",".",".", ],
        [".",".",".",".",".",".",".",".",".", ],
    ]
    # fmt: on
    return board


def get_base_moves(padding=None):
    if padding is not None and padding > 0:
        return list(itertools.product(list(range(0 + padding, 9 - padding)), repeat=2))
    else:
        return list(itertools.product(list(range(0, 9)), repeat=2))


def get_padding_moves():
    return (
        list(itertools.product([0], list(range(9))))
        + list(itertools.product(list(range(9)), [0]))
        + list(itertools.product([8], list(range(9))))
        + list(itertools.product(list(range(9)), [8]))
    )


def get_rand_move(padding=None):
    # randint is inclusive.
    if padding is not None and padding > 0:
        return random.randint(0 + padding, 8 - padding), random.randint(
            0 + padding, 8 - padding
        )
    else:
        return random.randint(0, 8), random.randint(0, 8)


def get_rand_unused_move(board, schema, padding=None):
    # randint is inclusive.
    m = get_rand_move(padding)
    while m in schema["cells_used"] or board[m[0]][m[1]] != ".":
        m = get_rand_move(padding)
    return m


def get_rand_unused_moves_sample(board, schema, n, padding):
    ms = get_base_moves(padding)
    ms = [m for m in ms if m not in schema["cells_used"]]
    ms = [m for m in ms if board[m[0]][m[1]] == "."]
    M = len(ms)
    # if n > M and padding is not None and padding > 0:
    #    padding_cells = get_padding_moves(padding)
    #    padding_cells = [
    #        m
    #        for m in padding_cells
    #        if m not in schema["cells_used"] and board[m[0]][m[1]] == "."
    #    ]
    #     padding_cells = random.sample(padding_cells, n - M)
    #        ms = ms + padding_cells
    #   else:
    #      assert False, f"{M} < {n}"
    return random.sample(ms, n)


def get_rand_unused_moves(cells, n: int, padding=None):
    ms = get_base_moves(padding)
    ms = [m for m in ms if m not in cells]
    M = len(ms)
    # if n > M:
    #   padding_cells = get_padding_moves()
    #  padding_cells = [m for m in padding_cells if m not in cells]
    # padding_cells = random.sample(padding_cells, n - M)
    # ms = ms + padding_cells
    return random.sample(ms, n)


def mtx_to_str(board):
    return "\n".join(["".join(r) for r in board])


def cells_to_actions(cells, agent):
    return [boardlaw_utils.cell_to_action(r, c, agent) for (r, c) in cells]


def get_edge_roles(schema):
    assert "edge" in schema
    if schema["concept"] in {"bottleneck"}:
        attacker = {"TOP": 1, "BOT": 1, "LEFT": 0, "RIGHT": 0}[schema["edge"]]
        defender = {"TOP": 0, "BOT": 0, "LEFT": 1, "RIGHT": 1}[schema["edge"]]
    else:
        attacker = {"TOP": 0, "BOT": 0, "LEFT": 1, "RIGHT": 1}[schema["edge"]]
        defender = {"TOP": 1, "BOT": 1, "LEFT": 0, "RIGHT": 0}[schema["edge"]]
    return attacker, defender
