from typing import List
import torch as th
from scipy import signal
from templates import concepts
import templates.templates


class ConceptDetector:
    def __init__(self, concept) -> None:
        self.filters = build_filters(concept)

    def __call__(self, board) -> bool:
        return detect(board.obs, self.filters)


def build_filters(concept: str) -> List[th.tensor]:
    return [schema_to_filter(s) for s in concepts.get_schemas(concept)]


def schema_to_filter(schema) -> th.tensor:
    r, c = templates.templates.get_window(schema["cells_used"])
    fltr = [
        [[0 for _ in range(c + 1)] for _ in range(r + 1)],
        [[0 for _ in range(c + 1)] for _ in range(r + 1)],
    ]
    for _r, _c in schema["cell_moves"]:
        fltr[0][_r][_c] = -1
        fltr[1][_r][_c] = -1
    for _r, _c in schema["cells_attacking"]:
        fltr[0][_r][_c] = 1
    for _r, _c in schema["cells_defending"]:
        fltr[1][_r][_c] = 1
    return th.tensor(fltr)


def detect(board: th.tensor, filters: List[th.tensor]):
    """Detect the given pattern (defined by the filters) on the board.

    Parameters
    ----------
    board : ?B x H x W x 2
        We assume B = 0/1.
    filters : 2 x N x M
        The first slice is the positive filter; the second, negative.


    Each filter has a positive and a negative filter.
    When checking for, say, a black bridge, we look as the black positions
    and check for a bridge--indexing into the black positions of the board and the
    positive positions of the filter--then, we check for mitigating moves of the
    white pieces--indexing ingto the white positions of the board and the negative positions
    of the filter.

    Example
    -------
    ```
    # bridge (filter, f2)
    board
        b . w      1 0 0 | 0 0 1
        . b .  --> 0 1 0 | 0 0 0
        w . .      0 0 0 | 1 0 0
    filters
        # positive
        1 0
        0 1
        # negative
        -1 -1
        -1 -1

    Leads to
    pos  | neg  | total
    2 0  | 0 -1 | 2 -1
    0 1  | -1 0 | -1 0

    Because max (total) == max (filter), we have a bridge.

    # negative case.
    board
        b . w      1 0 0 | 0 0 1
        w b .  --> 1 1 0 | 0 0 0
        w . .      0 0 0 | 1 0 0
    filters
        # positive
        1 0
        0 1
        # negative
        -1 -1
        -1 -1

    Leads to
    pos  | neg  | total
    2 0  | -1 -1 | 1 -1
    0 1  | -1 0 | -1 0

    Because max (total) != max (filter), there is no bridge.
    """
    board = board.squeeze().cpu()
    for A, B in [(0, 1), (1, 0)]:
        for filter in filters:
            output_A = signal.convolve2d(
                board[:, :, A].cpu(), filter[0].cpu(), mode="valid"
            )
            output_B = signal.convolve2d(
                board[:, :, B].cpu(), filter[1].cpu(), mode="valid"
            )
            output = output_A + output_B
            f_max = filter[filter > 0].sum()
            # Check that the pattern existed by checking the max value extant
            # vs the max value possible: All the 1s must line up, and no -1s
            # must be included.
            if output.max() == f_max:
                return True
    return False


def detect_bridge(board):
    """This was hard-coded. We now generate these filters from the schemas
    in templates/schema/*.py.
    """
    # f0, f1 are transposes of each other.
    f0 = th.tensor([[[0, -1, 1], [1, -1, 0]], [[0, -1, -1], [-1, -1, 0]]])
    f1 = th.tensor([[[0, 1], [-1, -1], [1, 0]], [[0, -1], [-1, -1], [-1, 0]]])
    f2 = th.tensor([[[1, -1], [-1, 1]], [[-1, -1], [-1, -1]]])
    return detect(board.obs, [f0, f1, f2])
