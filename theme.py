
from color import Color

ColorValue = tuple[int, int, int] | str


class Theme:

    def __init__(
        self,
        light_bg: ColorValue,
        dark_bg: ColorValue,
        light_trace: ColorValue,
        dark_trace: ColorValue,
        light_moves: ColorValue,
        dark_moves: ColorValue,
    ) -> None:
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)
        
