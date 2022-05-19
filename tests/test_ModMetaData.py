from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
import pytest
from datetime import datetime

from py_openmw_modder.mod_resources import ModMetaData, ModsFolder


@dataclass
class Case:
    mod_dir_name: str
    mod_metadata: Dict[str, Any]

    def __str__(self):
        return (
            f"""mod_dir_name: {self.mod_dir_name}\nmod_metadata: {self.mod_metadata}"""
        )

    def __repr__(self):
        return self.__str__()


cases = [
    Case(
        mod_dir_name="Expansion Delay-47588-1-3-1612481103",
        mod_metadata={
            "title": "Expansion Delay",
            "id": 47588,
            "version": "1.3",
            "posted_time": datetime.fromtimestamp(1612481103),
        },
    ),
    Case(
        mod_dir_name="Fonts-46854-1-0-1559397215",
        mod_metadata={
            "title": "Fonts",
            "id": 46854,
            "version": "1.0",
            "posted_time": datetime.fromtimestamp(1559397215),
        },
    ),
    Case(
        mod_dir_name="Morrowind Optimization Patch-45384-14-1648563790",
        mod_metadata={
            "title": "Morrowind Optimization Patch",
            "id": 45384,
            "version": "14",
            "posted_time": datetime.fromtimestamp(1648563790),
        },
    ),
    Case(
        mod_dir_name="Patch for Purists-45096-4-0-2-1593803721",
        mod_metadata={
            "title": "Patch for Purists",
            "id": 45096,
            "version": "4.0.2",
            "posted_time": datetime.fromtimestamp(1593803721),
        },
    ),
    Case(
        mod_dir_name="Pickpocket_Fix_v101",
        mod_metadata={"title": "Pickpocket Fix", "version": "v101"},
    ),
    Case(
        mod_dir_name="Tamriel_Data_v8 - HD",
        mod_metadata={"title": "Tamriel Data", "variant": "HD", "version": "v8"},
    ),
    Case(
        mod_dir_name="TamrielRebuilt_21-01-01",
        mod_metadata={"title": "Tamriel Rebuilt", "version": "21.01.01"},
    ),
    Case(
        mod_dir_name="TamrielRebuilt_21-01",
        mod_metadata={"title": "Tamriel Rebuilt", "version": "21.01"},
    ),
]


@dataclass
class SimpleMod:
    name: str
    path: Path


@pytest.fixture(scope="function")
def mods_folder(tmp_path: Path) -> ModsFolder:
    tmp_mod_parent_dir = tmp_path / "tmp_mods"
    tmp_mod_parent_dir.mkdir()
    return ModsFolder(tmp_mod_parent_dir)


def create_temp_mod_dir(mfolder: ModsFolder, mod_dir_name) -> Path:
    tmp = mfolder.path / mod_dir_name
    tmp.mkdir()
    return tmp


@pytest.mark.parametrize("test_case", cases)
def test_name_parsing(test_case: Case, mods_folder: ModsFolder):
    mod_dir = create_temp_mod_dir(mods_folder, test_case.mod_dir_name)
    mod = SimpleMod(name=test_case.mod_dir_name, path=mod_dir)
    expected = test_case.mod_metadata

    meta = ModMetaData(mod)

    for k, v in expected.items():
        assert hasattr(meta, k)
        assert meta.__getattribute__(k) == v
