import edifice as ed
from edifice import Label, TextInput, View

STYLES = {
    "from_unit_label": {"width": 170},
    "to_unit_label": {"margin-left": 20, "width": 200},
    "input_style": {"padding": 2, "width": 120},
}

METERS_TO_FEET = 3.28084


def str_to_float(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        return 0.0


def float_to_str(flt: float) -> str:
    try:
        return f"{flt:.3f}"
    except ValueError:
        return ""


class ConversionWidget(ed.Component):
    @ed.register_props
    def __init__(self, from_unit: str, to_unit: str, factor: float):
        super().__init__()
        self.to_unit = to_unit
        self.from_unit = from_unit
        self.factor = factor

        self.text_str = ""
        self.from_value = 0.0

    def on_text_change(self, text: str):
        self.set_state(text_str=text)
        self.set_state(from_value=str_to_float(text))

    def render(self):
        to_value = self.from_value * self.factor

        return View(layout="row")(
            Label(f"Measurement in {self.from_unit}:", style=STYLES["from_unit_label"]),
            TextInput(
                self.text_str,
                style=STYLES["input_style"],
                on_change=self.on_text_change,
            ),
            Label(
                f"Measurement in {self.to_unit}: {float_to_str(to_value)}",
                style=STYLES["to_unit_label"],
            ),
        )


class MyApp(ed.Component):
    def render(self):
        return ed.View(layout="column")(
            ConversionWidget("meters", "feet", METERS_TO_FEET),
            ConversionWidget("feet", "meters", 1 / METERS_TO_FEET),
        )


if __name__ == "__main__":
    ed.App(MyApp()).start()
