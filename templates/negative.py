import templates.templates


def get_templates(schemas, templates_per_concept: int, num_rand_to_add: int = 0):
    """Returns templates used for the negative behavioral test."""
    return templates.templates.get_templates_generic(
        schemas,
        templates_per_concept,
        num_rand_to_add,
        [{"connect": False, "owner_to_play": False, "intrude": False}],
        templates.templates.generate_templates,
        generate_kwargs=dict(),
    )
