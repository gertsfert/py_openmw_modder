from functools import total_ordering
from pathlib import Path
from typing import Tuple
from enum import Enum
import click

from py_openmw_modder.app_settings import AppSettings

settings = AppSettings()


class ColourComponentType(Enum):
    RED = "r"
    GREEN = "g"
    BLUE = "b"


class ColourComponent:
    def __init__(self, component_type: ColourComponentType, value: int):
        self.component_type = component_type
        self.value = value

    def __str__(self):
        return str(self.value).zfill(3)

    def __repr__(self):
        return f"ColourComponent[{self.component_type}: {self.value}]"


class Value:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class ColourValue(Value):
    def __init__(
        self, red: ColourComponent, green: ColourComponent, blue: ColourComponent
    ):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return f"{self.red},{self.green},{self.blue}"

    def __repr__(self):
        return f"ColourValue[red={self.red}, green={self.green}, blue={self.blue}]"


class BoolValue(Value):
    def __str__(self):
        return str(int(self.value))

    def __repr__(self):
        return f"BoolValue[{self.value}]"


@total_ordering
class Option:
    def __init__(self, order: int, name: str, value: Value):
        self.order = order
        self.name = name
        self.value = value

    def __gt__(self, other):
        return self.order > other.order

    def __eq__(self, other):
        return self.order == other.order

    def __repr__(self):
        return f"Option[{self.name}: {self.value}]"

    def __str__(self):
        return f"{self.name}={self.value}"


class FallbackOption(Option):
    def __repr__(self):
        return f"FallbackOption[{self.name}: {self.value}]"

    def __str__(self):
        return f"fallback={self.name},{self.value}"


class DataOption(Option):
    def __init__(self, order, name, value: Path):
        self.order = order
        self.name = name
        self.value = value

    def path_exists(self):
        return self.value.exists()


def detect_fallback_type(value_segment: str) -> object:
    if len(value_segment) == 3:
        return ColourValue

    elif value_segment in ["0", "1"]:
        return BoolValue

    else:
        return Value


def parse_fallback_line(fallback_segment: str) -> Tuple[str, Value]:
    parsed = fallback_segment.split(",")
    name = parsed[0]
    value_segment = parsed[1:]

    value_type = detect_fallback_type(value_segment)

    if value_type is ColourValue:
        value = ColourValue(*value_segment)

    else:
        value = Value("".join(value_segment))

    return (name, value)


def parse_cfg_line(line_number: int, line: str):
    # TODO: deal with empty lines!

    parsed = line.split("=")
    if len(parsed) > 2:
        raise ValueError(
            f"Error reading line - \
more than 1 '=' character found: {line}"
        )

    if len(parsed) == 1:
        raise ValueError(
            f"Error reading line - \
no '=' character found: {line}"
        )

    if parsed[0] == "fallback":
        name, value = parse_fallback_line(parsed[1])
        return FallbackOption(line_number, name, value)

    else:
        name, value = parsed[0], Value(parsed[1])
        return Option(line_number, name, value)


def read_cfg(cfg_path: Path) -> dict:
    """Reads a open MW config file and returns
    all values as a dictionary"""

    with open(cfg_path, "r") as cfg_file:
        parsed = [
            parsed_line
            for parsed_line in map(
                lambda x: parse_cfg_line(*x),
                [
                    (line_number, line.strip())
                    for (line_number, line) in enumerate(cfg_file.readlines())
                ],
            )
        ]

    for p in parsed:
        print(p)


@click.command()
def cli():
    """Automatic datafiles?!"""
    print("oh hi there")


read_cfg(settings.core.open_mw_conf_path)


if __name__ == "__main__":
    cli()
