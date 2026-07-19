from collections.abc import Callable

class Plugin:
    def __init__(self):
        self.commands = {}

    def get_commands(self) -> dict[str, Callable[[str], str]]:
        return self.commands