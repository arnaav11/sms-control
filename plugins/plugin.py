from typing import Callable, Literal

class Plugin:
    def __init__(self):
        self.tool_calling = False
        self.tools = {}
        self.callback_method = ''

    def get_tools(self) -> dict[str, dict[Literal['method', 'description'], Callable[[str], str] | str]]:
        return self.tools

    def set_tools(self) -> None:
        self.tools = {}