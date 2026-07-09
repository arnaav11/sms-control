from collections.abc import Callable

class Plugin:
    def __init__(self):
        pass

    def get_commands(self) -> dict[str, Callable[[str], str]]:
        pass