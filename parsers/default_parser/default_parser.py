import json

from plugins.plugin import Plugin
from parsers.parser import Parser
from tooling.tooling import Tooling

class DefaultParser(Parser):
    def __init__(self, plugins: list[Plugin], tooling: Tooling):
        super().__init__()

        self.plugins = plugins
        self.tooling = tooling

    def parse_command(self, command_str: str) -> str:
        command_str = command_str.strip()

        if len(command_str) < 2 or command_str[0] != '/':
            return ''
        
        command_str = command_str[1:]
        command = command_str.split()
        if len(command) == 1:
            args = ''
        else:
            args = ' '.join(command[1:])

        for idx in range(len(self.plugins)):
            plugin = self.plugins[idx]
            if command[0] in plugin.get_tools():
                method = plugin.get_tools()[command[0]]['method']
                command_output = method(args)
                
                if plugin.tool_calling:
                    return self.tooling.call_tools(command_output, callback_cmd=command[0])

                return command_output

    
if __name__ == '__main__':
    from config import *

    tester = DefaultParser(
        plugins=plugins,
        tooling=tooling
    )

    test_input = input('Enter command: ')
    while test_input != '/quit':
        print(f'Result: \n{tester.parse_command(test_input)}')
        test_input = input('Enter command: ')