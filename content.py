class Content:
    def __init__(self, name: str, version: str | None):
        self.name = name
        self.version = version
    def is_untracked(self): return self.version is None

class Provides(Content):
    def __init__(self, provides: list[str], name: str, version: str | None):
        super().__init__(name, version)
        self.provides = provides

class Mod(Provides):
    def __init__(self, name: str, version: str | None, depends: list[str] | None, optional_depends: list[str] | None):
        super().__init__([name], name, version)
        self.depends = depends if depends is not None else []
        self.optional_depends = optional_depends if optional_depends is not None else []

class Modpack(Provides):
    def __init__(self, name: str, version: str | None, mod_list: list[Mod | "Modpack"]):
        all_provides = []
        for item in mod_list:
            all_provides.extend(item.provides)
        super().__init__(all_provides, name, version)

class Game(Provides):
    def __init__(self, name: str, version: str | None, mods: list[Mod | Modpack]):
        all_provides = []
        for item in mods:
            all_provides.extend(item.provides)
        super().__init__(all_provides, name, version)

class Textures(Content):
    def __init__(self, name: str, version: str | None):
        super().__init__(name, version)