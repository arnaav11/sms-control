from plugins.plugin import Plugin

class Parser:
    def __init__(self, plugins: list[Plugin]):
        self.plugins = plugins

    def parse_command(self, command_str: str) -> str:
        return ''