from plugins.plugin import Plugin
from plugins.shell_plugin.shell_connector import ShellConnector

class ShellPlugin(Plugin):
    def __init__(self, allowed_commands: list, allow_piping: bool = False, allow_chains: bool = False, exe: str = '/bin/fish'):
        self.connector = ShellConnector(
            allowed_commands=allowed_commands,
            allow_piping=allow_piping,
            allow_chains=allow_chains,
            exe=exe
        )
        super().__init__()

        self.commands = {
            'shell': self.run_command
        }

    def run_command(self, command: str) -> str:
        if self.connector.allow_command(command):
            return self.connector.run_command(command).stdout
        
        else:
            return 'Command not allowed'