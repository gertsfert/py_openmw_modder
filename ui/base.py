from abc import ABC, abstractmethod
from mod_resources import ModDataDir, ParentModDir


class UI(ABC):
    @abstractmethod
    def display_data_dir_contents(self, data_dir: ModDataDir) -> None:
        ...

    @abstractmethod
    def display_mod_contents(self, mod: ParentModDir) -> None:
        ...

    @abstractmethod
    def ask_to_activate(self, mod: ParentModDir) -> bool:
        ...
