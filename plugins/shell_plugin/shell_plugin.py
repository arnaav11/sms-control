from plugins.plugin import Plugin
from plugins.shell_plugin.shell_connector import ShellConnector

class ShellPlugin(Plugin):
    def __init__(self, allowed_commands: list, exe: str = '/bin/fish'):
        self.connector = ShellConnector(
            allowed_commands=allowed_commands
        )
        self.allowed_commands = allowed_commands
        super().__init__()

        self.tools = {
            'shell': {
                'method': self.run_command,
                'description': f'Runs shell command if allowed. Requires shell command as argument. You cannot pipe or chain commands'
            },
            'commands': {
                'method': self.get_commands,
                'description': 'Returns available shell commands. Check this atleast once before running a shell command'
            }
        }

    def get_tools(self) -> dict[str, str]:
        return self.tools

    def get_commands(self, command: str) -> list[str]:
        return self.allowed_commands

    def run_command(self, command: str) -> str:
        if self.connector.allow_command(command.split()):
            return self.connector.run_command(command).stdout
        else:
            return 'Command not allowed'