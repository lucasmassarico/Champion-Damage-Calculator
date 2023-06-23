def normalize_fields(
        name=None,
        is_keystone=False,
        is_shard=False,
        description=None,
        tree_path=None,
        tier=0,
        version=None,
):
    """
    This method is for the normalize fields of items resource.
    Args:
        name: string
        is_keystone: bool
        is_shard: bool
        description: str
        tree_path: str
        tier: int
        version: str
    Returns:
        all params
    """
    return {
        'name': name.capitalize(),
        'is_keystone': is_keystone,
        'is_shard': is_shard,
        'description': description,
        'tree_path': tree_path,
        'tier': tier,
        'version': version,
    }
