from content import Textures


def parse_version_txt(version_txt: str) -> str | None:
    try:
        with open(version_txt, "r") as f:
            return f.read().strip()
    except Exception:
        return None

def write_version_txt(version_txt: str, version: str):
    with open(version_txt, "w") as f:
        f.write(version)