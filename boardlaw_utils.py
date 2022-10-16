from flags import flags
import numpy as np
import torch as th

import boardlaw
from boardlaw.hex import Hex
from boardlaw import sql, elos

import pandas as pd

from typing import List, Tuple

from boardlaw import mcts
from boardlaw.arena import common
from boardlaw import backup

import random

# hex.Hex
HexBoard = None


def get_agent_args(run: str, idx: int, n_nodes: int) -> mcts.MCTSAgent:
    """Get the given agent by `run` and `idx`. These index into boardlaw's agents."""
    try:
        agent = common.agent(run, idx)
        tested_agent = mcts.MCTSAgent(agent.network, n_nodes=n_nodes)
        tested_agent.network.to("cuda")
    except:
        print(
            "Agent not downloaded. Manually download the networks s.t. there are less"
            "network calls during experiment execution. Use backup.download_agent(*)."
        )
        return None
    return tested_agent


def action_to_cell(action: int, seat: int, S: int = 9) -> Tuple[int, int]:
    if seat == 0:
        row, col = action // S, action % S
    else:
        row, col = action % S, action // S
    return row, col


def cell_to_action(row: int, col: int, seat: int, S: int = 9) -> int:
    if seat == 0:
        return row * S + col
    else:
        return row + col * S


def swap_colors(action: int, seat_from: int, S: int = 9):
    i, j = action_to_cell(action, seat_from)
    seat_to: int = other_player(seat_from)
    # transpose row and col
    return cell_to_action(j, i, seat_to)


def show_puzzle(puzzle):
    """Returns (for notebook) video of forced and expected moves.

    Saves the video as bytes, compatible with boardlaw's rebar.
    """
    from rebar import arrdict, recording

    def _show(board, forcing_actions, expected_actions):
        trace = []
        for i, (f_a, e_a) in enumerate(zip(forcing_actions, expected_actions)):
            board, _ = board.step(th.tensor([f_a], device="cuda"))
            trace.append(arrdict.arrdict(worlds=board))
            board, _ = board.step(th.tensor([e_a], device="cuda"))
            trace.append(arrdict.arrdict(worlds=board))
        return arrdict.stack(trace)

    def _record_worlds(worlds, N=0):
        state = arrdict.numpyify(worlds)
        with recording.ParallelEncoder(
            boardlaw.analysis.plot_all(worlds.plot_worlds), N=N, fps=3
        ) as encoder:
            for i in range(state.board.shape[0]):
                encoder(state[i])
        return encoder

    trace = _show(
        puzzle["board"], puzzle["forcing_actions"], puzzle["expected_actions"]
    )
    _record_worlds(trace.worlds).save(f"{puzzle['concept']}-{puzzle['template']}.mp4")
    return _record_worlds(trace.worlds).notebook()


def save_puzzle_error(puzzle, output_path):
    """Returns (for notebook) video of forced and expected moves.

    Saves the video as bytes, compatible with boardlaw's rebar.
    """
    from rebar import arrdict, recording
    from boardlaw.analysis import plot_all

    def _show(board, forcing_actions, expected_actions):
        trace = []
        for i, (f_a, e_a) in enumerate(zip(forcing_actions, expected_actions)):
            board, _ = board.step(th.tensor([f_a], device="cuda"))
            trace.append(arrdict.arrdict(worlds=board))
            board, _ = board.step(th.tensor([e_a], device="cuda"))
            trace.append(arrdict.arrdict(worlds=board))
        return arrdict.stack(trace)

    def _record_worlds(worlds, N=0):
        state = arrdict.numpyify(worlds)
        with recording.ParallelEncoder(
            plot_all(worlds.plot_worlds), N=N, fps=2
        ) as encoder:
            for i in range(state.board.shape[0]):
                encoder(state[i])
        return encoder

    board = from_string(puzzle["template"])
    trace = _show(
        board,
        puzzle["forcing_actions"],
        puzzle["expected_actions"],
    )
    # Saves readable as mp4.
    _record_worlds(trace.worlds).save(f"{output_path}")


def save_puzzle_error_correct(board, forcing_actions, expected_actions, output_path):
    """Returns (for notebook) video of forced and expected moves.

    Saves the video as bytes, compatible with boardlaw's rebar.
    """
    from rebar import arrdict, recording
    from boardlaw.analysis import plot_all

    def _show(board, forcing_actions, expected_actions):
        trace = [arrdict.arrdict(worlds=board)]
        for i, (f_a, e_a) in enumerate(zip(forcing_actions, expected_actions)):
            board, _ = board.step(th.tensor([f_a], device="cuda"))
            trace.append(arrdict.arrdict(worlds=board))
            board, _ = board.step(th.tensor([e_a], device="cuda"))
            trace.append(arrdict.arrdict(worlds=board))
        return arrdict.stack(trace)

    def _record_worlds(worlds, N=0):
        state = arrdict.numpyify(worlds)
        with recording.ParallelEncoder(
            plot_all(worlds.plot_worlds), N=N, fps=4
        ) as encoder:
            for i in range(state.board.shape[0]):
                encoder(state[i])
        return encoder

    trace = _show(
        board,
        forcing_actions,
        expected_actions,
    )
    # Saves readable as mp4.
    _record_worlds(trace.worlds).save(f"{output_path}")


def from_string(s, **kwargs):
    """Moved implementation from boardlaw's test files which were not
    immediately importable outside the project.

    Example:

    s = '''
    bwb
    wbw
    ...
    '''

    """

    def _strip(s):
        return "\n".join(l.strip() for l in s.splitlines() if l.strip())

    def _board_size(s):
        return len(_strip(s).splitlines())

    def _board_actions(s):
        size = _board_size(s)
        board = np.frombuffer((_strip(s) + "\n").encode(), dtype="S1").reshape(
            size, size + 1
        )[:, :-1]
        indices = np.indices(board.shape)

        bs = indices[:, board == b"b"].T
        ws = indices[:, board == b"w"].T

        assert len(bs) - len(ws) in {0, 1}, len(bs) - len(ws)

        actions = []
        for i in range(len(ws)):
            actions.append([bs[i, 0], bs[i, 1]])
            actions.append([ws[i, 1], ws[i, 0]])

        if len(ws) < len(bs):
            actions.append([bs[-1, 0], bs[-1, 1]])

        return th.tensor(actions)

    worlds = Hex.initial(n_envs=1, boardsize=_board_size(s), **kwargs)
    for a in _board_actions(s).to(worlds.device):
        worlds, terminal = worlds.step(a[None])
        if terminal.terminal:
            assert False, "Template is already over."
    return worlds


def from_sgf_file(sgf_path: str):
    with open(sgf_path, "r") as f:
        return from_sgf(f.read())


def from_sgf(sgf: str) -> Hex:
    """Load a board from an sgf string."""

    def _from_notation(notation: str):
        # Ex: e1
        row: str = notation[0]  # e
        row: int = ord(row) - ord("a")  # 4 = (60 + 56)
        col: int = int(notation[1:]) - 1  # 0 = 1 - 1

        return col, row

    # sgf as hexgui saves it.
    # (;AP[HexGui:0.9.GIT]FF[4]GM[11]SZ[9];AB[g1][f3][e5][d6][d7]AW[i1][c2][c7][e7][c9]PL[B])
    # (;AP[HexGui:1.0.]FF[4]GM[11]SZ[3];AB[a2][b3]AW[a1]PL[W])
    boardsize = int(
        sgf.split(";")[-2].split("SZ")[-1].replace("[", "").replace("]", "")
    )
    moves = sgf.split(";")[-1]
    w, b = moves.split("AW")[-1], moves.split("AW")[0]
    w, b = w.split("PL")[0], b.replace("AB", "")

    _split_moves = lambda x: ["".join(y.split("]")) for y in x.split("[") if y]

    b = [_from_notation(m) for m in _split_moves(b)]
    w = [_from_notation(m) for m in _split_moves(w)]

    assert len(b) - len(w) in {0, 1}

    actions = []
    for i in range(len(w)):
        actions.append([b[i][0], b[i][1]])
        actions.append([w[i][1], w[i][0]])

    if len(w) < len(b):
        actions.append([b[-1][0], b[-1][1]])

    actions = th.tensor(actions)

    worlds = Hex.initial(n_envs=1, boardsize=boardsize)
    for a in actions.to(worlds.device):
        worlds, _ = worlds.step(a[None])
    return worlds


def other_player(player: int) -> int:
    return {0: 1, 1: 0}[player]


def _floatify(l: List) -> List[float]:
    """For json saving convert values to raw float."""
    return [float(i) for i in l]


def step(agent, board: HexBoard) -> Tuple[HexBoard, int, List[float], bool]:
    """Step the agent on the board."""
    if agent.kwargs["n_nodes"] == 0:
        with th.no_grad():
            output = agent.network(board)
            logits = output.logits
            actions = logits.argmax().unsqueeze(0)
            value = output.v
    else:
        with th.no_grad():
            output = agent(board)
            actions = output.actions
            logits = output.logits
            value = output.v

    next_board, terminal = board.step(actions)
    return (
        next_board,
        actions.cpu().item(),
        _floatify(logits.squeeze()),
        terminal,
        value,
    )
