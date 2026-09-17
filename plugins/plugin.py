from collections.abc import Callable

class Plugin:
    def __init__(self):
        self.commands = {}
        self.non_command = False
        self.usable_tools = {}

    def get_commands(self) -> dict[str, Callable[[str], str]]:
        return self.commands

    def get_tools(self) -> dict[str, str]:
        return self.usable_tools