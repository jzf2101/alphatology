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
    "A": (2, 1),
    "B": (2, 2),
    "C": (2, 3),
    "D": (3, 2),
}
# _schema_1_attacking = [(0, 1), (0, 2), (2, 0), (2, 2)]
_schema_1_attacking = [(1, 2), (1, 3), (3, 1), (3, 3)]
_schema_1_defending = [(3, 0), (4, 0), (4, 1), (4, 2), (1, 4), (2, 4)]
schema_1 = dict(
    idea=""" |
            ..bbw->
             ABCw
            wbDb
          <-www |
            """,
    name="pattern1",
    concept="trapezoid",
    cells_attacking=_schema_1_attacking,
    cells_defending=_schema_1_defending,
    cells_used=list(_schema_1_moves.values())
    + _schema_1_defending
    + _schema_1_attacking,
    lines=trapezoid_lines(_schema_1_moves),
    cell_moves=list(_schema_1_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cells_idx_connect_defender=[0, 5],
)

_schema_2_moves = {
    "C": (1, 2),
    "B": (2, 2),
    "A": (3, 2),
    "D": (2, 1),
}
_schema_2_attacking = [(1, 1), (3, 1), (1, 3), (2, 3)]
_schema_2_defending = [(2, 0), (3, 0), (4, 0), (4, 1), (0, 3)]
schema_2 = dict(
    idea="""|  w->
            *bCb
            wDBb-|
            wbA. v
          <-ww
            """,
    name="pattern2",
    concept="trapezoid",
    cells_attacking=_schema_2_attacking,
    cells_defending=_schema_2_defending,
    cells_used=list(_schema_2_moves.values())
    + _schema_2_defending
    + _schema_2_attacking,
    lines=trapezoid_lines(_schema_2_moves),
    cell_moves=list(_schema_2_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cells_idx_connect_defender=[0, 4],
)

_schema_3_moves = {
    "A": (2, 3),
    "B": (2, 2),
    "C": (2, 1),
    "D": (1, 2),
}
_schema_3_attacking = [(1, 1), (1, 3), (3, 1), (3, 2)]
_schema_3_defending = [(1, 4), (0, 2), (0, 3), (0, 4), (2, 0), (3, 0)]
schema_3 = dict(
    idea="""bDb
            CBA
            bb.
            """,
    name="pattern3",
    concept="trapezoid",
    cells_attacking=_schema_3_attacking,
    cells_defending=_schema_3_defending,
    cells_used=list(_schema_3_moves.values())
    + _schema_3_attacking
    + _schema_3_defending,
    lines=trapezoid_lines(_schema_3_moves),
    cell_moves=list(_schema_3_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cells_idx_connect_defender=[0, 5],
)


_schema_4_moves = {
    "A": (1, 2),
    "B": (2, 2),
    "C": (3, 2),
    "D": (2, 3),
}
_schema_4_attacking = [(2, 1), (1, 3), (3, 1), (3, 3)]
_schema_4_defending = [(1, 5), (0, 3), (0, 4), (1, 4), (4, 2), (4, 1)]
schema_4 = dict(
    idea="""
    .Ab
    bBD
    bCb
        """,
    name="pattern4",
    concept="trapezoid",
    cells_attacking=_schema_4_attacking,
    cells_defending=_schema_4_defending,
    cells_used=list(_schema_4_moves.values())
    + _schema_4_attacking
    + _schema_4_defending,
    lines=trapezoid_lines(_schema_4_moves),
    cell_moves=list(_schema_4_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cells_idx_connect_defender=[0, 5],
)


def schemas():
    return [schema_1, schema_2, schema_3, schema_4]
