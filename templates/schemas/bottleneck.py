"""Defense against bottlenecks:
1. Tests bottleneck.
2. Tests agent understands that they must repond to each move.
"""


def bottleneck_lines(
    forcing,
    expected,
    intrusion,
    bottleneck_dim: int,
    bottleneck_to_center: int,
    forcing_idx: int = 0,
    expected_idx: int = 0,
):
    """
    attacker =
    .wXw.....
    987654321
    ABCDEFGHI
    """
    center = expected[bottleneck_dim + bottleneck_to_center]
    left_forcing = [
        forcing[n]
        for n in range(
            bottleneck_dim + bottleneck_to_center - forcing_idx, 0 - forcing_idx, -1
        )
    ]
    left_expected = [
        expected[i - 1] for i in range(bottleneck_dim + bottleneck_to_center, 0, -1)
    ]

    right_forcing = [
        forcing[n] for n in range(bottleneck_dim + forcing_idx, 9 - forcing_idx)
    ]
    right_expected = expected[bottleneck_dim + expected_idx :]
    return [
        {
            "forcing": [intrusion, *right_forcing, *left_forcing],
            "expected": [center, *right_expected, *left_expected],
        }
    ]


def generate_schemas_bot():
    forcing = [(1, i) for i in range(9)]
    expected = [(0, i) for i in range(9)]

    s = []
    # -1 (padding)
    # -3 (size of pattern)
    for start in range(1, 9 - 3 - 1):
        bottleneck_idx = 1 + start
        attacking = [(2, start), (2, 2 + start)]
        avoid = [(2, i) for i in range(9)]
        schema = dict(
            idea="""wXw......
                    012345678
                    ABCDEFGHI
                    """,
            name=f"bot-{start}",
            concept="bottleneck",
            cells_attacking=attacking,
            cells_defending=[],
            cells_used=attacking + forcing + expected + avoid,
            lines=bottleneck_lines(
                forcing, expected, (2, bottleneck_idx), bottleneck_idx, -1
            ),
            defender_to_play=True,
            c_start=start,
            r_start=1,
            edge="BOT",
        )
        s.append(schema)
    return s


def generate_schemas_top():
    forcing = [(1, i) for i in range(9)]
    expected = [(0, i) for i in range(9)]

    s = []
    # -1 (padding)
    # -3 (size of pattern)
    for start in range(1, 9 - 3 - 1):
        bottleneck_idx = 1 + start
        attacking = [(2, start), (2, 2 + start)]
        avoid = [(2, i) for i in range(9)]
        schema = dict(
            idea="""wXw......
                    012345678
                    ABCDEFGHI
                    """,
            name=f"top-{start}",
            concept="bottleneck",
            cells_attacking=attacking,
            cells_defending=[],
            cells_used=attacking + forcing + expected + avoid,
            lines=bottleneck_lines(
                forcing,
                expected,
                (2, bottleneck_idx),
                bottleneck_idx,
                +1,
                forcing_idx=1,
                expected_idx=2,
            ),
            defender_to_play=True,
            c_start=start,
            r_start=1,
            edge="TOP",
        )
        s.append(schema)
    return s


def generate_schemas_left():
    forcing = [(i, 1) for i in range(9)]
    expected = [(i, 0) for i in range(9)]

    s = []
    # -1 (padding)
    # -3 (size of pattern)
    for start in range(1, 9 - 3 - 1):
        bottleneck_idx = 1 + start
        attacking = [(start, 2), (2 + start, 2)]
        avoid = [(i, 2) for i in range(9)]
        schema = dict(
            idea="""wXw......
                    012345678
                    ABCDEFGHI
                    """,
            name=f"left-{start}",
            concept="bottleneck",
            cells_attacking=attacking,
            cells_defending=[],
            cells_used=attacking + forcing + expected + avoid,
            lines=bottleneck_lines(
                forcing,
                expected,
                (bottleneck_idx, 2),
                bottleneck_idx,
                +1,
                forcing_idx=1,
                expected_idx=2,
            ),
            defender_to_play=True,
            edge="LEFT",
            c_start=1,
            r_start=start,
        )
        s.append(schema)
    return s


def generate_schemas_right():
    forcing = [(i, 1) for i in range(9)]
    expected = [(i, 0) for i in range(9)]

    s = []
    # -1 (padding)
    # -3 (size of pattern)
    for start in range(1, 9 - 3 - 1):
        bottleneck_idx = 1 + start
        attacking = [(start, 2), (2 + start, 2)]
        avoid = [(i, 2) for i in range(9)]
        schema = dict(
            idea="""wXw......
                    012345678
                    ABCDEFGHI
                    """,
            name=f"right-{start}",
            concept="bottleneck",
            cells_attacking=attacking,
            cells_defending=[],
            cells_used=attacking + forcing + expected + avoid,
            lines=bottleneck_lines(
                forcing, expected, (bottleneck_idx, 2), bottleneck_idx, -1
            ),
            defender_to_play=True,
            edge="RIGHT",
            c_start=1,
            r_start=start,
        )
        s.append(schema)
    return s


def schemas():
    return [
        *generate_schemas_bot(),
        *generate_schemas_top(),
        *generate_schemas_left(),
        *generate_schemas_right(),
    ]
