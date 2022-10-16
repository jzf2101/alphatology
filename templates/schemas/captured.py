# http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.297.3376&rep=rep1&type=pdf
# page 11
schema_1 = dict(
    idea="""w..w
       www.""",
    name="pattern1-1",
    concept="captured",
    cells_attacking=[(0, 0), (0, 3), (1, 0), (1, 1), (1, 2)],
    cells_defending=[],
    avoid_defending=[(0, 1), (0, 2)],
    avoid_attacking=[],
    cells_used=[(0, 0), (0, 3), (1, 0), (1, 1), (1, 2)] + [(0, 1), (0, 2)],
)
schema_2 = dict(
    idea=""".www.
            w..w.""",
    name="pattern1-2",
    concept="captured",
    cells_attacking=[(0, 1), (0, 2), (0, 3), (1, 0), (1, 3)],
    cells_defending=[],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(0, 1), (0, 2), (0, 3), (1, 0), (1, 3)] + [(1, 1), (1, 2)],
)

schema_3 = dict(
    idea="""ww...
            .w...
            .w...
            w..bb""",
    name="pattern1-3",
    concept="captured",
    cells_attacking=[(0, 0), (0, 1), (1, 1), (2, 1), (3, 0)],
    cells_defending=[],
    avoid_defending=[(1, 0), (2, 0)],
    avoid_attacking=[],
    cells_used=[(0, 0), (0, 1), (1, 1), (2, 1), (3, 0)] + [(1, 0), (2, 0)],
)
schema_4 = dict(
    idea=""".w..
            w...
            w...
            wwbb""",
    name="pattern1-4",
    concept="captured",
    cells_attacking=[(0, 1), (1, 0), (2, 0), (3, 0), (3, 1)],
    cells_defending=[],
    avoid_defending=[(1, 1), (2, 1)],
    avoid_attacking=[],
    cells_used=[(0, 1), (1, 0), (2, 0), (3, 0), (3, 1)] + [(1, 1), (2, 1)],
)
schema_5 = dict(
    idea="""..w
            ...
            www""",
    name="pattern2-1",
    concept="captured",
    cells_attacking=[(0, 2), (2, 0), (2, 1), (2, 2)],
    cells_defending=[],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(0, 2), (2, 0), (2, 1), (2, 2)] + [(1, 1), (1, 2)],
)
schema_6 = dict(
    idea="""www
            ...
            w..""",
    name="pattern2-2",
    concept="captured",
    cells_attacking=[(2, 0), (0, 0), (0, 1), (0, 2)],
    cells_defending=[],
    avoid_defending=[(1, 0), (1, 1)],
    avoid_attacking=[],
    cells_used=[(2, 0), (0, 0), (0, 1), (0, 2)] + [(1, 0), (1, 1)],
)
schema_7 = dict(
    idea="""w.w
            w..
            w..""",
    name="pattern2-2",
    concept="captured",
    cells_attacking=[(0, 2), (0, 0), (1, 0), (2, 0)],
    cells_defending=[],
    avoid_defending=[(0, 1), (1, 1)],
    avoid_attacking=[],
    cells_used=[(0, 2), (0, 0), (1, 0), (2, 0)] + [(0, 1), (1, 1)],
)
schema_8 = dict(
    idea="""..w
            ..w
            w.w""",
    name="pattern2-2",
    concept="captured",
    cells_attacking=[(2, 0), (0, 2), (1, 2), (2, 2)],
    cells_defending=[],
    avoid_defending=[(1, 1), (2, 1)],
    avoid_attacking=[],
    cells_used=[(2, 0), (0, 2), (1, 2), (2, 2)] + [(1, 1), (2, 1)],
)
schema_9 = dict(
    idea="""..ww
            ....
            ww..""",
    name="pattern3-1",
    concept="captured",
    cells_attacking=[(0, 2), (0, 3), (2, 0), (2, 1)],
    cells_defending=[],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(0, 2), (0, 3), (2, 0), (2, 1)] + [(1, 1), (1, 2)],
)
schema_10 = dict(
    idea="""ww..
            ....
            ww..""",
    name="pattern3-2",
    concept="captured",
    cells_attacking=[(0, 0), (0, 1), (2, 0), (2, 1)],
    cells_defending=[],
    avoid_defending=[(1, 0), (1, 1)],
    avoid_attacking=[],
    cells_used=[(0, 0), (0, 1), (2, 0), (2, 1)] + [(1, 0), (1, 1)],
)
schema_11 = dict(
    idea="""w.w.
            w.w.
            ....""",
    name="pattern3-3",
    concept="captured",
    cells_attacking=[(0, 0), (0, 2), (1, 0), (1, 2)],
    cells_defending=[],
    avoid_defending=[(0, 1), (1, 1)],
    avoid_attacking=[],
    cells_used=[(0, 0), (0, 2), (1, 0), (1, 2)] + [(0, 1), (1, 1)],
)
schema_12 = dict(
    idea=""".w.w
            w.w.
            ....""",
    name="pattern3-4",
    concept="captured",
    cells_attacking=[(0, 1), (0, 3), (1, 0), (1, 2)],
    cells_defending=[],
    avoid_defending=[(0, 2), (1, 1)],
    avoid_attacking=[],
    cells_used=[(0, 1), (0, 3), (1, 0), (1, 2)] + [(0, 2), (1, 1)],
)
schema_16 = dict(
    idea="""w.w
            w..
            .b.""",
    name="pattern4-4",
    concept="captured",
    cells_attacking=[(0, 0), (0, 2), (1, 0)],
    cells_defending=[(2, 1)],
    avoid_defending=[(0, 1), (1, 1)],
    avoid_attacking=[],
    cells_used=[(0, 0), (0, 2), (1, 0)] + [(2, 1)] + [(0, 1), (1, 1)],
)
schema_15 = dict(
    idea=""".b..
            ..w.
            w...
            w...""",
    name="pattern4-3",
    concept="captured",
    cells_attacking=[(1, 2), (2, 0), (3, 0)],
    cells_defending=[(0, 1)],
    avoid_defending=[(1, 1), (2, 1)],
    avoid_attacking=[],
    cells_used=[(1, 2), (2, 0), (3, 0)] + [(0, 1)] + [(1, 1), (2, 1)],
)
schema_14 = dict(
    idea="""..w
            b..
            .ww""",
    name="pattern4-2",
    concept="captured",
    cells_attacking=[(0, 3), (2, 1), (2, 2)],
    cells_defending=[(1, 0)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(0, 3), (2, 1), (2, 2)] + [(1, 0)] + [(1, 1), (1, 2)],
)
schema_13 = dict(
    idea="""..w..
            ...b.
            ww...""",
    name="pattern4-1",
    concept="captured",
    cells_attacking=[(0, 2), (2, 0), (2, 1)],
    cells_defending=[(1, 3)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(0, 2), (2, 0), (2, 1)] + [(1, 3)] + [(1, 1), (1, 2)],
)


schema_17 = dict(
    idea="""..w.
            b..b
            .w..""",
    name="pattern5-1",
    concept="captured",
    cells_attacking=[(0, 2), (2, 1)],
    cells_defending=[(1, 0), (1, 3)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(0, 2), (2, 1)] + [(1, 0), (1, 3)] + [(1, 1), (1, 2)],
)
schema_18 = dict(
    idea="""b..
            ..w
            w..
            .b.""",
    name="pattern5-2",
    concept="captured",
    cells_attacking=[(1, 2), (2, 0)],
    cells_defending=[(0, 0), (3, 1)],
    avoid_defending=[(1, 1), (2, 1)],
    avoid_attacking=[],
    cells_used=[(1, 2), (2, 0)] + [(0, 0), (3, 1)] + [(1, 1), (2, 1)],
)
schema_19 = dict(
    idea="""...b
            .w..
            ..w.
            b...""",
    name="pattern5-3",
    concept="captured",
    cells_attacking=[(1, 1), (2, 2)],
    cells_defending=[(0, 3), (3, 0)],
    avoid_defending=[(1, 2), (2, 1)],
    avoid_attacking=[],
    cells_used=[(1, 1), (2, 2)] + [(0, 3), (3, 0)] + [(1, 2), (2, 1)],
)

schema_20 = dict(
    idea=""".w..b
            w...b
            w.b.b
            w....
            .....
            """,
    name="pattern6-1",
    concept="captured",
    cells_attacking=[(0, 1), (1, 0), (2, 0), (3, 0)],
    cells_defending=[(2, 2)],
    avoid_defending=[(1, 1), (2, 1)],
    avoid_attacking=[],
    cells_used=[(0, 1), (1, 0), (2, 0), (3, 0)] + [(2, 2)] + [(1, 1), (2, 1)],
)
schema_21 = dict(
    idea="""..b.b
            w...b
            w...b
            ww...
            .....
            """,
    name="pattern6-2",
    concept="captured",
    cells_attacking=[(1, 0), (2, 0), (3, 0), (3, 1)],
    cells_defending=[(0, 2)],
    avoid_defending=[(1, 1), (2, 1)],
    avoid_attacking=[],
    cells_used=[(1, 0), (2, 0), (3, 0), (3, 1)] + [(0, 2)] + [(1, 1), (2, 1)],
)
schema_22 = dict(
    idea="""..w
            b.w
            ..w
            .w.
            """,
    name="pattern6-3",
    concept="captured",
    cells_attacking=[(0, 2), (1, 2), (2, 2), (3, 1)],
    cells_defending=[(1, 0)],
    avoid_defending=[(1, 1), (2, 1)],
    avoid_attacking=[],
    cells_used=[(0, 2), (1, 2), (2, 2), (3, 1)] + [(1, 0)] + [(1, 1), (2, 1)],
)
schema_23 = dict(
    idea=""".b...
            ...w.
            www..
            """,
    name="pattern6-4",
    concept="captured",
    cells_attacking=[(2, 0), (2, 1), (2, 2), (1, 3)],
    cells_defending=[(0, 1)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(2, 0), (2, 1), (2, 2), (1, 3)] + [(0, 1)] + [(1, 1), (1, 2)],
)
schema_24 = dict(
    idea="""...b.
            w....
            www..
            .....
            bbbb.
            """,
    name="pattern6-5",
    concept="captured",
    cells_attacking=[(1, 0), (2, 0), (2, 1), (2, 2)],
    cells_defending=[(0, 3)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(1, 0), (2, 0), (2, 1), (2, 2)] + [(0, 3)] + [(1, 1), (1, 2)],
)

schema_25 = dict(
    idea=""".b.b.
            .....
            www..
            .....
            ....b
            """,
    name="pattern7-1",
    concept="captured",
    cells_attacking=[(2, 1), (2, 2), (2, 0)],
    cells_defending=[(0, 1), (0, 3)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(2, 1), (2, 2), (2, 0)] + [(0, 1), (0, 3)] + [(1, 1), (1, 2)],
)
schema_26 = dict(
    idea=""".www.
            .....
            b.b..
            .....
            ....b
            """,
    name="pattern7-2",
    concept="captured",
    cells_attacking=[(0, 1), (0, 2), (0, 3)],
    cells_defending=[(2, 0), (2, 2)],
    avoid_defending=[(1, 2), (1, 1)],
    avoid_attacking=[],
    cells_used=[(0, 1), (0, 2), (0, 3)] + [(2, 0), (2, 2)] + [(1, 2), (1, 1)],
)
schema_27 = dict(
    idea="""..b..
            ...w.
            b.w..
            .w...
            ....b
            """,
    name="pattern7-3",
    concept="captured",
    cells_attacking=[(1, 3), (2, 2), (3, 1)],
    cells_defending=[(0, 2), (2, 0)],
    avoid_defending=[(1, 2), (2, 1)],
    avoid_attacking=[],
    cells_used=[(1, 3), (2, 2), (3, 1)] + [(0, 2), (2, 0)] + [(1, 2), (2, 1)],
)
schema_28 = dict(
    idea="""..w..
            .w.b.
            w....
            .b...
            """,
    name="pattern7-4",
    concept="captured",
    cells_attacking=[(0, 2), (1, 1), (2, 0)],
    cells_defending=[(1, 3), (3, 1)],
    avoid_defending=[(1, 2), (2, 1)],
    avoid_attacking=[],
    cells_used=[(0, 2), (1, 1), (2, 0)] + [(1, 3), (3, 1)] + [(1, 2), (2, 1)],
)


schema_29 = dict(
    idea=""".w..
            w...
            w.b..
            .b...
            .....
            """,
    name="pattern8-1",
    concept="captured",
    cells_attacking=[(0, 1), (1, 0), (2, 0)],
    cells_defending=[(2, 2), (3, 1)],
    avoid_defending=[(1, 1), (2, 1)],
    avoid_attacking=[],
    cells_used=[
        (0, 1),
        (1, 0),
        (2, 0),
    ]
    + [(2, 2), (3, 1)]
    + [(1, 1), (2, 1)],
)
schema_30 = dict(
    idea=""".bb.b
            ....b
            w....
            ww...
            .....
            """,
    name="pattern8-2",
    concept="captured",
    cells_attacking=[(2, 0), (3, 0), (3, 1)],
    cells_defending=[(0, 1), (0, 2)],
    avoid_defending=[(1, 1), (2, 1)],
    avoid_attacking=[],
    cells_used=[(2, 0), (3, 0), (3, 1)] + [(0, 1), (0, 2)] + [(1, 1), (2, 1)],
)
schema_31 = dict(
    idea=""".b...
            b.w.b
            ..w.b
            .w...
            .....
            """,
    name="pattern8-3",
    concept="captured",
    cells_attacking=[(1, 2), (2, 2), (3, 2)],
    cells_defending=[(1, 0), (0, 1)],
    avoid_defending=[(1, 1), (2, 1)],
    avoid_attacking=[],
    cells_used=[(1, 2), (2, 2), (3, 2)] + [(1, 0), (0, 1)] + [(1, 1), (2, 1)],
)
schema_32 = dict(
    idea=""".b...
            b..w.
            .ww..
            .....
            bbbb.
            """,
    name="pattern8-4",
    concept="captured",
    cells_attacking=[(2, 1), (2, 2), (1, 3)],
    cells_defending=[(0, 1), (1, 0)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(2, 1), (2, 2), (1, 3)] + [(0, 1), (1, 0)] + [(1, 1), (1, 2)],
)
schema_33 = dict(
    idea="""...b.
            w..b.
            ww...
            .....
            b....
            """,
    name="pattern8-5",
    concept="captured",
    cells_attacking=[(1, 0), (2, 0), (2, 1)],
    cells_defending=[(0, 3), (1, 3)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(1, 0), (2, 0), (2, 1)] + [(0, 3), (1, 3)] + [(1, 1), (1, 2)],
)

schema_34 = dict(
    idea=""".b.b.
            ...b.
            ww...
            .....
            .....
          """,
    name="pattern9-1-a",
    concept="captured",
    cells_attacking=[(2, 1), (2, 2)],
    cells_defending=[(0, 1), (0, 3), (1, 3)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(2, 1), (2, 2)] + [(0, 1), (0, 3), (1, 3)] + [(1, 1), (1, 2)],
)
schema_35 = dict(
    idea=""".b.b.
            b....
            .ww..
            .....
            .....
          """,
    name="pattern9-1-b",
    concept="captured",
    cells_attacking=[(2, 1), (2, 2)],
    cells_defending=[(0, 1), (0, 3), (1, 0)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(2, 1), (2, 2)] + [(0, 1), (0, 3), (1, 0)] + [(1, 1), (1, 2)],
)


schema_36 = dict(
    idea="""..ww.
            b....
            b.b..
            .....
            .....
            """,
    name="pattern9-2-a",
    concept="captured",
    cells_attacking=[(0, 2), (0, 3)],
    cells_defending=[(1, 0), (2, 0), (2, 2)],
    avoid_defending=[(1, 2), (1, 1)],
    avoid_attacking=[],
    cells_used=[(0, 2), (0, 3)] + [(1, 0), (2, 0), (2, 2)] + [(1, 2), (1, 1)],
)
schema_37 = dict(
    idea=""".ww..
            ...b.
            b.b..
            .....
            .....
            """,
    name="pattern9-2-b",
    concept="captured",
    cells_attacking=[(0, 1), (0, 2), (0, 3)],
    cells_defending=[(2, 0), (2, 2), (1, 3)],
    avoid_defending=[(1, 1), (1, 2)],
    avoid_attacking=[],
    cells_used=[(0, 1), (0, 2), (0, 3)] + [(2, 0), (2, 2), (1, 3)] + [(1, 1), (1, 2)],
)

schema_38 = dict(
    idea="""..bb.
            .....
            b.w..
            .w...
            .....
            """,
    name="pattern9-3-a",
    concept="captured",
    cells_attacking=[(2, 2), (3, 1)],
    cells_defending=[(0, 2), (2, 0), (0, 3)],
    avoid_defending=[(1, 2), (2, 1)],
    avoid_attacking=[],
    cells_used=[(2, 2), (3, 1)] + [(0, 2), (2, 0), (0, 3)] + [(1, 2), (2, 1)],
)
schema_39 = dict(
    idea="""..b..
            ...w.
            b.w..
            b....
            .....
            """,
    name="pattern9-3-b",
    concept="captured",
    cells_attacking=[(1, 3), (2, 2)],
    cells_defending=[(0, 2), (2, 0), (3, 0)],
    avoid_defending=[(1, 2), (2, 1)],
    avoid_attacking=[],
    cells_used=[(1, 3), (2, 2)] + [(0, 2), (2, 0), (3, 0)] + [(1, 2), (2, 1)],
)

schema_40 = dict(
    idea="""...b.
            .w.b.
            w....
            .b...
            .....
            """,
    name="pattern9-4-a",
    concept="captured",
    cells_attacking=[(1, 1), (2, 0)],
    cells_defending=[(1, 3), (3, 1), (0, 3)],
    avoid_defending=[(1, 2), (2, 1)],
    avoid_attacking=[],
    cells_used=[(1, 1), (2, 0)] + [(1, 3), (3, 1), (0, 3)] + [(1, 2), (2, 1)],
)
schema_41 = dict(
    idea="""..w..
            .w.b.
            .....
            bb...
            .....
            """,
    name="pattern9-4-b",
    concept="captured",
    cells_attacking=[(0, 2), (1, 1)],
    cells_defending=[(1, 3), (3, 1), (3, 0)],
    avoid_defending=[(1, 2), (2, 1)],
    avoid_attacking=[],
    cells_used=[(0, 2), (1, 1)] + [(1, 3), (3, 1), (3, 0)] + [(1, 2), (2, 1)],
)


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
        schema_27,
        schema_28,
        schema_29,
        schema_30,
        schema_31,
        schema_32,
        schema_33,
        schema_34,
        schema_35,
        schema_36,
        schema_37,
        schema_38,
        schema_39,
        schema_40,
        schema_41,
    ]
