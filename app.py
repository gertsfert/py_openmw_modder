from mod_resources import ModsFolder
from ui.cli import CLI

import settings

if __name__ == "__main__":
    mod_collection = ModsFolder(settings.MODS_PATH)

    ui = CLI()

    for mod in mod_collection.mods:
        ui.display_title(mod)
        ui.display_mod_metadata(mod)
        # ui.display_mod_contents(mod)
