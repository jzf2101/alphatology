Each schema contains the information needed to generate behavioral tests and probing boards.

Most concepts have 3-4 different permutations/orientations. The structure of the "lines", i.e.,
which moves a player should take should HOLD across all of these permutations. Thus, we can use
a small function like:

```
def bridge_lines(moves: Dict[str, cell]):
    L, R = moves["L"], moves["R"]
    return [
        {
            "forcing": [L],
            "expected": [R],
        },
        {
            "forcing": [L],
            "expected": [R],
        },
    ]
```
Where moves is a mapping from names of cells to cells, we can test the agent along certain forced lines.
NOTE: We also consider alternate victories of the same number of moves or less as passing the test.
ALTERNATE: Filter these cases.


Next, the schema looks like this:
```
schema_1_moves = {"L": (0, 1), "R": (1, 0)}
schema_1_attacking = [(0, 0), (1, 1)]
schema_1 = dict(
    idea="""b...
            .b..
            ....
            """,
    name="pattern1",
    concept="bridge",
    cells_attacking=schema_1_attacking,
    cells_defending=[],
    cells_used=schema_1_attacking + list(schema_1_moves.values()),
    lines=bridge_lines(schema_1_moves),
    defender_to_play=True,
)
```

idea: Small minimal board pictograph that is unused in the code but useful for recognizing the pattern.
name: Name of this permutation/orientation.
concept: Concept. Generally shared among all schema in a file. For now, I group them after in a post-hoc manner (as desired).
cells_attacking: The cells that form the concept on the board. Generally, the attacker is the agent tested. For the negative concepts (captured and deadcells), things are a bit different.
cells_defending: Cells that are part of the concept. Some edge templates and captured templates include enemy cells.
cells_used: All the cells used by the concept that are required for the concept to be present.
lines: The forced lines. See the lines function above.
defender_to_play: This is always true so far for positive concepts. In effect: The defender intrudes into the template (forcing moves) and we then test if the attacker responds optimally.

