from typing import Callable, Literal

class Plugin:
    def __init__(self):
        self.tool_calling: bool = False
        self.tools: dict[str, dict[Literal['method', 'description'], Callable[[str], str] | str]] = {}
        self.callback_method: str = ''

    def get_tools(self) -> dict[str, dict[Literal['method', 'description'], Callable[[str], str] | str]]:
        return self.tools