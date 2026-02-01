class Provides:
    def __init__(self, provides: list[str]):
        self.provides = provides

class Mod(Provides):
    def __init__(self, name: str, version: str, depends: list[str], optional_depends: list[str]):
        super().__init__([name])
        self.name = name
        self.version = version
        self.depends = depends
        self.optional_depends = optional_depends

class Modpack(Provides):
    def __init__(self, name: str, version: str, mod_list: list[Mod | "Modpack"]):
        all_provides = []
        for item in mod_list:
            all_provides.extend(item.provides)
        super().__init__(all_provides)
        self.name = name
        self.version = version

class Game(Provides):
    def __init__(self, name: str, version: str, mods: list[Mod | Modpack]):
        all_provides = []
        for item in mods:
            all_provides.extend(item.provides)
        super().__init__(all_provides)
        self.name = name
        self.version = version

class Textures:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version