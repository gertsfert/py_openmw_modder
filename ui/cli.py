from mod_resources import ModDataDir, Mod, ModsFolder
from .base import UI

PADDING_SCALE = 2


class CLI(UI):
    @staticmethod
    def display_title(item, indent_level: int = 0):
        spacing = " " * (indent_level * PADDING_SCALE)
        print(f"{spacing} ┖ {item}")

    @staticmethod
    def display_item(item, indent_level: int = 0):
        spacing = " " * (indent_level * PADDING_SCALE)
        print(f"{spacing} - {item}")

    def display_data_dir_contents(self, data_dir: ModDataDir) -> None:
        if data_dir.has_esp:
            self.display_title("ESPs", indent_level=1)
            for esp in data_dir.esp_files:
                self.display_item(esp, indent_level=2)

        if data_dir.has_bsa:
            self.display_title("BSAs", indent_level=1)
            for bsa in data_dir.bsa_files:
                self.display_item(bsa, indent_level=2)

        if data_dir.has_resource_dirs:
            self.display_title("Resources", indent_level=1)
            for resource in data_dir.resource_dirs:
                self.display_item(resource, indent_level=2)

    def display_mod_contents(self, mod: Mod) -> None:
        for data_dir in mod.data_dirs:
            if data_dir is not mod:
                self.display_title(data_dir)
            self.display_data_dir_contents(data_dir)

    def display_mod_metadata(self, mod: Mod):
        meta = mod.metadata
        self.display_title(meta.title)
        if meta.variant:
            self.display_item(f"variant: {meta.variant}", indent_level=1)

        self.display_item(f"version: {meta.version}", indent_level=1)
        self.display_item(f"modified: {meta.modified_time}", indent_level=1)

    def ask_to_activate(self) -> bool:
        """Presents the directory mod contents, and asks the user if the
        dir should be activated"""

        print(f" Contents:")
        self.display_mod_contents()

        choice = None
        while choice is None:
            answer = input(f"Activate {self}? (y/n):").lower().strip()
            if answer == "n":
                choice = False
            elif answer == "y":
                choice = True
            else:
                print("invalid answer")

        return choice
