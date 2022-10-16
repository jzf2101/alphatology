import torch as th
import numpy as np
import os, random


def seed_everything(seed: int) -> int:
    """Implementation from PyTorchLightning.

    Function that sets seed for pseudo-random number generators in:
    pytorch, numpy, python.random
    In addition, sets the following environment variables:

    - `PL_GLOBAL_SEED`: will be passed to spawned subprocesses (e.g. ddp_spawn backend).

    Args:
        seed: the integer value seed for global random state in Lightning.
            If `None`, will read seed from `PL_GLOBAL_SEED` env variable
            or select it randomly.
    """
    os.environ["PL_GLOBAL_SEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    th.manual_seed(seed)
    th.cuda.manual_seed_all(seed)
    return seed
