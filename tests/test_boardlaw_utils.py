import torch as th
from boardlaw_utils import from_sgf, action_to_cell, cell_to_action


def test_from_sgf_1():
    sgf = "(;AP[HexGui:1.0.]FF[4]GM[11]SZ[3];AB[a1]AW[a2]PL[B])"
    actual = from_sgf(sgf).obs
    expected = th.tensor(
        [
            [
                [[1, 0], [0, 0], [0, 0]],
                [[0, 1], [0, 0], [0, 0]],
                [[0, 0], [0, 0], [0, 0]],
            ]
        ],
        device=actual.device,
    )
    assert th.equal(expected, actual)


def test_from_sgf_2():
    # NOTE: Hex (boardlaw) swaps/transposes locations based upon whose turn it is.
    sgf = "(;AP[HexGui:1.0.]FF[4]GM[11]SZ[3];AB[a1][b1]AW[a2]PL[W])"
    actual = from_sgf(sgf).obs
    expected = th.tensor(
        [
            [
                [[0, 1], [1, 0], [0, 0]],
                [[0, 1], [0, 0], [0, 0]],
                [[0, 0], [0, 0], [0, 0]],
            ]
        ],
        device=actual.device,
    )
    assert th.equal(expected, actual)


def test_cell_to_action():
    for i in range(9):
        for j in range(9):
            a, b = action_to_cell(cell_to_action(i, j, seat=0), seat=0)
            assert i == a
            assert j == b

            a, b = action_to_cell(cell_to_action(i, j, seat=1), seat=1)
            assert i == a
            assert j == b

    assert cell_to_action(0, 0, seat=1) == 0
    assert cell_to_action(0, 0, seat=0) == 0
    assert cell_to_action(8, 8, seat=1) == 80
    assert cell_to_action(8, 8, seat=0) == 80
    assert cell_to_action(0, 8, seat=0) == 8
    assert cell_to_action(8, 0, seat=1) == 8
