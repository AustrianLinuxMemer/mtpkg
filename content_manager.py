import os
from content import Mod, Modpack, Game, Textures
from version_txt import parse_version_txt
def parse_config_file(config_file_path) -> dict | None:
    try:
        with open(config_file_path, "r") as f:
            config = {}
            for line in f.readlines():
                if line.startswith("#"): continue # Ignore lines with comments
                if len(line.strip()) == 0: continue # Ignore empty/whitespace lines
                key, value = line.split('=', maxsplit=1)
                key, value = key.strip(), value.strip()
                config[key] = value
            return config
    except Exception:
        return None

def parse_mod(mod_root) -> Mod | None:
    config = parse_config_file(os.path.join(mod_root, 'mod.conf'))
    if config is None: return None
    if "optional_depends" in config:
        optional_depends = [d.strip() for d in config["optional_depends"].split(",")]
    else:
        optional_depends = None
    if "depends" in config:
        depends = [d.strip() for d in config["depends"].split(",")]
    else:
        depends = None
    return Mod(config.get("name", os.path.basename(mod_root)), config.get("version", None), depends, optional_depends)

def parse_modpack(modpack_root) -> Modpack | None:
    config = parse_config_file(os.path.join(modpack_root, 'modpack.conf'))
    if config is None: return None
    child_mods = []
    fs_list = os.listdir(modpack_root)
    fs_list.remove("modpack.conf")
    for item in fs_list:
        item_root = os.path.join(modpack_root, item)
        if os.path.isdir(item_root):
            mod_conf = os.path.join(item_root, 'mod.conf')
            modpack_conf = os.path.join(item_root, 'modpack.conf')
            if os.path.isfile(mod_conf):
                maybe_mod = parse_mod(item_root)
                if maybe_mod is not None: child_mods.append(item_root)
            elif os.path.isfile(modpack_conf):
                maybe_modpack = parse_modpack(item_root)
                if maybe_modpack is not None: child_mods.append(maybe_modpack)

    return Modpack(config.get("name", os.path.basename(modpack_root)), config.get("version", None), child_mods)

def parse_game(games_root) -> Game | None:
    game_conf = os.path.join(games_root, 'game.conf')
    config = parse_config_file(game_conf)
    if config is None: return None
    mod_list = []
    mod_folder = os.path.join(games_root, 'mods')
    for item in os.listdir(mod_folder):
        item_root = os.path.join(mod_folder, item)
        if os.path.isdir(item_root):
            mod_conf = os.path.join(item_root, 'mod.conf')
            modpack_conf = os.path.join(item_root, 'modpack.conf')
            if os.path.isfile(mod_conf):
                maybe_mod = parse_mod(item_root)
                if maybe_mod is not None: mod_list.append(maybe_mod)
            elif os.path.isfile(modpack_conf):
                maybe_modpack = parse_modpack(item_root)
                if maybe_modpack is not None: mod_list.append(maybe_modpack)
    return Game(config.get("name", os.path.basename(games_root)), config.get("version", None), mod_list)



def parse_texture_pack(tp_root) -> Textures | None:
    textures_conf = os.path.join(tp_root, 'texture_pack.conf')
    version_txt = os.path.join(tp_root, 'mtpkg_version.txt')
    config = parse_config_file(textures_conf)
    if config is None: return None
    return Textures(config.get("name", os.path.basename(tp_root)), parse_version_txt(version_txt))

def build_mod_tree(root_dir) -> list[Mod | Modpack]:
    mod_list = []
    for mod_dir in os.listdir(root_dir):
        mod_path = os.path.join(root_dir, mod_dir)
        if os.path.isdir(mod_path):
            mod_conf = os.path.join(mod_dir, 'mod.conf')
            modpack_conf = os.path.join(mod_dir, 'modpack.conf')
            if os.path.isfile(mod_conf):
                maybe_mod = parse_mod(mod_path)
                if maybe_mod is not None: mod_list.append(maybe_mod)
            elif os.path.isfile(modpack_conf):
                maybe_modpack = parse_modpack(mod_path)
                if maybe_modpack is not None: mod_list.append(maybe_modpack)
    return mod_list

def build_game_tree(root_dir) -> list[Game]:
    game_list = []
    for game_dir in os.listdir(root_dir):
        game_path = os.path.join(root_dir, game_dir)
        if os.path.isdir(game_path):
            game_conf = os.path.join(game_path, 'game.conf')
            if os.path.isfile(game_conf):
                maybe_game = parse_game(game_path)
                if maybe_game is not None: game_list.append(maybe_game)
    return game_list

def build_texture_pack_tree(root_dir) -> list[Textures]:
    tp_list = []
    for tp_dir in os.listdir(root_dir):
        tp_path = os.path.join(root_dir, tp_dir)
        if os.path.isdir(tp_path):
            texture_pack_conf = os.path.join(tp_path, 'texture_pack.conf')
            if os.path.isfile(texture_pack_conf):
                maybe_tp = parse_texture_pack(tp_path)
                if maybe_tp is not None: tp_list.append(maybe_tp)
    return tp_list

class ContentManager:
    def __init__(self, mods_path, games_path, textures_path):
        self.mods_path = mods_path
        self.games_path = games_path
        self.textures_path = textures_path

