import argparse

STR_SHORTEN = 3


def flags():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt_idx", default=20, type=int)
    parser.add_argument("--test_nodes", default=64, type=int)
    parser.add_argument("--seed", default=42, type=int)
    parser.add_argument("--concept", type=str, required=False)
    parser.add_argument(
        "--run",
        type=str,
        default="2021-02-20 22-35-41 grubby-wrench",
        help="model from @boardlaw to use.",
    )
    parser.add_argument(
        "--jobname",
        default="",
        type=str,
        help="name of job/output folder",
        required=False,
    )
    parser.add_argument(
        "--templates_per_concept",
        default=10_000,
        type=int,
        help="Number of templates per concept to generate",
        required=False,
    )
    return parser


def get_num_ckpt_idx(run: str) -> int:
    return {
        "2021-02-20 22-35-41 grubby-wrench": 21,
        "2021-02-20 23-35-25 simple-market": 20,
        "2021-02-20 21-33-42 recent-annex": 20,
        "2021-02-20 22-18-43 baggy-cans": 21,
        "2021-02-20 22-55-43 vital-bubble": 21,
    }[run]


def get_num_layers(run: str) -> int:
    return {
        "2021-02-20 22-35-41 grubby-wrench": 10,
        "2021-02-20 23-35-25 simple-market": 6,  # raw, 8 + output.
        "2021-02-20 21-33-42 recent-annex": 10,
        "2021-02-20 22-18-43 baggy-cans": 6,
        "2021-02-20 22-55-43 vital-bubble": 4,
    }[run]


def probing():
    parser = flags()
    parser.add_argument(
        "--probe",
        type=str,
        required=True,
        help="lr: LogisticRegression. mlp: MLP!",
    )
    return parser


def filename(ns):
    """Generates a filename based on the arguments in the namesapce."""
    return _namespace_to_string_with_change(
        ns,
        {
            "jobname": None,
        },
    )


def generate_filename(ns):
    """Generates a filename based on the arguments in the namespace.

    Renames the given args s.t. the files can be loaded easily in other
    files with different arguements. (Here, so the probing and encoding
    can be split.)
    """
    return _namespace_to_string_with_change(
        ns,
        {
            "jobname": "generate",
            "layer": None,
            "probe": None,
            "encode_jobname": None,
            "ckpt_idx": None,
            "run": None,
        },
    )


def encoding_filename(ns):
    """Generates a filename based on the arguments in the namespace.

    Renames the given args s.t. the files can be loaded easily in other
    files with different arguements. (Here, so the probing and encoding
    can be split.)
    """
    return _namespace_to_string_with_change(
        ns,
        {"jobname": "encode", "probe": None, "encode_jobname": None, "ckpt_idx": None},
    )


def encoding_filename_layer(ns, layer):
    """Generates a filename based on the arguments in the namespace.

    Renames the given args s.t. the files can be loaded easily in other
    files with different arguements. (Here, so the probing and encoding
    can be split.)
    """
    return (
        _namespace_to_string_with_change(
            ns,
            {"jobname": "encode", "probe": None, "encode_jobname": None},
        )
        + f"_{layer}"
    )


def instancewise_probing_filename(ns):
    return _namespace_to_string_with_change(
        ns,
        {
            "jobname": None,
            "layer": None,
            "encode_jobname": None,
        },
    )


def _namespace_to_string_with_change(ns, kvs) -> str:
    # Splice in the kvs, which will effectively be used to remove these
    # entries from the name. Here, we just don't want the jobname to be saved
    # as its redundant with the folder its saved into.

    out = {**vars(ns), **kvs}
    out = _dict_to_string(out)
    return out


def shorten_if_str(v):
    if isinstance(v, str):
        if " " in v:
            return v.split()[-1][:STR_SHORTEN]
        return v[:STR_SHORTEN]
    else:
        return v


def _dict_to_string(out) -> str:
    def _mb_list_to_string(v) -> str:
        if isinstance(v, list):
            return "@".join(sorted(v))
        else:
            return v

    def _filter(v) -> bool:
        if v:
            return True
        elif isinstance(v, int) and v == 0:
            # keep = 0s.
            return True
        else:
            # filter out empty string, None, empty list, False.
            return False

    # Convert arguements (potentially lists) into strings.
    out = {k: _mb_list_to_string(v) for k, v in out.items()}

    # We shorten key names and value names so that the filename isn't rejected for being too
    # long. Be very careful about collisions.
    out = [
        f"{k[:STR_SHORTEN]}:{shorten_if_str(v)}" for k, v in out.items() if _filter(v)
    ]
    return "-".join(out).replace("/", "_")
