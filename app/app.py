from app.mod_resources import ModsFolder
from app.ui.cli import CLI

from app.app_settings import AppSettings

settings = AppSettings()

if __name__ == "__main__":
    # TODO: allow parsing of multiple mods folders
    mod_collection = ModsFolder(settings.core.mods_path[0])

    ui = CLI()

    for mod in mod_collection.mods:
        mod.get_data_dirs()
        ui.display_title(mod)
        ui.display_mod_metadata(mod)
        # ui.display_mod_contents(mod)
