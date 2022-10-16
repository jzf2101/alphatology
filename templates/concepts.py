import templates.positive
import templates.negative
import templates.probing

from templates.schemas.bridge import schemas as _bridge_schemas
from templates.schemas.bottleneck import schemas as _bottleneck_schemas
from templates.schemas.crescent import schemas as _crescent_schemas
from templates.schemas.escape import schemas as _escape_schemas
from templates.schemas.span import schemas as _span_schemas
from templates.schemas.trapezoid import schemas as _trapezoid_schemas
from templates.schemas.edge_a2 import schemas as _edge2_schemas
from templates.schemas.edge_a3 import schemas as _edge3_schemas
from templates.schemas.captured import schemas as _captured_schemas
from templates.schemas.dead import schemas as _deadcell_schemas

import copy


def is_positive_concept(concept):
    return concept not in {"dead", "captured"}


def is_negative_concept(concept):
    return concept in {"dead", "captured"}


def get_negative(concept, templates_per_concept, num_rand_to_add: int = 0):
    assert concept in {"captured", "dead"}
    return templates.negative.get_templates(
        get_schemas(concept), templates_per_concept, num_rand_to_add
    )


def get_positive(concept, templates_per_concept, num_rand_to_add: int = 0):
    assert concept in {
        "bridge",
        "edge",
        "crescent",
        "span",
        "bottleneck",
        "escape",
        "trapezoid",
    }
    return templates.positive.get_templates(
        get_schemas_behavioral(concept), templates_per_concept, num_rand_to_add
    )


def get_probing(
    concept,
    templates_per_concept,
    conditions,
    neg_example,
    num_rand_to_add,
    selectivity_mask,
):
    assert concept in {
        "captured",
        "dead",
        "bridge",
        "edge",
        "crescent",
        "span",
        "bottleneck",
        "escape",
        "trapezoid",
    }
    return templates.probing.get_templates(
        get_schemas(concept),
        templates_per_concept,
        neg_example,
        num_rand_to_add,
        conditions,
        selectivity_mask,
    )


def get_schemas(concept):
    return {
        "bridge": bridge(),
        "edge": edge(),
        "crescent": crescent(),
        "span": span(),
        "trapezoid": trapezoid(),
        "captured": captured(),
        "dead": dead(),
        "bottleneck": bottleneck(),
        "escape": escape(),
    }[concept]


from templates.strict_schemas.bridge import schemas as bridge_schemas_strict
from templates.strict_schemas.span import schemas as span_schemas_strict
from templates.strict_schemas.trapezoid import schemas as trapezoid_schemas_strict
from templates.strict_schemas.crescent import schemas as crescent_schemas_strict
from templates.strict_schemas.edge_a2 import schemas as edge_a2_schemas_strict
from templates.strict_schemas.edge_a3 import schemas as edge_a3_schemas_strict


def get_schemas_behavioral(concept):
    return {
        "bridge": bridge_schemas_strict(),
        "trapezoid": trapezoid_schemas_strict(),
        "span": span_schemas_strict(),
        "crescent": crescent_schemas_strict(),
        "edge": edge_a2_schemas_strict() + edge_a3_schemas_strict(),
        # Already strict.
        "bottleneck": bottleneck(),
        "escape": escape(),
    }[concept]


def bridge():
    return _bridge_schemas()


def bottleneck():
    return _bottleneck_schemas()


def crescent():
    return _crescent_schemas()


def edge():
    return _edge2_schemas() + _edge3_schemas()


def escape():
    return _escape_schemas()


def span():
    return _span_schemas()


def trapezoid():
    return _trapezoid_schemas()


# def captured():
#     schemas = []
#     for s in _captured_schemas():
#         for i, m in enumerate(s["avoid_defending"]):
#             new_schema = copy.deepcopy(s)
#             add_moves = [_m for _m in s["avoid_defending"] if _m != m]
#             new_schema["cells_attacking"].extend(add_moves)
#             new_schema["avoid_defending"] = [m]
#             new_schema["avoid_attacking"] = [m]
#             new_schema["concept"] = "dead"
#             new_schema["name"] = f"captured_{s['name']}-{i}"
#             schemas.append(new_schema)
#     schemas.extend(_deadcell_schemas())
#     return schemas
def captured():
    return _captured_schemas()


def dead():
    return _deadcell_schemas()
