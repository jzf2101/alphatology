def crescent_lines(moves):
    return [
        {
            "forcing": [moves["D"], moves["B"]],
            "expected": [moves["C"], moves["A"]],
        },
        {
            "forcing": [moves["D"], moves["A"]],
            "expected": [moves["C"], moves["B"]],
        },
        # {
        #     "forcing": [moves["C"]],
        #     "expected": [moves["D"]],
        # },
    ]


_schema_1_moves = {
    "A": (0, 2),
    "B": (1, 1),
    "C": (1, 2),
    "D": (2, 1),
}
_schema_1_attacking = [(0, 1), (1, 0), (2, 0), (2, 2)]
_schema_1_defending = [(3, 0), (3, 1), (1, 3), (0, 3)]
schema_1 = dict(
    idea=""".bA
            bBC
            bDb
            """,
    name="pattern1",
    concept="crescent",
    cells_attacking=_schema_1_attacking,
    cells_defending=_schema_1_defending,
    cells_used=list(_schema_1_moves.values())
    + _schema_1_attacking
    + _schema_1_defending,
    lines=crescent_lines(_schema_1_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cells_idx_connect_defender=[0, 3],
    cell_moves=list(_schema_1_moves.values()),  # used for detection.
)

_schema_2_moves = {
    "A": (1, 3),
    "B": (1, 2),
    "C": (2, 2),
    "D": (2, 1),
}
_schema_2_attacking = [(0, 3), (1, 1), (0, 2), (3, 1)]
_schema_2_defending = [(2, 0), (3, 0), (2, 3), (1, 4)]
schema_2 = dict(
    idea=""".bb
            bBA
            DC
            b
            """,
    name="pattern2",
    concept="crescent",
    cells_attacking=_schema_2_attacking,
    cells_defending=_schema_2_defending,
    cells_used=list(_schema_2_moves.values())
    + _schema_2_attacking
    + _schema_2_defending,
    lines=crescent_lines(_schema_2_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cells_idx_connect_defender=[0, 3],
    cell_moves=list(_schema_2_moves.values()),  # used for detection.
)

_schema_3_moves = {
    "A": (2, 2),
    "B": (1, 2),
    "C": (2, 1),
    "D": (1, 1),
}
_schema_3_attacking = [(0, 3), (0, 2), (1, 3), (2, 0)]
_schema_3_defending = [(1, 0), (0, 1), (3, 1), (3, 2)]
schema_3 = dict(
    idea="""..bb
            .DBb
            bCA
            """,
    name="pattern3",
    concept="crescent",
    cells_attacking=_schema_3_attacking,
    cells_defending=_schema_3_defending,
    cells_used=list(_schema_3_moves.values())
    + _schema_3_attacking
    + _schema_3_defending,
    lines=crescent_lines(_schema_3_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cells_idx_connect_defender=[0, 3],
    cell_moves=list(_schema_3_moves.values()),  # used for detection.
)


_schema_4_moves = {
    "A": (1, 3),
    "B": (2, 2),
    "C": (1, 2),
    "D": (2, 1),
}
_schema_4_attacking = [(1, 1), (3, 1), (3, 2), (2, 3)]
_schema_4_defending = [(0, 3), (0, 2), (2, 0), (3, 0)]
schema_4 = dict(
    idea="""bCA
            DBb
            bb.
            """,
    name="pattern4",
    concept="crescent",
    cells_attacking=_schema_4_attacking,
    cells_defending=_schema_4_defending,
    cells_used=list(_schema_4_moves.values())
    + _schema_4_attacking
    + _schema_4_defending,
    lines=crescent_lines(_schema_4_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cells_idx_connect_defender=[0, 3],
    cell_moves=list(_schema_4_moves.values()),  # used for detection.
)


def schemas():
    return [schema_1, schema_2, schema_3, schema_4]
