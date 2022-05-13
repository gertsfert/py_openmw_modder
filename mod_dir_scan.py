from ast import Not
from pathlib import Path
from re import I
from typing import List
import random

# TODO: CONFIG FILE YO
MODS_PATH = Path("G:\Games\OpenMWMods")


PADDING_SCALE = 2
RESOURCE_FOLDER_NAMES = [
    "BookArt",
    "Fonts",
    "Icons",
    "Meshes",
    "Music",
    "Sound",
    "Splash",
    "Textures",
    "Video",
    "Font",  # TODO: Lookup how fonts are added - not a defualt folder
]


def is_valid_dir(dir: Path) -> bool:
    return dir.exists() and dir.is_dir()


class ModFile:
    def __init__(self, path):
        self.path = path
        self.name = path.stem

    def __str__(self):
        return self.name


class ModDir:
    def __init__(self, path: Path, parent=None):
        self.path = path
        self.name = path.stem
        # self.to_activate = False

        # TODO - this is for testing the display of activated folders
        self.to_activate = bool(random.getrandbits(1))
        self.parent = parent

        self.data_folders = None

    def get_data_folders(self):
        if self.data_folders is None:
            data_folders = self.find_data_folders()
            if isinstance(data_folders, ModDir):
                self.data_folders = [data_folders]
            else:
                self.data_folders = data_folders

        return self.data_folders

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return f"ModDir[{self.path}]"

    @property
    def resource_dirs(self) -> List:

        resource_dir_options = [
            self.path / resource for resource in RESOURCE_FOLDER_NAMES
        ]

        return [
            ModDir(resource_dir)
            for resource_dir in resource_dir_options
            if is_valid_dir(resource_dir)
        ]

    @property
    def has_resources(self) -> bool:
        return len(self.resource_dirs) > 0

    def filetypes_in_dir(self, filetype: str) -> List[Path]:
        return list(self.path.glob(f'*.{filetype.lstrip(".")}'))

    @property
    def esp_files(self):
        return self.filetypes_in_dir("esp")

    @property
    def has_esp(self):
        return len(self.esp_files) > 0

    @property
    def bsa_files(self):
        return self.filetypes_in_dir("bsa")

    @property
    def has_bsa(self):
        return len(self.bsa_files) > 0

    @property
    def is_data_folder(self) -> bool:
        """Returns true if dir is a top-level directory
        for a mod (i.e. contains .esp, .bsa, or resource
        sub-directories"""

        return self.has_esp or self.has_bsa or self.has_resources

    def find_data_folders(self) -> List:
        if self.is_data_folder:
            return self

        sub_dirs = [
            ModDir(sub_dir, parent=self)
            for sub_dir in self.path.glob("*")
            if sub_dir.is_dir()
        ]

        data_folders_list = list(
            filter(
                lambda x: x is not None,
                [sub_dir.find_data_folders() for sub_dir in sub_dirs],
            )
        )

        if len(data_folders_list) == 0:
            return None

        return data_folders_list

    def print_mod_contents(self) -> None:
        if self.has_esp:
            print_indent_title("ESPs", indent_level=1)
            for esp in self.esp_files:
                print_indent_item(esp, indent_level=2)

        if self.has_bsa:
            print_indent_title("BSAs", indent_level=1)
            for bsa in self.bsa_files:
                print_indent_item(bsa, indent_level=2)

        if self.has_resources:
            print_indent_title("Resources", indent_level=1)
            for resource in self.resource_dirs:
                print_indent_item(resource, indent_level=2)

    def ask_to_activate(self):
        """Presents the directory mod contents, and asks the user if the
        dir should be activated"""

        print(f" Contents:")
        self.print_mod_contents()

        choice = None
        while choice is None:
            answer = input(f"Activate {self}? (y/n):").lower().strip()
            if answer == "n":
                choice = False
            elif answer == "y":
                choice = True
            else:
                print("invalid answer")

        self.to_activate = choice

    def ask_to_activate_children(self):
        for data_folder in self.get_data_folders():
            print(data_folder)
            data_folder.ask_to_activate()

    def ask_to_activate_self_or_children(self):
        if self.is_data_folder:
            self.ask_to_activate()
        else:
            print(f"Contains {len(self.get_data_folders())} datafolders: ", end="")
            print("| ".join([df.__str__() for df in self.get_data_folders()]))

            self.ask_to_activate_children()

    def get_folder_to_activate(self) -> List:
        if self.is_data_folder:
            if self.to_activate:
                return [self]
            else:
                return []
        else:
            return [
                data_folder
                for data_folder in self.get_data_folders()
                if data_folder.is_data_folder and data_folder.to_activate
            ]


def print_indent_title(item, indent_level: int = 0):
    spacing = " " * (indent_level * PADDING_SCALE)
    print(f"{spacing} ┖ {item}")


def print_indent_item(item, indent_level: int = 0):
    spacing = " " * (indent_level * PADDING_SCALE)
    print(f"{spacing} - {item}")


class ParentModDir(ModDir):
    def print_data_folders(self):
        for data_folder in self.get_data_folders():
            print(f" {data_folder}")

            data_folder.print_mod_contents()


def get_folders_to_activate(parent_mod_dirs: List[ModDir]):
    for parent_mod_dir in parent_mod_dirs:
        print("-" * 80)
        print(parent_mod_dir)
        # parent_mod_dir.print_data_folders()
        parent_mod_dir.ask_to_activate_self_or_children()


def print_folders_to_activate(parent_mod_dirs: List[ModDir]):
    print("printing folders to activate:")
    for parent_mod_dir in parent_mod_dirs:
        last_parent_name = None
        if parent_mod_dir.to_activate and parent_mod_dir.is_data_folder:
            print_indent_title(parent_mod_dir)

        else:
            for to_activate in parent_mod_dir.get_folder_to_activate():
                if to_activate.parent:
                    if to_activate.parent.name != last_parent_name:
                        print_indent_title(to_activate.parent)
                        last_parent_name = to_activate.parent.name
                    print_indent_item(to_activate, indent_level=1)
                else:
                    print_indent_item(to_activate, indent_level=0)


if __name__ == "__main__":
    parent_mod_dirs = [ParentModDir(d) for d in MODS_PATH.iterdir() if d.is_dir()]

    print_folders_to_activate(parent_mod_dirs)
