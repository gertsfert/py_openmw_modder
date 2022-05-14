from typing import List

import edifice as ed
from mod_resources import ParentModDir, ModDir

from settings import MODS_PATH


class FolderWidget(ed.Component):
    @ed.register_props
    def __init__(self, mod_dir: ModDir):
        self.mod_dir = ModDir
        self.name = mod_dir.name
        self.path = mod_dir.path

    def render(self):
        return ed.View(layout="row")(ed.Label(self.name))


class MWModHelper(ed.Component):
    def __init__(self, **kwargs):
        super(MWModHelper, self).__init__(**kwargs)

        self.parent_mod_dirs = self.get_parent_mod_dirs()
        self.parent_mod_widgets = [
            FolderWidget(mod_dir) for mod_dir in self.parent_mod_dirs
        ]

    def get_parent_mod_dirs(self) -> List[ParentModDir]:
        return [ParentModDir(d) for d in MODS_PATH.iterdir() if d.is_dir()]

    def render(self):
        return ed.View(layout="column")(*self.parent_mod_widgets)


if __name__ == "__main__":
    ed.App(MWModHelper()).start()
