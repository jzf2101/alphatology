schema_1 = dict(
    idea="""....
            b..
            ....
            """,
    name="pattern1",
    concept="edge_a2",
    cells_attacking=[(1, 0)],
    cells_defending=[],
    cells_used=[(0, 0), (0, 1), (1, 0)],
    lines=[
        {"forcing": [(0, 0)], "expected": [(0, 1)]},
        {"forcing": [(0, 1)], "expected": [(0, 0)]},
    ],
    defender_to_play=True,
    edge="TOP",
)

schema_2 = dict(
    idea="""....
            ....
            .b..
            ....
            """,
    name="pattern2",
    concept="edge_a2",
    cells_attacking=[(1, 1)],
    cells_defending=[],
    cells_used=[(0, 0), (0, 1), (1, 1)],
    lines=[
        {"forcing": [(0, 0)], "expected": [(0, 1)]},
        {"forcing": [(0, 1)], "expected": [(0, 0)]},
    ],
    defender_to_play=True,
    edge="BOT",
)

schema_3 = dict(
    idea=""".b..
            ....
            """,
    name="pattern3",
    concept="edge_a2",
    cells_attacking=[(0, 1)],
    cells_defending=[],
    cells_used=[(0, 0), (0, 1), (1, 0)],
    lines=[
        {"forcing": [(0, 0)], "expected": [(1, 0)]},
        {"forcing": [(1, 0)], "expected": [(0, 0)]},
    ],
    defender_to_play=True,
    edge="LEFT",
)

schema_4 = dict(
    idea="""....
            ..b.
            """,
    name="pattern4",
    concept="edge_a2",
    cells_attacking=[(1, 1)],
    cells_defending=[],
    cells_used=[(0, 0), (1, 0), (1, 1)],
    lines=[
        {"forcing": [(0, 0)], "expected": [(1, 0)]},
        {"forcing": [(1, 0)], "expected": [(0, 0)]},
    ],
    defender_to_play=True,
    edge="RIGHT",
)


def schemas():
    return [schema_1, schema_2, schema_3, schema_4]
