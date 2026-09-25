from typing import Literal, Callable

from plugins.plugin import Plugin

class Tooling:
    def __init__(self):
        self.cur_depth: int = 0
        self.max_depth: int = 5
        self.plugins: list[Plugin] = []
        self.tools: dict[str, dict[Literal['method', 'description'], Callable[[str], str] | str]] = {}

    def call_tools(self, tools: str, callback_cmd: str) -> str:
        pass