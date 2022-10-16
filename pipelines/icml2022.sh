DATE="icml2022"

python job.py --experiment experiments/positive.json --date $DATE
python job.py --experiment experiments/negative.json --date $DATE

python job.py --experiment experiments/generate.json --date $DATE
python job.py --experiment experiments/encode.json --date $DATE
python job.py --experiment experiments/probing.json --date $DATE

almostjid1=$(sbatch jobs/generate-$DATE.sh)
arr=($almostjid1)
jid1=${arr[3]}

almostjid2=$(sbatch --dependency=afterok:$jid1 jobs/encode-$DATE.sh)
arr2=($almostjid2)
jid2=${arr2[3]}

sbatch --dependency=afterok:$jid2 jobs/probing-$DATE.sh

sbatch jobs/positive-$DATE.sh
sbatch jobs/negative-$DATE.sh 
