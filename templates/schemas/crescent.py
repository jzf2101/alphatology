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
schema_1 = dict(
    idea=""".bA
            bBC
            bDb
            """,
    name="pattern1",
    concept="crescent",
    cells_attacking=_schema_1_attacking,
    cells_defending=[],
    cells_used=list(_schema_1_moves.values()) + _schema_1_attacking + [(3, 0), (3, 1)],
    lines=crescent_lines(_schema_1_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cell_moves=list(_schema_1_moves.values()),  # used for detection.
)

_schema_2_moves = {
    "A": (1, 2),
    "B": (1, 1),
    "C": (2, 1),
    "D": (2, 0),
}
_schema_2_attacking = [(0, 2), (1, 0), (0, 1), (3, 0)]
schema_2 = dict(
    idea=""".bb
            bBA
            DC
            b
            """,
    name="pattern2",
    concept="crescent",
    cells_attacking=_schema_2_attacking,
    cells_defending=[],
    cells_used=list(_schema_2_moves.values())
    + _schema_2_attacking
    + [(2, -1), (3, -1)],
    lines=crescent_lines(_schema_2_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cell_moves=list(_schema_2_moves.values()),  # used for detection.
)

_schema_3_moves = {
    "A": (2, 2),
    "B": (1, 2),
    "C": (2, 1),
    "D": (1, 1),
}
_schema_3_attacking = [(0, 3), (0, 2), (1, 3), (2, 0)]
schema_3 = dict(
    idea="""..bb
            .DBb
            bCA
            """,
    name="pattern3",
    concept="crescent",
    cells_attacking=_schema_3_attacking,
    cells_defending=[],
    cells_used=list(_schema_3_moves.values()) + _schema_3_attacking + [(0, 1), (1, 0)],
    lines=crescent_lines(_schema_3_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cell_moves=list(_schema_3_moves.values()),  # used for detection.
)


_schema_4_moves = {
    "A": (0, 2),
    "B": (1, 1),
    "C": (0, 1),
    "D": (1, 0),
}
_schema_4_attacking = [(0, 0), (2, 0), (2, 1), (1, 2)]
schema_4 = dict(
    idea="""bCA
            DBb
            bb.
            """,
    name="pattern4",
    concept="crescent",
    cells_attacking=_schema_4_attacking,
    cells_defending=[],
    cells_used=list(_schema_4_moves.values())
    + _schema_4_attacking
    + [(1, -1), (2, -2)],
    lines=crescent_lines(_schema_4_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cell_moves=list(_schema_4_moves.values()),  # used for detection.
)


_schema_5_moves = {
    "A": (2, 1),
    "B": (1, 1),
    "C": (1, 2),
    "D": (0, 2),
}
_schema_5_attacking = [(2, 0), (0, 1), (1, 0), (0, 3)]
schema_5 = dict(
    idea=""".bDb
            bBC.
            bA
            """,
    name="pattern5",
    concept="crescent",
    cells_attacking=_schema_5_attacking,
    cells_defending=[],
    cells_used=list(_schema_5_moves.values())
    + _schema_5_attacking
    + [(-1, 2), (-1, 3)],
    lines=crescent_lines(_schema_5_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cell_moves=list(_schema_5_moves.values()),  # used for detection.
)

_schema_6_moves = {
    "A": (2, 2),
    "B": (2, 1),
    "C": (1, 2),
    "D": (1, 1),
}
_schema_6_attacking = [(0, 2), (2, 0), (3, 0), (3, 1)]
schema_6 = dict(
    idea="""..b
            .DC
            bBA
            bb.
            """,
    name="pattern6",
    concept="crescent",
    cells_attacking=_schema_6_attacking,
    cells_defending=[],
    cells_used=list(_schema_6_moves.values()) + _schema_6_attacking + [(0, 1), (1, 0)],
    lines=crescent_lines(_schema_6_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cell_moves=list(_schema_6_moves.values()),  # used for detection.
)


def schemas():
    return [schema_1, schema_2, schema_3, schema_4, schema_5, schema_6]
