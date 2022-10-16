import boardlaw_utils
import flags

import os
import tqdm

import boardlaw_utils
from templates import concepts

import utils
import random

if __name__ == "__main__":
    FLAGS = flags.flags().parse_args()
    utils.seed_everything(FLAGS.seed)
    os.makedirs(f"output/{FLAGS.jobname}", exist_ok=True)
    puzzles = concepts.get_positive(FLAGS.concept, 500, 0)
    output = []
    puzzles = [p for p in puzzles if p["name"] == "pattern4"]
    puzzles = random.sample(puzzles, min(10, len(puzzles)))
    for puzzle_i, puzzle in tqdm.tqdm(enumerate(puzzles), desc="Generating videos."):
        for test_idx, line in enumerate(puzzle["lines"]):
            example_name = f"{puzzle['concept']}-{puzzle['name']}-{test_idx}-{puzzle['attacker']}-{puzzle['defender']}-{puzzle_i}"
            output_path_correct = f"./output/{FLAGS.jobname}/{example_name}.mp4"
            print(example_name)
            print(puzzle["template"])
            print(line)
            board = boardlaw_utils.from_string(puzzle["template"])
            boardlaw_utils.save_puzzle_error_correct(
                board, line["forcing"], line["expected"], output_path_correct
            )
            log = f"""{puzzle["concept"]}\t{puzzle["name"]}\t{test_idx}\t{puzzle["tested_agent"]}\t{puzzle["attacker"]}\t{puzzle["defender"]}"""
            output.append(
                f"""
<div>
<script>
function good(log) {{
    console.log(log + '\t' + 'good')
}}
function bad(log) {{
    console.log(log + '\t' + 'bad')
}}
</script>
    <div style="width:700px;">
        <div style="width:300px; float:left;">
            <video width="320" height="240" controls loop autoplay>
                <source src="{example_name}.mp4" type="video/mp4">
                Your browser does not support the video tag.
        </video>
        </div>
        <div style="width:300px; float:right;">
            <button onclick="good('{log}')">Good</button>
            <button onclick="bad('{log}')">Bad</button>

            <table>
                <tbody>
                    <tr>
                        <th>concept</th>
                        <td>{puzzle["concept"]}</td>
                    </tr>
                    <tr>
                        <th>puzzle</th>
                        <td>{puzzle["name"]} : {test_idx}</td>
                    </tr>
                    <tr>
                        <th>tested_agent</th>
                        <td>{puzzle["tested_agent"]}</td>
                    </tr>
                    <tr>
                        <th>attacker</th>
                        <td>{puzzle["attacker"]}</td>
                    </tr>
                    <tr>
                        <th>defender</th>
                        <td>{puzzle["defender"]}</td>
                    </tr>
                    <tr>
                        <th>forcing</th>
                        <td>{line["forcing_cells"]}</td>
                    </tr>
                    <tr>
                        <th>expected</th>
                        <td>{line["expected_cells"]}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <div style="clear: both;" />
</div>
"""
            )
    out = "<div>" + "\n".join(output) + "</div>"
    with open(f"output/{FLAGS.jobname}/{FLAGS.concept}-walkthrough.html", "w") as f:
        f.write(out)
