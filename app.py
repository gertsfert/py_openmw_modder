from mod_resources import ModCollectionDir
from ui.cli_ui import CLI

import settings

if __name__ == "__main__":
    mod_collection = ModCollectionDir(settings.MODS_PATH)

    ui = CLI()

    for mod in mod_collection.mods:
        ui.display_title(mod)
        ui.display_mod_contents(mod)
