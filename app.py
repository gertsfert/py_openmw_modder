from mod_resources import ModsFolder
from ui.cli import CLI

from app_settings import AppSettings

settings = AppSettings()

if __name__ == "__main__":
    # TODO: allow parsing of multiple mods folders
    mod_collection = ModsFolder(settings.core.mods_path[0])

    ui = CLI()

    for mod in mod_collection.mods:
        ui.display_title(mod)
        ui.display_mod_metadata(mod)
        # ui.display_mod_contents(mod)
