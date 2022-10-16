def trapezoid_lines(moves):
    return [
        {
            "forcing": [moves["C"], moves["B"]],
            "expected": [moves["D"], moves["A"]],
        },
        {
            "forcing": [moves["C"], moves["A"]],
            "expected": [moves["D"], moves["B"]],
        },
        # We don't include the shortest path.
    ]


_schema_1_moves = {
    "A": (1, 0),
    "B": (1, 1),
    "C": (1, 2),
    "D": (2, 1),
}
_schema_1_attacking = [(0, 1), (0, 2), (2, 0), (2, 2)]
schema_1 = dict(
    idea=""" |
            .bb
            ABC
            bDb
              |
            """,
    name="pattern1",
    concept="trapezoid",
    cells_attacking=_schema_1_attacking,
    cells_defending=[],
    cells_used=list(_schema_1_moves.values()) + _schema_1_attacking + [(0, 0), (1, 3)],
    lines=trapezoid_lines(_schema_1_moves),
    cell_moves=list(_schema_1_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect=[0, 3],
)

_schema_2_moves = {
    "C": (0, 1),
    "B": (1, 1),
    "A": (2, 1),
    "D": (1, 0),
}
_schema_2_attacking = [(0, 0), (2, 0), (0, 2), (1, 2)]
schema_2 = dict(
    idea="""bCb
            DBb
            bA.
            """,
    name="pattern2",
    concept="trapezoid",
    cells_attacking=_schema_2_attacking,
    cells_defending=[],
    cells_used=list(_schema_2_moves.values()) + _schema_2_attacking + [(2, 2), (-1, 1)],
    lines=trapezoid_lines(_schema_2_moves),
    cell_moves=list(_schema_2_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect=[0, 3],
)

_schema_3_moves = {
    "A": (1, 2),
    "B": (1, 1),
    "C": (1, 0),
    "D": (0, 1),
}
_schema_3_attacking = [(0, 0), (0, 2), (2, 0), (2, 1)]
schema_3 = dict(
    idea="""bDb
            CBA
            bb.
            """,
    name="pattern3",
    concept="trapezoid",
    cells_attacking=_schema_3_attacking,
    cells_defending=[],
    cells_used=list(_schema_3_moves.values()) + _schema_3_attacking + [(1, -1), (2, 2)],
    lines=trapezoid_lines(_schema_3_moves),
    cell_moves=list(_schema_3_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect=[0, 3],
)


_schema_4_moves = {
    "A": (0, 1),
    "B": (1, 1),
    "C": (2, 1),
    "D": (1, 2),
}
_schema_4_attacking = [(1, 0), (0, 2), (2, 0), (2, 2)]
schema_4 = dict(
    idea="""
    .Ab
    bBD
    bCb
        """,
    name="pattern4",
    concept="trapezoid",
    cells_attacking=_schema_4_attacking,
    cells_defending=[],
    cells_used=list(_schema_4_moves.values()) + _schema_4_attacking + [(0, 0), (3, 1)],
    lines=trapezoid_lines(_schema_4_moves),
    cell_moves=list(_schema_4_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect=[0, 3],
)


def schemas():
    return [schema_1, schema_2, schema_3, schema_4]
