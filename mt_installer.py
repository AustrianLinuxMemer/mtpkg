import argparse
import os
import shutil
import subprocess
import re
import sys
import tomllib
from collections.abc import Iterable

version_search_regex = re.compile(r"(\d+\.\d+\.\d+)")
def get_version(executable: str) -> str | None:
    result = subprocess.run([executable, "--version"], capture_output=True, text=True, check=False)
    output = result.stdout or result.stderr
    matches = re.search(version_search_regex, output)
    if matches:
        version = matches.group(1)
        return version
    else:
        return None


def probe_engine(config_path: str | None=None, cli_path: str | None=None) -> tuple[str, str] | None:
    luanti_exec = shutil.which("luanti")
    minetest_exec = shutil.which("minetest")
    if cli_path is not None and os.path.exists(cli_path):
        return get_version(cli_path), cli_path
    if config_path is not None and os.path.exists(config_path):
        return get_version(config_path), config_path
    if luanti_exec is not None:
        return get_version(luanti_exec), luanti_exec
    if minetest_exec is not None:
        return get_version(minetest_exec), minetest_exec
    return None

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


arg_parser = argparse.ArgumentParser()
subparsers = arg_parser.add_subparsers(dest="command", required=False, help="Command to run")
install_parser = subparsers.add_parser("install", help="Install a package")
install_parser.add_argument("package_name", help="Name of the package to install", nargs="+", type=str)

uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall a package")
uninstall_parser.add_argument("package_name", help="Name of the package to uninstall", nargs="+", type=str)

update_parser = subparsers.add_parser("update", help="Update one, more or all packages")
update_parser.add_argument("package_name", help="Name of the package to update", nargs="*", type=str)

search_parser = subparsers.add_parser("search", help="Search packages")
search_parser.add_argument("query", help="Things to search for", type=str)

arg_parser.add_argument("--detect-engine", help="Detect the engine/protocol version", nargs="?", const=True)
arg_parser.add_argument("--hide-content", help="Hide these types of contents", choices=["mod", "game", "txp"], nargs="+")
arg_parser.add_argument("--ignore_content_flags", help="Ignore these content flags", nargs="+")
arg_parser.add_argument("--config", help="Path to config file", nargs="?")
args = arg_parser.parse_args()


possible_config_files = [
    "/etc/mtpkg/mtpkg.toml",
    os.path.expanduser("~/.mtpkg/mtpkg.toml"),
]
if isinstance(args.config, str):
    possible_config_files.append(os.path.expanduser(args.config))


config = get_config(possible_config_files)
if config is None:
    print("None of the config files were valid")
    print(possible_config_files)
    sys.exit(1)


if args.detect_engine:
    if isinstance(args.detect_engine, str):
        print("Detected engine (cli path):", probe_engine(cli_path=args.detect_engine))
    else:
        print("Detected engine (no cli path):", probe_engine())
    sys.exit(0)

