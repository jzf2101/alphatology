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
    "A": (0, 1),
    "B": (0, 2),
    "C": (0, 3),
    "D": (1, 1),
    "E": (1, 2),
    "F": (2, 1),
}
_schema_1_attacking = [(1, 0), (2, 0), (1, 3), (2, 2)]
schema_1 = dict(
    idea=""".ABC.
            bDEb
            bFb.
            **
            """,
    name="pattern1",
    concept="span",
    cells_attacking=_schema_1_attacking,
    cells_defending=[],
    cells_used=list(_schema_1_moves.values()) + _schema_1_attacking + [(3, 0), (3, 1)],
    lines=span_lines(_schema_1_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 3],
    cell_moves=list(_schema_1_moves.values()),  # used for detection.
)

_schema_2_moves = {
    "A": (0, 2),
    "B": (1, 2),
    "C": (2, 2),
    "D": (1, 1),
    "E": (2, 1),
    "F": (2, 0),
}
_schema_2_attacking = [(0, 1), (1, 0), (3, 0), (3, 1)]
schema_2 = dict(
    idea=""".bA
            bDB
            FEC
            bb
            """,
    name="pattern2",
    concept="span",
    cells_attacking=_schema_2_attacking,
    cells_defending=[],
    cells_used=list(_schema_2_moves.values())
    + _schema_2_attacking
    + [(2, -1), (3, -1)],
    lines=span_lines(_schema_2_moves),
    defender_to_play=True,
    cells_idx_connect=[1, 3],
    cell_moves=list(_schema_2_moves.values()),  # used for detection.
)

_schema_3_moves = {
    "A": (2, 0),
    "B": (2, 1),
    "C": (2, 2),
    "D": (1, 1),
    "E": (1, 2),
    "F": (0, 2),
}
_schema_3_attacking = [(0, 1), (1, 0), (0, 3), (1, 3)]
schema_3 = dict(
    idea=""".bFb
            bDEb
            ABC
            """,
    name="pattern3",
    concept="span",
    cells_attacking=_schema_3_attacking,
    cells_defending=[],
    cells_used=list(_schema_3_moves.values())
    + _schema_3_attacking
    + [(2, -1), (3, -1)],
    lines=span_lines(_schema_3_moves),
    defender_to_play=True,
    cells_idx_connect=[1, 3],
    cell_moves=list(_schema_3_moves.values()),  # used for detection.
)

_schema_4_moves = {
    "A": (1, 0),
    "B": (2, 0),
    "C": (3, 0),
    "D": (1, 1),
    "E": (2, 1),
    "F": (1, 2),
}
_schema_4_attacking = [(0, 1), (0, 2), (2, 2), (3, 1)]
schema_4 = dict(
    idea=""".bb
            ADF
            BEb
            Cb.
            """,
    name="pattern4",
    concept="span",
    cells_attacking=_schema_4_attacking,
    cells_defending=[],
    cells_used=list(_schema_4_moves.values()) + _schema_4_attacking + [(0, 3), (1, 3)],
    lines=span_lines(_schema_4_moves),
    defender_to_play=True,
    cells_idx_connect=[0, 2],
    cell_moves=list(_schema_4_moves.values()),  # used for detection.
)


def schemas():
    return [schema_1, schema_2, schema_3, schema_4]
