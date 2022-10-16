def a3_lines(moves):
    """
    *A
    BCD
    EFGH
    """
    return [
        # F
        {
            "forcing": [moves["F"], moves["C"], moves["G"]],
            "expected": [moves["D"], moves["A"], moves["H"]],
        },
        {
            "forcing": [moves["F"], moves["A"], moves["G"]],
            "expected": [moves["D"], moves["C"], moves["H"]],
        },
        {
            "forcing": [moves["F"], moves["C"], moves["H"]],
            "expected": [moves["D"], moves["A"], moves["G"]],
        },
        {
            "forcing": [moves["F"], moves["G"], moves["C"]],
            "expected": [moves["D"], moves["H"], moves["A"]],
        },
        {
            "forcing": [moves["F"], moves["G"], moves["A"]],
            "expected": [moves["D"], moves["H"], moves["C"]],
        },
        {
            "forcing": [moves["F"], moves["H"], moves["C"]],
            "expected": [moves["D"], moves["G"], moves["A"]],
        },
        # D
        # {"forcing": [moves["G"], moves["E"]], "expected": [moves["B"], moves["F"]]},
        # {"forcing": [moves["G"], moves["F"]], "expected": [moves["B"], moves["E"]]},
    ]


_schema_1_moves = {
    "attacker": (2, 2),
    "A": (2, 3),
    "B": (1, 1),
    "C": (1, 2),
    "D": (1, 3),
    "E": (0, 0),
    "F": (0, 1),
    "G": (0, 2),
    "H": (0, 3),
}
_schema_1_moves_reverse = {
    "attacker": (2, 3),
    "A": (2, 2),
    "D": (1, 1),
    "C": (1, 2),
    "B": (1, 3),
    "H": (0, 0),
    "G": (0, 1),
    "F": (0, 2),
    "E": (0, 3),
}
schema_1 = dict(
    idea="""..bA
            .BCD
            EFGH
            """,
    name="bot",
    concept="edge_a3",
    cells_attacking=[_schema_1_moves["attacker"]],
    cells_defending=[],
    cells_used=list(_schema_1_moves.values()),
    lines=a3_lines(_schema_1_moves),
    defender_to_play=True,
    edge="BOT",
)
schema_1_reverse = dict(
    idea="""..bA
            .BCD
            EFGH
            """,
    name="bot",
    concept="edge_a3_rev",
    cells_attacking=[_schema_1_moves_reverse["attacker"]],
    cells_defending=[],
    cells_used=list(_schema_1_moves_reverse.values()),
    lines=a3_lines(_schema_1_moves_reverse),
    defender_to_play=True,
    edge="BOT",
)

_schema_2_moves = {
    "attacker": (2, 0),
    "A": (2, 1),
    "B": (1, 0),
    "C": (1, 1),
    "D": (1, 2),
    "E": (0, 0),
    "F": (0, 1),
    "G": (0, 2),
    "H": (0, 3),
}
_schema_2_moves_reverse = {
    "attacker": (2, 1),
    "A": (2, 0),
    "D": (1, 0),
    "C": (1, 1),
    "B": (1, 2),
    "H": (0, 0),
    "G": (0, 1),
    "F": (0, 2),
    "E": (0, 3),
}
schema_2 = dict(
    idea="""EFGH
            BCD
            bA
            """,
    name="top",
    concept="edge_a3",
    cells_attacking=[_schema_2_moves["attacker"]],
    cells_defending=[],
    cells_used=list(_schema_2_moves.values()),
    lines=a3_lines(_schema_2_moves),
    defender_to_play=True,
    edge="TOP",
)
schema_2_reverse = dict(
    idea="""EFGH
            BCD
            bA
            """,
    name="top_rev",
    concept="edge_a3",
    cells_attacking=[_schema_2_moves_reverse["attacker"]],
    cells_defending=[],
    cells_used=list(_schema_2_moves_reverse.values()),
    lines=a3_lines(_schema_2_moves_reverse),
    defender_to_play=True,
    edge="TOP",
)


_schema_3_moves = {
    "attacker": (0, 2),
    "A": (1, 2),
    "B": (0, 1),
    "C": (1, 1),
    "D": (2, 1),
    "E": (0, 0),
    "F": (1, 0),
    "G": (2, 0),
    "H": (3, 0),
}
_schema_3_moves_reverse = {
    "attacker": (1, 2),
    "A": (0, 2),
    "D": (0, 1),
    "C": (1, 1),
    "B": (2, 1),
    "H": (0, 0),
    "G": (1, 0),
    "F": (2, 0),
    "E": (3, 0),
}
schema_3 = dict(
    idea="""EBw
            FCA
            GD
            H
            """,
    name="left",
    concept="edge_a3",
    cells_attacking=[_schema_3_moves["attacker"]],
    cells_defending=[],
    cells_used=list(_schema_3_moves.values()),
    lines=a3_lines(_schema_3_moves),
    defender_to_play=True,
    edge="LEFT",
)
schema_3_reverse = dict(
    name="left_rev",
    concept="edge_a3",
    cells_attacking=[_schema_3_moves_reverse["attacker"]],
    cells_defending=[],
    cells_used=list(_schema_3_moves_reverse.values()),
    lines=a3_lines(_schema_3_moves_reverse),
    defender_to_play=True,
    edge="LEFT",
)

_schema_4_moves = {
    "attacker": (2, 2),
    "A": (3, 2),
    "B": (1, 1),
    "C": (2, 1),
    "D": (3, 1),
    "E": (0, 0),
    "F": (1, 0),
    "G": (2, 0),
    "H": (3, 0),
}
_schema_4_moves_reverse = {
    "attacker": (3, 2),
    "A": (2, 2),
    "D": (1, 1),
    "C": (2, 1),
    "B": (3, 1),
    "H": (0, 0),
    "G": (1, 0),
    "F": (2, 0),
    "E": (3, 0),
}
schema_4 = dict(
    idea="""..E
            .BF
            wCG
            ADH
            """,
    name="right",
    concept="edge_a3",
    cells_attacking=[_schema_4_moves["attacker"]],
    cells_defending=[],
    cells_used=list(_schema_4_moves.values()),
    lines=a3_lines(_schema_4_moves),
    defender_to_play=True,
    edge="RIGHT",
)
schema_4_reverse = dict(
    idea="""..E
            .BF
            wCG
            ADH
            """,
    name="right_rev",
    concept="edge_a3",
    cells_attacking=[_schema_4_moves_reverse["attacker"]],
    cells_defending=[],
    cells_used=list(_schema_4_moves_reverse.values()),
    lines=a3_lines(_schema_4_moves_reverse),
    defender_to_play=True,
    edge="RIGHT",
)


def schemas():
    return [
        schema_1,
        schema_2,
        schema_3,
        schema_4,
        schema_1_reverse,
        schema_2_reverse,
        schema_3_reverse,
        schema_4_reverse,
    ]
