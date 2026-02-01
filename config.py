import tomllib
from collections.abc import Iterable


def read_config(filepath) -> dict | None:
    try:
        with open(filepath, "rb") as f:
            config_dict = tomllib.load(f)
            if any(key not in config_dict.keys() for key in {"Minetest", "Directories", "ContentDB"}):
                return None
            if any(key not in config_dict["Minetest"].keys() for key in {"engine_location", "engine_version"}):
                return None
            if any(key not in config_dict["Directories"].keys() for key in {"mods", "textures", "games"}):
                return None
            if "api_url" not in config_dict["ContentDB"].keys():
                return None
            content_flags = config_dict["ContentDB"].get("content_flags", [])
            content_types = config_dict["ContentDB"].get("content_types", [])
            if isinstance(content_flags, Iterable) and not isinstance(content_flags, str):
                config_dict["ContentDB"]["content_flags"] = set(content_flags)
            else:
                config_dict["ContentDB"]["content_flags"] = {content_flags}
            if isinstance(content_types, Iterable) and not isinstance(content_types, str):
                config_dict["ContentDB"]["content_types"] = set(content_types)
            else:
                config_dict["ContentDB"]["content_types"] = {content_types}
            return config_dict
    except Exception:
        return None

def get_config(names: list) -> dict | None:
    for name in names:
        config_dict = read_config(name)
        if config_dict is not None:
            return config_dict
    return None