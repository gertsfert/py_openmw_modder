from dataclasses import dataclass
from typing import Dict, List
import yaml
from pathlib import Path
from datetime import date

SETTINGS_PATH = Path(__file__).parent / "app_settings.yaml"


def print_recurse_dict(d: dict | str, indent_value: int = 0):
    indents = "  " * indent_value
    if isinstance(d, Dict):
        for k, v in d.items():
            print(f"{indents}{k}:")
            print_recurse_dict(v, indent_value=indent_value + 1)
    elif isinstance(d, List):
        for x in d:
            print(indents, x)

    else:
        print(indents, d)


@dataclass
class CoreAppSettings:
    mods_path: List[Path]
    open_mw_conf_path: Path

    def __init__(self, core_dict: Dict):
        self.mods_path = [Path(p) for p in core_dict["mods_path"]]
        self.open_mw_conf_path = Path(core_dict["open_mw_conf_path"])


@dataclass
class ParsingAppSettings:
    resource_dir_names: List[str]
    max_date_folder_timestamp: date
    min_date_folder_timestamp: date

    def __init__(self, parsing_dict: Dict):
        self.resource_dir_names = parsing_dict["resource_dir_names"]
        self.max_date_folder_timestamp = parsing_dict["max_date_folder_timestamp"]
        self.min_date_folder_timestamp = parsing_dict["min_date_folder_timestamp"]


class AppSettings:
    settings_path: Path
    core: CoreAppSettings
    parsing: ParsingAppSettings

    def __init__(self):
        self.settings_path = SETTINGS_PATH

        self._settings_dict = self.read_settings_file()
        self.core = CoreAppSettings(self._settings_dict["core"])
        self.parsing = ParsingAppSettings(self._settings_dict["parsing"])

    def read_settings_file(self) -> Dict:
        """Reads the file at settings_path, and returns the
        parsed settings as a dict"""
        with open(self.settings_path) as settings_file:
            return yaml.safe_load(settings_file)

    def display_settings_file(self) -> Dict:
        print_recurse_dict(self._settings_dict)


if __name__ == "__main__":
    settings = AppSettings()
    settings.display_settings_file()
