# alphatology
Code for Evaluation Beyond Task Performance: Analyzing Concepts in AlphaZero in Hex (NeurIPS 2022)

### setup jobs (assumes slurm)
```bash
# generates jobs in jobs/[job-name].sh
mkdir times
./pipelines/icml2020.sh

# download results (I moved this into a bashscript for myself)
# $1 == jobname.
rsync --progress [USER]@[REMOTE]:[PATH_TO_PROJECT]/results/$1/\* results/$1
```

### tests
```bash
pytest tests/*.py --disable-pytest-warnings
```
