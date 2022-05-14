from pathlib import Path
from typing import List, Callable

from settings import MODS_PATH, RESOURCE_DIR_NAMES


def is_valid_dir(dir: Path) -> bool:
    return dir.exists() and dir.is_dir()


class ModResource:
    """Generic class to hold any mod resource (file or directory)"""

    def __init__(self, path: Path, parent):
        self.path = path
        self.name = path.stem
        self.parent = parent

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ModResource[{self.parent}: {self}]"


class ModFile(ModResource):
    def __repr__(self):
        return f"ModFile[{self.parent}: {self}]"


class ESPFile(ModFile):
    def __repr__(self):
        return f"ESPFile[{self.parent}: {self}]"


class BSAFile(ModFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_active = None

    def __repr__(self):
        return f"BSAFile[{self.parent}: {self}]"

    def set_active(self, is_active: bool = True):
        self.is_active = is_active


class ModDir(ModResource):
    """A folder that is part of a mod structure"""

    def __init__(
        self,
        *args,
        child_factory: Callable = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.child_factory = child_factory
        self.children = self.get_children()

    def __repr__(self):
        return f"ModDir[{self.parent}: {self}]"

    def init_child(self, child_path: Path) -> ModResource:
        return self.child_factory(path=child_path, parent=self)

    def get_children(self) -> List[ModResource]:
        children = [self.init_child(child) for child in self.path.iterdir()]

        # wont list unclassified children
        return [child for child in children if child is not None]

    def get_children_of_type(self, object) -> List[ModResource]:
        return [child for child in self.children if type(child) is object]

    def has_child_of_type(self, object) -> bool:
        return len(self.get_children_of_type(object)) > 0

    def get_children_of_instance(self, object) -> List[ModResource]:
        return [child for child in self.children if isinstance(child, object)]

    def has_child_of_instance(self, object) -> bool:
        return len(self.get_children_of_instance(object)) > 0

    def search_children(
        self, condition: Callable, only_of_instance: object = None
    ) -> List[ModResource]:

        if only_of_instance is not None:
            valid_children = self.get_children_of_instance(only_of_instance)

        else:
            valid_children = self.children

        if len(valid_children) == 0:
            # no more children, so no possible serach results, terminate result
            return [None]

        return [child for child in valid_children if condition(child)]

    def recurse_search_children(
        self, condition: Callable, only_of_instance=None
    ) -> List[ModResource]:
        """Recursively search though children (and children of children etc...)
        for children that meet the input 'condition'.

        Optional: Limit search to only those of a instance using only_of_instnace"""

        if only_of_instance is not None:
            children = self.get_children_of_instance(only_of_instance)

        else:
            children = self.children

        if len(children) == 0:
            # no more children, so no possible search results, terminate result
            return None

        # check if any direct children meets condition
        search_results = [child for child in children if condition(child)]

        if len(search_results) > 0:
            # if we've found results - terminate search here and return results
            return search_results

        # otherwise, if we havent found results - perform search in all child directories
        child_dirs = self.get_children_of_instance(ModDir)

        if len(child_dirs) == 0:
            return None

        # iterate through child directories, performing same search
        recurse_results = [
            child_dir.recurse_search_children(condition, only_of_instance)
            for child_dir in child_dirs
        ]

        recurse_results = [
            child_dir for child_dir in recurse_results if child_dir is not None
        ]

        # unpacking result list
        return [result for results in recurse_results for result in results]


class ModSpecialDir(ModDir):
    def __init__(self, *args, **kwargs):
        if isinstance(args[0], ModDir):
            self.from_mod_dir(args[0])

        elif isinstance(args[0], Path):
            self.from_path(*args, **kwargs)

    def from_mod_dir(self, mod_dir: ModDir):
        self.path = mod_dir.path
        self.name = mod_dir.name
        self.parent = mod_dir.parent
        self.child_factory = mod_dir.child_factory
        self.children = mod_dir.children

    def from_path(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ModResourceDir(ModSpecialDir):
    def __repr__(self):
        return f"ModResourceDir[{self.parent}: {self}]"

    @staticmethod
    def is_mod_resource_dir(mod_dir: ModDir) -> bool:
        return mod_dir.name.lower() in RESOURCE_DIR_NAMES


class ModDataDir(ModSpecialDir):
    """A 'Data Directory' - will have core mod files (ESP/BSA)
    or 'resource folders' at top-level.

    Some mods will have multiple Data Directories in a given mod, this
    is usually to :
      - provide customisation (i.e. installing different sets of
        spell effects)
      - or add compatibility layers (i.e. install this data dir if
        you also X mod)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.to_activate = False

        self._esp_files = None
        self._bsa_files = None
        self._resource_dirs = None

    def __repr__(self):
        return f"ModDataDir[{self.parent}: {self}]"

    @staticmethod
    def is_mod_data_dir(mod_dir: ModDir) -> bool:
        return (
            mod_dir.has_child_of_instance(BSAFile)
            or mod_dir.has_child_of_instance(ESPFile)
            or mod_dir.has_child_of_instance(ModResourceDir)
        )

    @property
    def esp_files(self):
        if self._esp_files is None:
            self._esp_files = self.get_children_of_type(ESPFile)

        return self._esp_files

    @property
    def has_esp(self):
        return len(self.esp_files) > 0

    @property
    def bsa_files(self):
        if self._bsa_files is None:
            self._bsa_files = self.get_children_of_type(BSAFile)

        return self._bsa_files

    @property
    def has_bsa(self):
        return len(self.bsa_files) > 0

    @property
    def resource_dirs(self) -> List:
        if self._resource_dirs is None:
            self._resource_dirs = self.search_children(
                condition=ModResourceDir.is_mod_resource_dir,
                only_of_instance=ModDir,
            )
        return self._resource_dirs

    @property
    def has_resource_dirs(self) -> bool:
        return len(self.resource_dirs) > 0


def mod_resource_factory(path: Path = None, **kwargs) -> ModResource:
    """Takes an input path, and returns  an instantiation of ModResource
    subclass depending on the path characteristics."""
    if path is None:
        raise TypeError("mod_resource_factory requires a path")

    if path.is_file():
        file_type = path.suffix.lower()

        if file_type == ".bsa":
            return BSAFile(path, **kwargs)

        elif file_type == ".esp":
            return ESPFile(path, **kwargs)

        else:
            return ModFile(path, **kwargs)

    elif path.is_dir():
        mod_dir = ModDir(path, child_factory=mod_resource_factory, **kwargs)

        # check if dir should be promoted? the constructors feel a little gross

        if ModDataDir.is_mod_data_dir(mod_dir):
            return ModDataDir(mod_dir)
        elif ModResourceDir.is_mod_resource_dir(mod_dir):
            return ModResourceDir(mod_dir)
        else:
            return mod_dir


class ParentModDir(ModDataDir):
    """A directory found in the MODS_DIR set in the config file"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data_dirs = self.get_data_dirs()

    def __repr__(self):
        return f"ParentModDir[{self}]"

    def get_data_dirs(self) -> List[ModDataDir]:
        if ModDataDir.is_mod_data_dir(self):
            return [self]

        else:
            return self.recurse_search_children(
                condition=ModDataDir.is_mod_data_dir, only_of_instance=ModDir
            )


class ModCollectionDir(ModDir):
    """Top-level directory where mods directories are saved/unzipped into."""

    def __init__(self, path: Path):
        self.path = path
        self.name = path.stem

        self.mods = self.get_mods()

    def __repr__(self):
        return f"ModCollectionDir[{self}]"

    def get_mods(self) -> List[ParentModDir]:
        return [
            ParentModDir(dir, parent=self.name, child_factory=mod_resource_factory)
            for dir in self.path.iterdir()
            if dir.is_dir()
        ]


if __name__ == "__main__":
    from settings import MODS_PATH

    print(f"scanning path {MODS_PATH} for Morrowind Mod Resources")
    mod_dir = ModCollectionDir(MODS_PATH)

    print(
        f"finished scanning directory - printing parent mod dirs and their child data folders"
    )
    for parent_mod_dir in mod_dir.children:
        print(parent_mod_dir)
        for data_dir in parent_mod_dir.data_dirs:
            print(f"\t{data_dir}")
        print()
