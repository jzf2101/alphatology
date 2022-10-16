"""Utilities for building templates and generating random walks.
"""
import itertools
import random

from probe import N


def filter(predicate, iterable):
    return list(itertools.filterfalse(lambda x: not predicate(x), iterable))


def at_top(m):
    r, _ = m
    return r == 0


def at_bot(m):
    r, _ = m
    return r == 8


def at_left(m):
    _, c = m
    return c == 0


def at_right(m):
    _, c = m
    return c == 8


def go_up(m):
    r, _ = m
    up = lambda rc: rc[0] < r
    return filter(up, get_neighbors(m))


def go_down(m):
    r, _ = m
    down = lambda rc: rc[0] > r
    return filter(down, get_neighbors(m))


def go_left(m):
    _, c = m
    left = lambda rc: rc[1] < c
    return filter(left, get_neighbors(m))


def go_right(m):
    _, c = m
    right = lambda rc: rc[1] > c
    return filter(right, get_neighbors(m))


def connect_up(m, cells_used):
    return _build_path(m, at_top, go_up, cells_used, [go_left, go_right])


def connect_down(m, cells_used):
    return _build_path(m, at_bot, go_down, cells_used, [go_left, go_right])


def connect_left(m, cells_used):
    return _build_path(m, at_left, go_left, cells_used, [go_up, go_down])


def connect_right(m, cells_used):
    return _build_path(m, at_right, go_right, cells_used, [go_up, go_down])


def _build_path(m, at_edge, go_direction, cells_used, orthogonal_directions=None):
    path = []
    current = m
    while not at_edge(current):
        candidates_moves = go_direction(current)
        moves = [m for m in candidates_moves if m not in (cells_used + path)]
        if not moves and orthogonal_directions is not None:
            # side-tracking ok.
            for d in orthogonal_directions:
                orthogonal_moves = d(current)
                moves = [m for m in orthogonal_moves if m not in (cells_used + path)]
                if moves:
                    break
        if not moves:
            raise AssertionError("Failed to find a path. Poor generantion.")
        current = random.choice(moves)
        path.append(current)
    return path


def get_left_right(c1, c2):
    if is_left_of(c1, c2):
        return c1, c2
    else:
        return c2, c1


def get_leftmost(moves):
    return _get_most(moves, is_left_of)


def get_rightmost(moves):
    return _get_most(moves, lambda x, y: not is_left_of(x, y))


def get_topmost(moves):
    return _get_most(moves, is_top_of)


def get_botmost(moves):
    return _get_most(moves, lambda x, y: not is_top_of(x, y))


def _get_most(moves, func):
    current = moves[0]
    for m in moves[1:]:
        if func(m, current):
            current = m
    return current


def get_top_bot(c1, c2):
    if is_top_of(c1, c2):
        return c1, c2
    else:
        return c2, c1


def is_left_of(m1, m2):
    _, r1 = m1
    _, r2 = m2
    return r1 <= r2


def is_top_of(m1, m2):
    c1, _ = m1
    c2, _ = m2
    return c1 <= c2


def get_neighbors(m):
    r, c = m
    inside_board = lambda rc: rc[0] >= 0 and rc[0] <= 8 and rc[1] >= 0 and rc[1] <= 8
    neighbor_directions = [
        # above
        (r - 1, c),
        (r - 1, c + 1),
        # left
        (r, c - 1),
        # right
        (r, c + 1),
        # below
        (r + 1, c),
        (r + 1, c - 1),
    ]
    return filter(inside_board, neighbor_directions)
