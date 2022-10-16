schema_1_defending = [(1, 0), (1, 2)]
schema_1 = dict(
    idea="""....
            wbw.
            ....
            """,
    name="pattern1",
    concept="edge_a2",
    cells_attacking=[(1, 1)],
    cells_defending=schema_1_defending,
    cells_used=[(0, 1), (0, 2), (1, 1)] + schema_1_defending,
    lines=[
        {"forcing": [(0, 1)], "expected": [(0, 2)]},
        {"forcing": [(0, 2)], "expected": [(0, 1)]},
    ],
    defender_to_play=True,
    edge="TOP",
    cells_idx_connect_defender=[0, 1],
)

schema_2_defending = [(1, 0), (1, 2)]
schema_2 = dict(
    idea="""....
            ....
            wbw.
            ....
            """,
    name="pattern2",
    concept="edge_a2",
    cells_attacking=[(1, 1)],
    cells_defending=schema_2_defending,
    cells_used=[(0, 0), (0, 1), (1, 1)] + schema_2_defending,
    lines=[
        {"forcing": [(0, 0)], "expected": [(0, 1)]},
        {"forcing": [(0, 1)], "expected": [(0, 0)]},
    ],
    defender_to_play=True,
    edge="BOT",
    cells_idx_connect_defender=[0, 1],
)

schema_3_defending = [(0, 1), (2, 1)]
schema_3 = dict(
    idea=""".w
            .b..
            .w..
            """,
    name="pattern3",
    concept="edge_a2",
    cells_attacking=[(1, 1)],
    cells_defending=schema_3_defending,
    cells_used=[(1, 0), (1, 1), (2, 0)] + schema_3_defending,
    lines=[
        {"forcing": [(1, 0)], "expected": [(2, 0)]},
        {"forcing": [(2, 0)], "expected": [(1, 0)]},
    ],
    defender_to_play=True,
    edge="LEFT",
    cells_idx_connect_defender=[0, 1],
)

schema_4_defending = [(0, 1), (2, 1)]
schema_4 = dict(
    idea="""..w.
            ..b.
            ..w.
            """,
    name="pattern4",
    concept="edge_a2",
    cells_attacking=[(1, 1)],
    cells_defending=schema_4_defending,
    cells_used=[(0, 0), (1, 0), (1, 1)],
    lines=[
        {"forcing": [(0, 0)], "expected": [(1, 0)]},
        {"forcing": [(1, 0)], "expected": [(0, 0)]},
    ],
    defender_to_play=True,
    edge="RIGHT",
    cells_idx_connect_defender=[0, 1],
)


def schemas():
    return [schema_1, schema_2, schema_3, schema_4]
