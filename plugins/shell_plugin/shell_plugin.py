from plugins.plugin import Plugin
from plugins.shell_plugin.shell_connector import ShellConnector

class ShellPlugin(Plugin):
    def __init__(self, allowed_commands: list, exe: str = '/bin/fish'):
        self.connector = ShellConnector(
            allowed_commands=allowed_commands,
            exe=exe
        )
        super().__init__()

        self.tools = {
            'shell': {
                'method': self.run_command,
                'description': 'Runs shell command if allowed. Requires shell command as argument'
            }
        }

    def get_tools(self) -> dict[str, str]:
        return self.tools

    def run_command(self, command: str) -> str:
        if self.connector.allow_command(command.split()):
            return self.connector.run_command(command).stdout
        else:
            return 'Command not allowed'