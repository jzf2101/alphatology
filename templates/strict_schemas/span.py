def span_lines(moves):
    return [
        # {
        #     "forcing": [moves["D"]],
        #     "expected": [moves["F"]],
        # },
        # {
        #     "forcing": [moves["E"]],
        #     "expected": [moves["F"]],
        # },
        {
            "forcing": [moves["F"], moves["C"], moves["A"]],
            "expected": [moves["B"], moves["E"], moves["D"]],
        },
        {
            "forcing": [moves["F"], moves["C"], moves["D"]],
            "expected": [moves["B"], moves["E"], moves["A"]],
        },
        {
            "forcing": [moves["F"], moves["E"], moves["A"]],
            "expected": [moves["B"], moves["C"], moves["D"]],
        },
        {
            "forcing": [moves["F"], moves["E"], moves["D"]],
            "expected": [moves["B"], moves["C"], moves["A"]],
        },
    ]


_schema_1_moves = {
    "A": (1, 1),
    "B": (1, 2),
    "C": (1, 3),
    "D": (2, 1),
    "E": (2, 2),
    "F": (3, 1),
}
_schema_1_attacking = [(2, 0), (3, 0), (2, 3), (3, 2)]
_schema_1_defending = [(0, 3), (0, 1), (0, 2), (4, 1), (4, 0)]
schema_1 = dict(
    idea=""".ABC.
            bDEb
            bFb.
            **
            """,
    name="pattern1",
    concept="span",
    cells_attacking=_schema_1_attacking,
    cells_defending=_schema_1_defending,
    cells_used=list(_schema_1_moves.values())
    + _schema_1_attacking
    + _schema_1_defending,
    lines=span_lines(_schema_1_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cells_idx_connect_defender=[0, 4],
    cell_moves=list(_schema_1_moves.values()),  # used for detection.
)

_schema_2_moves = {
    "A": (1, 3),
    "B": (2, 3),
    "C": (3, 3),
    "D": (2, 2),
    "E": (3, 2),
    "F": (3, 1),
}
_schema_2_attacking = [(1, 2), (2, 1), (4, 1), (4, 2)]
_schema_2_defending = [(4, 0), (3, 0), (0, 4), (1, 4), (2, 4), (3, 4)]
schema_2 = dict(
    idea=""".bA
            bDB
            FEC
            bb
            """,
    name="pattern2",
    concept="span",
    cells_attacking=_schema_2_attacking,
    cells_defending=_schema_2_defending,
    cells_used=list(_schema_2_moves.values())
    + _schema_2_attacking
    + _schema_2_defending,
    lines=span_lines(_schema_2_moves),
    defender_to_play=True,
    cells_idx_connect=[1, 3],
    cells_idx_connect_defender=[0, 5],
    cell_moves=list(_schema_2_moves.values()),  # used for detection.
)

_schema_3_moves = {
    "A": (3, 0),
    "B": (3, 1),
    "C": (3, 2),
    "D": (2, 1),
    "E": (2, 2),
    "F": (1, 2),
}
_schema_3_attacking = [(1, 1), (2, 0), (1, 3), (2, 3)]
_schema_3_defending = [(0, 3), (0, 2), (4, 1), (4, 2), (4, 0)]
schema_3 = dict(
    idea=""".bFb
            bDEb
            ABC
            """,
    name="pattern3",
    concept="span",
    cells_attacking=_schema_3_attacking,
    cells_defending=_schema_3_defending,
    cells_used=list(_schema_3_moves.values())
    + _schema_3_attacking
    + _schema_3_defending,
    lines=span_lines(_schema_3_moves),
    defender_to_play=True,
    cells_idx_connect=[1, 3],
    cells_idx_connect_defender=[0, 4],
    cell_moves=list(_schema_3_moves.values()),  # used for detection.
)

_schema_4_moves = {
    "A": (1, 1),
    "B": (2, 1),
    "C": (3, 1),
    "D": (1, 2),
    "E": (2, 2),
    "F": (1, 3),
}
_schema_4_attacking = [(0, 2), (0, 3), (2, 3), (3, 2)]
_schema_4_defending = [(0, 4), (1, 4), (1, 0), (2, 0), (3, 0), (4, 0)]
schema_4 = dict(
    idea=""".bb
            ADF
            BEb
            Cb.
            """,
    name="pattern4",
    concept="span",
    cells_attacking=_schema_4_attacking,
    cells_defending=_schema_4_defending,
    cells_used=list(_schema_4_moves.values())
    + _schema_4_attacking
    + _schema_4_defending,
    lines=span_lines(_schema_4_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 2],
    cells_idx_connect_defender=[0, 5],
    cell_moves=list(_schema_4_moves.values()),  # used for detection.
)


def schemas():
    return [schema_1, schema_2, schema_3, schema_4]
