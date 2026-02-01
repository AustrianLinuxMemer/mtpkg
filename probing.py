import os
import re
import shutil
import subprocess

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