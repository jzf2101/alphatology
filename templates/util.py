import random
from boardlaw_utils import other_player, swap_colors
import templates.templates


def get_defender_to_play(defender_to_play: bool, owner_to_play: bool) -> bool:
    assert defender_to_play
    return not owner_to_play


def fill_board(board, sample, attacker_c, defender_c):
    for x, y in sample["cells_attacking"]:
        board[x][y] = attacker_c
    for x, y in sample["cells_defending"]:
        board[x][y] = defender_c
    return board

    # else:
    #     # The key cells to the board randomly mapped.
    #     selectivity_cell_used = set()
    #     for x, y in sample["orig_cells_attacking"]:
    #         sx, sy = selectivity_mask[(x, y)]
    #         board[sx][sy] = attacker_c
    #         selectivity_cell_used.add((sx, sy))

    #     for x, y in sample["orig_cells_defending"]:
    #         sx, sy = selectivity_mask[(x, y)]
    #         board[sx][sy] = defender_c
    #         selectivity_cell_used.add((sx, sy))

    #     # Keep the rest as is (as best as we can) (random cells
    #     # or the connection cells, as with the negative examples.)
    #     for x, y in sample["cells_attacking"]:
    #         if (x, y) in sample["orig_cells_attacking"]:
    #             continue
    #         while (x, y) in selectivity_cell_used:
    #             x, y = get_rand_unused_move_on_board(board)
    #         board[x][y] = attacker_c

    #     for x, y in sample["cells_defending"]:
    #         if (x, y) in sample["orig_cells_defending"]:
    #             continue
    #         while (x, y) in selectivity_cell_used:
    #             x, y = get_rand_unused_move_on_board(board)
    #         board[x][y] = defender_c


def map_board_given_moves(board, sample, attacker_c, defender_c, selectivity_mask):
    for x, y in sample["cells_attacking"]:
        sx, sy = selectivity_mask[(x, y)]
        board[sx][sy] = attacker_c

    for x, y in sample["cells_defending"]:
        sx, sy = selectivity_mask[(x, y)]
        board[sx][sy] = defender_c
    return board


def map_board_given_board(original_board, selectivity_mask):
    mapped_board = templates.templates.get_base_board()
    for i in range(len(original_board)):
        for j in range(len(original_board)):
            sx, sy = selectivity_mask[(i, j)]
            mapped_board[sx][sy] = original_board[i][j]
    return mapped_board


def get_rand_move():
    # randint is inclusive.
    return random.randint(0, 8), random.randint(0, 8)


def get_rand_unused_move_on_board(board):
    # randint is inclusive.
    m = get_rand_move()
    while board[m[0]][m[1]] != ".":
        m = get_rand_move()
    return m


def shuffled(x):
    x = list(x)
    random.shuffle(x)
    return x


def check_board(t: str) -> str:
    from collections import Counter

    c = Counter(t)
    bs = c["b"]
    ws = c["w"]
    assert bs - ws in {0, 1}, len(bs) - len(ws)


def transpose_board(t: str) -> str:
    t = t.replace(" ", "")
    t = t.replace("w", "z")
    t = t.replace("b", "w")
    t = t.replace("z", "b")

    orig_mtx = [list(row) for row in t.split("\n") if len(row) > 0]
    new_mtx = [list(row) for row in t.split("\n") if len(row) > 0]
    assert len(orig_mtx) == len(orig_mtx[0])

    for i in range(len(orig_mtx)):
        for j in range(len(orig_mtx)):
            if orig_mtx[j][i] not in {".", "b", "w"}:
                assert False, (orig_mtx[j][i], "here")
            new_mtx[i][j] = orig_mtx[j][i]
    out = "\n".join(["".join(row) for row in new_mtx])
    return out


def transpose_template(template):
    t = transpose_board(template["template"])
    for opt in ["white_avoid", "black_avoid", "white_skip", "black_skip"]:
        template[opt] = []

    return dict(
        white_skip=template["white_avoid"],
        black_skip=template["black_avoid"],
        white_avoid=template["white_skip"],
        black_avoid=template["black_skip"],
        name=template["name"] + "_transpose",
        concept=template["concept"],
        template=t,
        forcing_player=other_player(template["forcing_player"]),
    )


def transpose_template_positive(template):
    new_template = transpose_template(template)
    t = new_template["template"].replace(" ", "")
    # assert template["forcing_player"] == 0
    # assert new_template["forcing_player"] == 1
    # if template["forcing_player"] == 0:
    # black was to move; so, there were equal number of
    # pieces on the board.
    # now, to make it so white is to move, we have to add
    # an extra black piece.

    # We check that no templates (originals or transposed)
    # are messed up by this addition.
    assert t[0] == "."
    t = "b" + t[1:]

    positive = []
    for test in template["positive"]:
        new_test = {}
        new_test["forcing_actions"] = [
            swap_colors(a, template["forcing_player"]) for a in test["forcing_actions"]
        ]
        new_test["expected_actions"] = [
            swap_colors(a, new_template["forcing_player"])
            for a in test["expected_actions"]
        ]
        positive.append(new_test)

    new_template["positive"] = positive
    new_template["template"] = t
    return new_template
