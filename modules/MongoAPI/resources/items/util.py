def normalize_fields(
        name=None,
        tier=None,
        rank=None,
        buildsFrom=None,
        buildsInto=None,
        specialRecipe=0,
        noEffects=True,
        removed=False,
        requiredChampion="",
        requiredAlly="",
        simpleDescription=None,
        nicknames=None,
        passives=None,
        active=None,
        stats=None,
        shop=None
):
    """
    This method is for the normalize fields of items resource.
    Args:
        name: string
        tier: int
        rank: array
        buildsFrom: array
        buildsInto: array
        specialRecipe: int
        noEffects: bool
        removed: bool
        requiredChampion: string
        requiredAlly: string
        simpleDescription: string
        nicknames: array
        passives: array
        active: array
        stats: dict
        shop: dict

    Returns:
        all params
    """
    if rank is None:
        rank = []
    if stats is None:
        stats = dict()
    if shop is None:
        shop = dict()
    if active is None:
        active = []
    if passives is None:
        passives = []
    if nicknames is None:
        nicknames = []
    if buildsInto is None:
        buildsInto = []
    if buildsFrom is None:
        buildsFrom = []

    return {
        'name': name.capitalize(),
        'tier': tier,
        'rank': rank,
        'buildsFrom': buildsFrom,
        'buildsInto': buildsInto,
        'specialRecipe': specialRecipe,
        'noEffects': noEffects,
        'removed': removed,
        'requiredChampion': requiredChampion,
        'requiredAlly': requiredAlly,
        'simpleDescription': simpleDescription,
        'nicknames': nicknames,
        'passives': passives,
        'active': active,
        'stats': stats,
        'shop': shop
    }


def validate_dict(value):
    """
    This method is necessary for reparse.add_argument to verify if field is a dictionary.
    Args:
        value:

    Returns:
        value: dict
    """
    print(type(value))
    print(value)
    if not isinstance(value, dict):
        raise ValueError(f"Invalid value '{value}'. Value must be a dictionary.")
    return value
