import argparse
import datetime
import flags
import itertools
import json
import os


def main(FLAGS):
    experiment = FLAGS.experiment
    assert "json" in experiment
    with open(experiment, "r") as f:
        settings = json.load(f)

    precondition_valid_settings(settings["settings"])

    experiment = experiment.split("/")[-1].replace(".json", "")
    if FLAGS.date is None:
        jobname = datetime.datetime.now().strftime(f"{experiment}-%Y-%m-%d")
    else:
        jobname = f"{experiment}-{FLAGS.date}"

    jobs_per_gpu = settings["jobs_per_gpu"]
    jobs = generate_jobs(experiment, jobname, settings, jobs_per_gpu)
    is_using_gpu = settings["use_gpu"]
    write_jobs(jobs, jobname, experiment, is_using_gpu, jobs_per_gpu)


def precondition_valid_settings(settings):
    # Ensure there are no collisions.
    for k, v in settings.items():
        num_settings = len(v)
        assert num_settings == len(
            set([flags.shorten_if_str(_v) for _v in v])
        ), f"Collision. Change values for {k}."


def generate_jobs(experiment, jobname, settings, jobs_per_gpu):
    settings["settings"]["jobname"] = [jobname]
    options = list(itertools.product(*settings["settings"].values()))
    keys = list(settings["settings"].keys())
    jobs = []

    options = [o for o in options]
    python_script = settings["script"]
    idx = 0
    if jobs_per_gpu == 1:
        for option in options:
            zipped = list(zip(keys, list(option)))
            _options = {k: v for k, v in zipped}
            job_text = _template_option(python_script, _options)
            job = setup(job_text, idx, experiment)
            idx += 1
            jobs.append(job)
    else:
        for start in range(0, len(options), jobs_per_gpu):
            batch = options[start : start + jobs_per_gpu]
            texts = []
            for option in batch:
                zipped = list(zip(keys, list(option)))
                _options = {k: v for k, v in zipped}
                job_text = _template_option(python_script, _options)
                texts.append(job_text)
            job = setup_parallel(texts, idx, experiment)
            idx += 1
            jobs.append(job)
    return jobs


def write_jobs(jobs, jobname, experiment, is_using_gpu, jobs_per_gpu):
    jobs_file = _template_file(jobs, experiment, is_using_gpu, jobs_per_gpu)
    os.makedirs("jobs", exist_ok=True)
    os.makedirs(f"results/", exist_ok=True)
    os.makedirs(f"results/{jobname}", exist_ok=True)
    os.makedirs(f"output/{jobname}", exist_ok=True)
    with open(f"./jobs/{jobname}.sh", "w") as f:
        f.write(jobs_file)


def _template_file(texts, experiment, is_using_gpu, jobs_per_gpu):
    text = "".join(texts)
    if is_using_gpu:
        raise NotImplementedError("Add the appropriate line to request GPUs.")
        using_gpu = "#SBATCH -p nameofgpupartition --gres=gpu:1"
        mem = "32G"
    else:
        using_gpu = ""
        # dataset creation should be minimal.
        mem = "8G"
    # using_gpu = ""
    out = f"""#!/bin/sh

# Request half an hour of runtime:
#SBATCH --time=24:00:00

# Ask for the GPU partition and 1 GPU
# skipping this for now.
{using_gpu}

# Use more memory (8GB) and correct partition.
#SBATCH --mem={mem}

# Specify a job name:
#SBATCH -J {experiment}

# Specify an output file
#SBATCH -o ./out/%x-%a.out
#SBATCH -e ./err/%x-%a.out

#SBATCH -a 0-{len(texts) - 1}%12
#SBATCH -n {jobs_per_gpu}

module load cuda/11.1.1 gcc/10.2 python/3.7.4
conda activate alpha

mkdir -p ./out/
mkdir -p ./err/
mkdir -p ./log/
mkdir -p ./results/

{text}
"""
    return out


def setup(text, index, experiment):
    return f"""
if [ "$SLURM_ARRAY_TASK_ID" -eq {index} ];
then
{text}
exit_code=$?
if [[ $exit_code = 0 ]]; then
echo "{index}\t{text}" >> log/{experiment}_success.tsv
elif [[ $exit_code = 1 ]]; then
echo "{index}\t{text}" >> log/{experiment}_failed.tsv
fi
fi
"""


def setup_parallel(texts, index, experiment):
    text = "\n".join([f"{t} &" for t in texts])
    return f"""
if [ "$SLURM_ARRAY_TASK_ID" -eq {index} ];
then
{text}
wait
exit_code=$?
if [[ $exit_code = 0 ]]; then
echo "{index}\t{text}" >> log/{experiment}_success.tsv
elif [[ $exit_code = 1 ]]; then
echo "{index}\t{text}" >> log/{experiment}_failed.tsv
fi
fi
"""


def _template_option(
    experiment,
    options,
):
    """Generates the template for an a call to train."""
    joined_options = "  ".join(
        [f"--{k} {_handle_value(v)}" for k, v in options.items()]
    )
    return f"""python {experiment}.py {joined_options}"""


def _handle_value(v):
    if isinstance(v, str) and " " in v:
        return f"'{v}'"
    return v


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", type=str, required=True)
    parser.add_argument("--date", type=str, required=False, default=None)
    FLAGS = parser.parse_args()
    main(FLAGS)
