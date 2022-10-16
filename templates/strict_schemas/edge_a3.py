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
_schema_1_defenders = [(1, 0), (2, 1), (2, 4), (1, 4), (0, 4)]
schema_1 = dict(
    idea="""..bA
            .BCD
            EFGH
            """,
    name="bot",
    concept="edge_a3",
    cells_attacking=[_schema_1_moves["attacker"]],
    cells_defending=_schema_1_defenders,
    cells_used=list(_schema_1_moves.values()) + _schema_1_defenders,
    lines=a3_lines(_schema_1_moves),
    defender_to_play=True,
    edge="BOT",
    cells_idx_connect_defender=[0, 4],
)
schema_1_reverse = dict(
    idea="""..bA
            .BCD
            EFGH
            """,
    name="bot",
    concept="edge_a3_rev",
    cells_attacking=[_schema_1_moves_reverse["attacker"]],
    cells_defending=_schema_1_defenders,
    cells_used=list(_schema_1_moves_reverse.values()) + _schema_1_defenders,
    lines=a3_lines(_schema_1_moves_reverse),
    defender_to_play=True,
    edge="BOT",
    cells_idx_connect_defender=[0, 4],
)

_schema_2_moves = {
    "attacker": (2, 1),
    "A": (2, 2),
    "B": (1, 1),
    "C": (1, 2),
    "D": (1, 3),
    "E": (0, 1),
    "F": (0, 2),
    "G": (0, 3),
    "H": (0, 4),
}
_schema_2_moves_reverse = {
    "attacker": (2, 2),
    "A": (2, 1),
    "B": (1, 1),
    "C": (1, 2),
    "D": (1, 3),
    "E": (0, 1),
    "F": (0, 2),
    "G": (0, 3),
    "H": (0, 4),
}
_schema_2_defenders = [(0, 0), (1, 0), (2, 3), (1, 4)]
schema_2 = dict(
    idea="""EFGH
            BCD
            bA
            """,
    name="top",
    concept="edge_a3",
    cells_attacking=[_schema_2_moves["attacker"]],
    cells_defending=_schema_2_defenders,
    cells_used=list(_schema_2_moves.values()) + _schema_2_defenders,
    lines=a3_lines(_schema_2_moves),
    defender_to_play=True,
    edge="TOP",
    cells_idx_connect_defender=[0, 3],
)
schema_2_reverse = dict(
    idea="""EFGH
            BCD
            bA
            """,
    name="top_rev",
    concept="edge_a3",
    cells_attacking=[_schema_2_moves_reverse["attacker"]],
    cells_defending=_schema_2_defenders,
    cells_used=list(_schema_2_moves_reverse.values()) + _schema_2_defenders,
    lines=a3_lines(_schema_2_moves_reverse),
    defender_to_play=True,
    edge="TOP",
    cells_idx_connect_defender=[0, 3],
)


_schema_3_moves = {
    "attacker": (1, 2),
    "A": (2, 2),
    "B": (1, 1),
    "C": (2, 1),
    "D": (3, 1),
    "E": (1, 0),
    "F": (2, 0),
    "G": (3, 0),
    "H": (4, 0),
}
_schema_3_moves_reverse = {
    "attacker": (2, 2),
    "A": (1, 2),
    "B": (1, 1),
    "C": (2, 1),
    "D": (3, 1),
    "E": (1, 0),
    "F": (2, 0),
    "G": (3, 0),
    "H": (4, 0),
}
_schema_3_defenders = [(0, 0), (0, 1), (4, 1), (3, 2)]
schema_3 = dict(
    idea="""EBw
            FCA
            GD
            H
            """,
    name="left",
    concept="edge_a3",
    cells_attacking=[_schema_3_moves["attacker"]],
    cells_defending=_schema_3_defenders,
    cells_used=list(_schema_3_moves.values()) + _schema_3_defenders,
    lines=a3_lines(_schema_3_moves),
    defender_to_play=True,
    edge="LEFT",
    cells_idx_connect_defender=[0, 3],
)
schema_3_reverse = dict(
    name="left_rev",
    concept="edge_a3",
    cells_attacking=[_schema_3_moves_reverse["attacker"]],
    cells_defending=_schema_3_defenders,
    cells_used=list(_schema_3_moves_reverse.values()) + _schema_3_defenders,
    lines=a3_lines(_schema_3_moves_reverse),
    defender_to_play=True,
    edge="LEFT",
    cells_idx_connect_defender=[0, 3],
)

_schema_4_moves = {
    "attacker": (3, 2),
    "A": (4, 2),
    "B": (2, 1),
    "C": (3, 1),
    "D": (4, 1),
    "E": (1, 0),
    "F": (2, 0),
    "G": (3, 0),
    "H": (4, 0),
}
_schema_4_moves_reverse = {
    "attacker": (4, 2),
    "A": (3, 2),
    "B": (2, 1),
    "C": (3, 1),
    "D": (4, 1),
    "E": (1, 0),
    "F": (2, 0),
    "G": (3, 0),
    "H": (4, 0),
}
_schema_4_defenders = [(1, 1), (2, 2), (5, 1), (5, 2)]
schema_4 = dict(
    idea="""..E
            .BF
            wCG
            ADH
            """,
    name="right",
    concept="edge_a3",
    cells_attacking=[_schema_4_moves["attacker"]],
    cells_defending=_schema_4_defenders,
    cells_used=list(_schema_4_moves.values()) + _schema_4_defenders,
    lines=a3_lines(_schema_4_moves),
    defender_to_play=True,
    edge="RIGHT",
    cells_idx_connect_defender=[0, 3],
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
    cells_defending=_schema_4_defenders,
    cells_used=list(_schema_4_moves_reverse.values()) + _schema_4_defenders,
    lines=a3_lines(_schema_4_moves_reverse),
    defender_to_play=True,
    edge="RIGHT",
    cells_idx_connect_defender=[0, 3],
)


def schemas():
    return [
        schema_1,
        schema_2,
        schema_3,
        schema_4,
        schema_1_reverse,
        schema_2_reverse,
        # schema_3_reverse,
        schema_4_reverse,
    ]
