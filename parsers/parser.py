from plugins.plugin import Plugin
from tooling.tooling import Tooling

class Parser:
    def __init__(self):
        self.plugins: list[Plugin] = []
        self.tooling: Tooling = None

    def parse_command(self, command_str: str) -> str:
        return ''