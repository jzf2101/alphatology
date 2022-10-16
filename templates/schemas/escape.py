"""Defense against bottlenecks:
1. Tests bottleneck.
2. Tests agent understands that they must repond to each move.

This file is highly tested, but terribly ugly.
"""


def escape_lines(
    forcing,
    expected,
    bottleneck_idx: int,
    bottleneck_to_center: int,
    forcing_idx: int = 0,
    expected_idx: int = 0,
    N: int = 2,
):
    start = bottleneck_idx - 1
    right_forcing = [
        forcing[n] for n in range(bottleneck_idx + forcing_idx, 9 - forcing_idx)
    ]
    right_expected = expected  # : bottleneck_idx + N + 1]

    return [
        {
            "expected": [
                *right_forcing[:N],
                right_expected[
                    N + expected_idx + bottleneck_idx
                ],  # [N + expected_idx + 1],
            ],
            "forcing": right_expected[
                expected_idx + start : N + expected_idx + bottleneck_idx
            ],
        },
        {
            "expected": [
                *right_forcing[:N],
                right_expected[N + start + expected_idx],
            ],
            "forcing": [
                *right_expected[expected_idx + start : expected_idx + start + N],
                right_expected[N + expected_idx + bottleneck_idx],
            ],
        },
    ]


def generate_schemas_bot(N):
    forcing = [(1, i) for i in range(9)]
    expected = [(0, i) for i in range(9)]

    s = []

    for start in range(9 - 2 - 1):
        bottleneck_idx = 1 + start
        attacking = [(1, bottleneck_idx + N), (2, 1 + start)]
        if bottleneck_idx + N >= 8:
            continue
        defending = [(2, start), (2, 2 + start)]

        avoid = [(2, i) for i in range(9)]
        schema = dict(
            idea="""wXw......
                    01234578
                    ABCDEFGHI
                    """,
            name=f"bot-{start}",
            concept=f"escape-{N}",
            cells_attacking=attacking,
            cells_defending=defending,
            cells_used=attacking + defending + forcing + expected + avoid,
            lines=escape_lines(
                forcing,
                expected,
                bottleneck_idx,
                -1,
                N=N,
            ),
            defender_to_play=True,
            edge="BOT",
            c_start=start,
            r_start=1,
        )
        s.append(schema)

    # NOTE: We're only going right to escape.
    return s


def generate_schemas_top(N):
    forcing = [(1, i) for i in range(9)]
    expected = [(0, i) for i in range(9)]

    s = []
    for start in range(9 - 3 - 1):
        bottleneck_idx = 1 + start

        attacking = [(1, 1 + bottleneck_idx + N), (2, start + 1)]
        if bottleneck_idx + 1 + N >= 8:
            continue
        defending = [(2, start), (2, start + 2)]

        avoid = [(2, i) for i in range(9)]

        schema = dict(
            idea="""wXw......
                    012345678
                    ABCDEFGHI
                    """,
            name=f"top-{start}",
            concept=f"escape-{N}",
            cells_attacking=attacking,
            cells_defending=defending,
            cells_used=attacking + defending + forcing + expected + avoid,
            lines=escape_lines(
                forcing,
                expected,
                bottleneck_idx,
                +1,
                forcing_idx=1,
                expected_idx=2,
                N=N,
            ),
            defender_to_play=True,
            edge="TOP",
            c_start=start,
            r_start=1,
        )
        s.append(schema)
    return s


def generate_schemas_left(N):
    forcing = [(i, 1) for i in range(9)]
    expected = [(i, 0) for i in range(9)]

    s = []
    for start in range(9 - 3 - 1):
        bottleneck_idx = 1 + start

        attacking = [(1 + bottleneck_idx + N, 1), (start + 1, 2)]
        if bottleneck_idx + 1 + N >= 8:
            continue
        defending = [(start, 2), (2 + start, 2)]

        avoid = [(i, 2) for i in range(9)]
        schema = dict(
            idea="""wXw......
                    012345678
                    ABCDEFGHI
                    """,
            name=f"left-{start}",
            concept=f"escape-{N}",
            cells_attacking=attacking,
            cells_defending=defending,
            cells_used=attacking + forcing + defending + expected + avoid,
            lines=escape_lines(
                forcing,
                expected,
                bottleneck_idx,
                +1,
                forcing_idx=1,
                expected_idx=2,
                N=N,
            ),
            defender_to_play=True,
            edge="LEFT",
            c_start=1,
            r_start=start,
        )
        s.append(schema)
    return s


def generate_schemas_right(N):
    forcing = [(i, 1) for i in range(9)]
    expected = [(i, 0) for i in range(9)]

    s = []
    for start in range(9 - 2 - 1):
        bottleneck_idx = 1 + start

        attacking = [(bottleneck_idx + N, 1), (start + 1, 2)]
        if bottleneck_idx + N >= 8:
            continue
        defending = [(start, 2), (2 + start, 2)]

        avoid = [(i, 2) for i in range(9)]
        schema = dict(
            idea="""wXw......
                    012345678
                    ABCDEFGHI
                    """,
            name=f"right-{start}",
            concept=f"escape-{N}",
            cells_attacking=attacking,
            cells_defending=defending,
            cells_used=attacking + defending + forcing + expected + avoid,
            lines=escape_lines(
                forcing,
                expected,
                bottleneck_idx,
                -1,
                N=N,
            ),
            defender_to_play=True,
            edge="RIGHT",
            c_start=1,
            r_start=start,
        )
        s.append(schema)
    return s


def schemas():
    out = []

    for N in range(2, 6):
        out.extend(
            [
                *generate_schemas_bot(N),
                *generate_schemas_top(N),
                *generate_schemas_left(N),
                *generate_schemas_right(N),
            ]
        )
    return out
