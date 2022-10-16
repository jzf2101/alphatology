def bridge_lines(moves):
    L, R = moves["L"], moves["R"]
    return [
        {
            "forcing": [L],
            "expected": [R],
        },
        {
            "forcing": [R],
            "expected": [L],
        },
    ]


schema_1_moves = {"L": (0, 2), "R": (1, 1)}
schema_1_attacking = [(0, 1), (1, 2)]
schema_1_defending = [(1, 0), (0, 3)]
schema_1 = dict(
    idea=""".b.w
            w.b.
            """,
    name="pattern1",
    concept="bridge",
    cells_attacking=schema_1_attacking,
    cells_defending=schema_1_defending,
    cells_used=schema_1_attacking + schema_1_defending + list(schema_1_moves.values()),
    lines=bridge_lines(schema_1_moves),
    cell_moves=list(schema_1_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect=[0, 1],
    cells_idx_connect_defender=[0, 1],
)

schema_2_moves = {"L": (1, 0), "R": (1, 1)}
schema_2_attacking = [(0, 1), (2, 0)]
schema_2_defending = [(0, 0), (2, 1)]
schema_2 = dict(
    idea="""wb
            ..
            bw
            """,
    name="pattern2",
    concept="bridge",
    cells_attacking=schema_2_attacking,
    cells_defending=schema_2_defending,
    cells_used=schema_2_attacking + schema_2_defending + list(schema_2_moves.values()),
    lines=bridge_lines(schema_2_moves),
    cell_moves=list(schema_2_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect_defender=[0, 1],
)
schema_3_moves = {"L": (0, 1), "R": (1, 1)}
schema_3_attacking = [(0, 2), (1, 0)]
schema_3_defending = [(0, 0), (1, 2)]
schema_3 = dict(
    idea="""w.b
            b.w
            """,
    name="pattern3",
    concept="bridge",
    cells_attacking=schema_3_attacking,
    cells_defending=schema_3_defending,
    cells_used=schema_3_attacking + schema_3_defending + list(schema_3_moves.values()),
    lines=bridge_lines(schema_3_moves),
    cell_moves=list(schema_3_moves.values()),  # used for detection.
    defender_to_play=True,
    cells_idx_connect_defender=[0, 1],
)


def schemas():
    return [schema_1, schema_2, schema_3]
