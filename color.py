class Color:

    def __init__(self, light: tuple[int, int, int] | str, dark: tuple[int, int, int] | str) -> None:
        self.light = light
        self.dark = dark
