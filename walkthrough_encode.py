from typing import Tuple
import flags

import tqdm
import utils

import templates.templates
from templates import concepts, probing
import matplotlib.pyplot as plt
from rebar import arrdict

from detect import ConceptDetector


def get_examples(concept, conditions, examples_per_schema, selectivity_mask):
    schemas = concepts.get_schemas(concept)
    examples = []

    for s in schemas:
        if "edge" in s:
            a, d = templates.templates.get_edge_roles(s)
        else:
            a, d = 1, 0
        for c in conditions:
            c["roles"] = {"attacker": a, "defender": d}
        for board_id in range(examples_per_schema):
            ts = probing.generate_templates_probing(
                s,
                0,
                conditions,
                board_id,
                neg_example="RSA_SHUFFLE_ALL",
                selectivity_mask=selectivity_mask,
            )
            examples.extend(ts)
    return examples


def save_fig(board, path):
    ax = board.plot_worlds(arrdict.numpyify(arrdict.arrdict(board)))
    plt.savefig(path)
    plt.close(ax.figure)


if __name__ == "__main__":
    FLAGS = flags.flags().parse_args()
    utils.seed_everything(FLAGS.seed)

    CENTER = (4, 4)
    moves = [m for m in templates.templates.get_base_moves() if m != CENTER]
    selectivity_mask = {
        k: v
        for k, v in zip(
            moves,
            templates.util.shuffled(moves),
        )
    }
    selectivity_mask[CENTER] = CENTER

    ts = []
    conditions = [
        {
            "intrude": False,
            "connect": False,
            "owner_to_play": False,
        },
        # {
        #     "intrude": True,
        #     "connect": False,
        #     "owner_to_play": False,
        # },
        {
            "intrude": False,
            "connect": True,
            "owner_to_play": False,
        },
        # {
        #     "intrude": True,
        #     "connect": True,
        #     "owner_to_play": False,
        # },
        #
        {
            "intrude": False,
            "connect": False,
            "owner_to_play": True,
        },
        # {
        #     "intrude": True,
        #     "connect": False,
        #     "owner_to_play": True,
        # },
        {
            "intrude": False,
            "connect": True,
            "owner_to_play": True,
        },
        # {
        #     "intrude": True,
        #     "connect": True,
        #     "owner_to_play": True,
        # },
    ]
    if FLAGS.concept in {"dead", "captured"}:
        conditions = [
            {
                "intrude": False,
                "connect": False,
                "owner_to_play": False,
            },
            {
                "intrude": False,
                "connect": False,
                "owner_to_play": True,
            },
        ]
    ts = get_examples(
        FLAGS.concept,
        conditions,
        1,
        selectivity_mask,
    )

    use_concept_detector = FLAGS.concept in {"bridge"}

    if use_concept_detector:
        concept_detector = ConceptDetector(FLAGS.concept)

    output = []
    for i, t in tqdm.tqdm(enumerate(ts), desc="Generating board images."):
        name = f"{t['concept']}-{t['name']}-{t['attacker']}-{t['defender']}-{t['intrude']}-{t['connect']}-{t['owner_to_play']}_{i}"
        pos, neg, sel_pos, sel_neg = probing.template_to_board_probing(t)
        if pos is None or neg is None or sel_pos is None or sel_neg is None:
            continue

        if use_concept_detector:
            if concept_detector(neg):
                print("skipping board; neg board has concept.")
                continue

        path_pos = f"./output/{FLAGS.jobname}/{name}_pos.png"
        path_neg = f"./output/{FLAGS.jobname}/{name}_neg.png"

        path_sel_pos = f"./output/{FLAGS.jobname}/{name}_sel_pos.png"
        path_sel_neg = f"./output/{FLAGS.jobname}/{name}_sel_neg.png"
        save_fig(pos, path_pos)
        save_fig(neg, path_neg)
        save_fig(sel_pos, path_sel_pos)
        save_fig(sel_neg, path_sel_neg)
        #             <img width="320" height="240" src="{name}_sel_pos.png" >
        #     <img width="320" height="240" src="{name}_sel_neg.png" >
        log = f"""{t["concept"]}\t{t["name"]}\t{t["attacker"]}\t{t["attacker"]}\t{t["defender"]}\t{t['intrude']}\t{t['connect']}\t{t['owner_to_play']}"""
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
    <div style="width:1300px;">
        <div style="width:1000px; float:left;">
            <span> Pos left; Neg right. </span>
            <img width="320" height="240" src="{name}_pos.png" >
            <img width="320" height="240" src="{name}_neg.png" >
        </div>
        <div style="width:1000px; float:left;">
            <span> Sel Pos left; Sel Neg right. </span>
            <img width="320" height="240" src="{name}_sel_pos.png" >
            <img width="320" height="240" src="{name}_sel_neg.png" >
        </div>
        <div style="width:300px; float:right;">
            <button onclick="good('{log}')">Good</button>
            <button onclick="bad('{log}')">Bad</button>

            <table>
                <tbody>
                    <tr>
                        <th>board_id</th>
                        <td>{t["board_id"]}</td>
                    </tr>
                    <tr>
                        <th>concept</th>
                        <td>{t["concept"]}</td>
                    </tr>
                    <tr>
                        <th>t</th>
                        <td>{t["name"]}</td>
                    </tr>
                    <tr>
                        <th>attacker</th>
                        <td>{t["attacker"]}</td>
                    </tr>
                    <tr>
                        <th>defender</th>
                        <td>{t["defender"]}</td>
                    </tr>
                    <tr>
                        <th>intrude</th>
                        <td>{t["intrude"]}</td>
                    </tr>
                    <tr>
                        <th>connect</th>
                        <td>{t["connect"]}</td>
                    </tr>
                    <tr>
                        <th>owner to play</th>
                        <td>{t["owner_to_play"]}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <div style="clear: both;" />
    <hr />
</div>
"""
        )
    out = "<div>" + "\n".join(output) + "</div>"
    with open(f"output/{FLAGS.jobname}/{FLAGS.concept}-walkthrough.html", "w") as f:
        f.write(out)
