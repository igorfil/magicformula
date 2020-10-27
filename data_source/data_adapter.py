def pick_keys(source_dict: dict, key_mapping: dict) -> dict:
    if source_dict is None:
        source_dict = {}
    return { target_key: source_dict.get(source_key, "") for source_key, target_key in key_mapping.items() }