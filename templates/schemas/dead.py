# https://www.hexwiki.net/index.php/Dead_cell
schema_1 = dict(
    idea="""w.w..
            ww...
            .....
            """,
    name="pattern1-1",
    concept="dead",
    cells_attacking=[(0, 0), (0, 2), (1, 0), (1, 1)],
    cells_defending=[],
    avoid_defending=[(0, 1)],
    avoid_attacking=[(0, 1)],
    cells_used=[(0, 0), (0, 2), (1, 0), (1, 1)] + [(0, 1)],
)
schema_2 = dict(
    idea=""".w..
            w...
            ww..
        """,
    name="pattern1-2",
    concept="dead",
    cells_attacking=[(0, 1), (1, 0), (2, 0), (2, 1)],
    cells_defending=[],
    avoid_defending=[(1, 1)],
    avoid_attacking=[(1, 1)],
    cells_used=[(0, 1), (1, 0), (2, 0), (2, 1)] + [(1, 1)],
)
schema_3 = dict(
    idea="""ww..
            .w..
            w...
            """,
    name="pattern1-3",
    concept="dead",
    cells_attacking=[(0, 0), (0, 1), (1, 1), (2, 0)],
    cells_defending=[],
    avoid_defending=[(1, 0)],
    avoid_attacking=[(1, 0)],
    cells_used=[(0, 0), (0, 1), (1, 1), (2, 0)] + [(1, 0)],
)
schema_4 = dict(
    idea=""".ww..
            w.w..
            .....
            bbbb.
            .....
            """,
    name="pattern1-4",
    concept="dead",
    cells_attacking=[(0, 1), (0, 2), (1, 0), (1, 2)],
    cells_defending=[],
    avoid_defending=[(1, 1)],
    avoid_attacking=[(1, 1)],
    cells_used=[(0, 1), (0, 2), (1, 0), (1, 2)] + [(1, 1)],
)
schema_5 = dict(
    idea=""".ww..
            ..w..
            b....
            """,
    name="pattern2-1",
    concept="dead",
    cells_attacking=[(0, 1), (0, 2), (1, 2)],
    cells_defending=[(2, 0)],
    avoid_defending=[(1, 1)],
    avoid_attacking=[(1, 1)],
    cells_used=[(0, 1), (0, 2), (1, 2)] + [(2, 0)] + [(1, 1)],
)
schema_6 = dict(
    idea=""".ww..
            w....
            .b...
            """,
    name="pattern2-2",
    concept="dead",
    cells_attacking=[(1, 0), (0, 1), (0, 2)],
    cells_defending=[(2, 1)],
    avoid_defending=[(1, 1)],
    avoid_attacking=[(1, 1)],
    cells_used=[(0, 1), (0, 2), (1, 0)] + [(2, 1)] + [(1, 1)],
)
schema_7 = dict(
    idea="""..b..
            w....
            ww...
            """,
    name="pattern2-3",
    concept="dead",
    cells_attacking=[(1, 0), (2, 0), (2, 1)],
    cells_defending=[(0, 2)],
    avoid_defending=[(1, 1)],
    avoid_attacking=[(1, 1)],
    cells_used=[(1, 0), (2, 0), (2, 1)] + [(0, 2)] + [(1, 1)],
)
schema_8 = dict(
    idea=""".b...
            ..w..
            ww...
            """,
    name="pattern2-4",
    concept="dead",
    cells_attacking=[(1, 2), (2, 0), (2, 1)],
    cells_defending=[(0, 1)],
    avoid_defending=[(1, 1)],
    avoid_attacking=[(1, 1)],
    cells_used=[(1, 2), (2, 0), (2, 1)] + [(0, 1)] + [(1, 1)],
)
schema_9 = dict(
    idea=""".bb..
            .....
            ww...
            .....
            .....
            """,
    name="pattern3-1",
    concept="dead",
    cells_attacking=[(2, 0), (2, 1)],
    cells_defending=[(0, 1), (0, 2)],
    avoid_defending=[(1, 1)],
    avoid_attacking=[(1, 1)],
    cells_used=[(2, 0), (2, 1)] + [(0, 1), (0, 2)] + [(1, 1)],
)
schema_10 = dict(
    idea=""".w...
            w.b..
            .b...
            .....
            .....
            """,
    name="pattern3-2",
    concept="dead",
    cells_attacking=[(0, 1), (1, 0)],
    cells_defending=[(1, 2), (2, 1)],
    avoid_defending=[(1, 1)],
    avoid_attacking=[(1, 1)],
    cells_used=[(0, 1), (1, 0)] + [(1, 2), (2, 1)] + [(1, 1)],
)


# WE WILL NUMBER THESE PER DIRECTION
# attacking --> edge's owner
schema_11 = dict(
    # bot, black
    idea="""
        .....
        .b...
        b....
        """,
    name="pattern4-1-edge",
    concept="dead",
    cells_attacking=[(0, 0), (1, 1)],
    cells_defending=[],
    avoid_defending=[(0, 1)],
    avoid_attacking=[(0, 1)],
    cells_used=[(0, 0), (1, 1)] + [(0, 1)],
    edge_template=True,
    edge="BOT",
)
schema_12 = dict(
    # top, black
    idea="""
        b....
        b....
        .....
        """,
    name="pattern4-2-edge",
    concept="dead",
    cells_attacking=[(0, 0), (1, 0)],
    cells_defending=[],
    avoid_defending=[(0, 1)],
    avoid_attacking=[(0, 1)],
    cells_used=[(0, 0), (1, 0)] + [(0, 1)],
    edge_template=True,
    edge="TOP",
)
schema_13 = dict(
    # left, white
    idea="""ww...
            .....
            .....
            """,
    name="pattern4-3-edge",
    concept="dead",
    cells_attacking=[(0, 0), (0, 1)],
    cells_defending=[],
    avoid_defending=[(1, 0)],
    avoid_attacking=[(1, 0)],
    cells_used=[(0, 0), (0, 1)] + [(1, 0)],
    edge_template=True,
    edge="LEFT",
)
schema_14 = dict(
    # right, white
    idea="""....w
            ...w.
            """,
    name="pattern4-4-edge",
    concept="dead",
    cells_attacking=[(0, 0), (1, 1)],
    cells_defending=[],
    avoid_defending=[(1, 0)],
    avoid_attacking=[(1, 0)],
    cells_used=[(0, 0), (1, 1)] + [(1, 0)],
    edge_template=True,
    edge="RIGHT",
)

schema_15 = dict(
    # bot, black
    idea="""
        .....
        .....
        b.b..
        """,
    name="pattern5-1-edge",
    concept="dead",
    cells_attacking=[(0, 0), (0, 2)],
    cells_defending=[],
    avoid_defending=[(0, 1)],
    avoid_attacking=[(0, 1)],
    cells_used=[(0, 0), (0, 2)] + [(0, 1)],
    edge_template=True,
    edge="BOT",
)
schema_16 = dict(
    # top, black
    idea="""
        b.b..
        .....
        .....
        """,
    name="pattern5-2-edge",
    concept="dead",
    cells_attacking=[(0, 0), (0, 2)],
    cells_defending=[],
    avoid_defending=[(0, 1)],
    avoid_attacking=[(0, 1)],
    cells_used=[(0, 0), (0, 2)] + [(0, 1)],
    edge_template=True,
    edge="TOP",
)
schema_17 = dict(
    # left, white
    idea="""w....
            .....
            w....
            """,
    name="pattern5-3-edge",
    concept="dead",
    cells_attacking=[(0, 0), (2, 0)],
    cells_defending=[],
    avoid_defending=[(1, 0)],
    avoid_attacking=[(1, 0)],
    cells_used=[(0, 0), (2, 0)] + [(1, 0)],
    edge_template=True,
    edge="LEFT",
)
schema_18 = dict(
    # right, white
    idea="""....w
            .....
            ....w
            """,
    name="pattern5-4-edge",
    concept="dead",
    cells_attacking=[(0, 0), (2, 0)],
    cells_defending=[],
    avoid_defending=[(1, 0)],
    avoid_attacking=[(1, 0)],
    cells_used=[(0, 0), (2, 0)] + [(1, 0)],
    edge_template=True,
    edge="RIGHT",
)


schema_19 = dict(
    # bot, black
    idea=""".....
            .....
            .....
            ..w..
            b....
            """,
    name="pattern6-1-edge",
    concept="dead",
    cells_attacking=[(0, 0)],
    cells_defending=[(1, 2)],
    avoid_defending=[(0, 1)],
    avoid_attacking=[(0, 1)],
    cells_used=[(0, 0), (1, 2)] + [(0, 1)],
    edge_template=True,
    edge="BOT",
)
schema_20 = dict(
    # top, black
    idea="""b....
            .w...
            .....
            .....
            .....
            """,
    name="pattern6-2-edge",
    concept="dead",
    cells_attacking=[(0, 0)],
    cells_defending=[(1, 1)],
    avoid_defending=[(0, 1)],
    avoid_attacking=[(0, 1)],
    cells_used=[(0, 0), (1, 1)] + [(0, 1)],
    edge_template=True,
    edge="TOP",
)
schema_21 = dict(
    # left, white
    idea="""w....
            .b...
            """,
    name="pattern6-3-edge",
    concept="dead",
    cells_attacking=[(0, 0)],
    cells_defending=[(1, 1)],
    avoid_defending=[(1, 0)],
    avoid_attacking=[(1, 0)],
    cells_used=[(0, 0), (1, 1)] + [(1, 0)],
    edge_template=True,
    edge="LEFT",
)
schema_22 = dict(
    # right, white
    idea="""....w
            .....
            ...b.
            """,
    name="pattern6-4-edge",
    concept="dead",
    cells_attacking=[(0, 0)],
    cells_defending=[(2, 1)],
    avoid_defending=[(1, 0)],
    avoid_attacking=[(1, 0)],
    cells_used=[(0, 0), (2, 1)] + [(1, 0)],
    edge_template=True,
    edge="RIGHT",
)

schema_23 = dict(
    # bot, black
    idea=""".
            .....
            ww...
            .....
            """,
    name="pattern7-1-edge",
    concept="dead",
    cells_attacking=[],
    cells_defending=[(1, 0), (1, 1)],
    avoid_defending=[(0, 0)],
    avoid_attacking=[(0, 0)],
    cells_used=[(1, 0), (1, 1)] + [(0, 0)],
    edge_template=True,
    edge="BOT",
)
schema_24 = dict(
    # top, black
    idea=""".....
            ww...
            """,
    name="pattern7-2-edge",
    concept="dead",
    cells_attacking=[],
    cells_defending=[(1, 0), (1, 1)],
    avoid_defending=[(0, 1)],
    avoid_attacking=[(0, 1)],
    cells_used=[(1, 0), (1, 1)] + [(0, 1)],
    edge_template=True,
    edge="TOP",
)
schema_25 = dict(
    # left, white
    idea=""".b...
            .b...
            """,
    name="pattern7-3-edge",
    concept="dead",
    cells_attacking=[],
    cells_defending=[(0, 1), (1, 1)],
    avoid_defending=[(1, 0)],
    avoid_attacking=[(1, 0)],
    cells_used=[(0, 1), (1, 1)] + [(1, 0)],
    edge_template=True,
    edge="LEFT",
)
schema_26 = dict(
    # right, white
    idea="""...b.
            ...b.
            """,
    name="pattern7-4-edge",
    concept="dead",
    cells_attacking=[],
    cells_defending=[(0, 1)],
    avoid_defending=[(1, 1)],
    avoid_attacking=[(0, 0)],
    cells_used=[(0, 1), (1, 1)] + [(0, 0)],
    edge_template=True,
    edge="RIGHT",
)

# NOTE: We are skipping the corner template for now.
def schemas():
    return [
        schema_1,
        schema_2,
        schema_3,
        schema_4,
        schema_5,
        schema_6,
        schema_7,
        schema_8,
        schema_9,
        schema_10,
        # edge schemas
        schema_11,
        schema_12,
        schema_13,
        schema_14,
        schema_15,
        schema_16,
        schema_17,
        schema_18,
        schema_19,
        schema_20,
        schema_21,
        schema_22,
        schema_23,
        schema_24,
        schema_25,
        schema_26,
    ]
