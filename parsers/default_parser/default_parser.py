import json

from plugins.plugin import Plugin
from parsers.parser import Parser

class DefaultParser(Parser):
    def __init__(self, plugins: list[Plugin]):
        super().__init__(plugins)

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

        for i in range(len(self.plugins)):
            plugin = self.plugins[i]
            if command[0] in plugin.get_tools():
                method = plugin.get_tools()[command[0]]['method']
                command_output = method(args)
                
                if plugin.tool_calling:
                    return self.call_tool(command_output, plugin=plugin)

                return command_output

    def call_tool(self, call_str: str, plugin: Plugin) -> str:
        try:
            tool_call = json.loads(call_str)
        except json.decoder.JSONDecodeError:
            return call_str

        print('Received agentic tool calls: ')
        print(tool_call)
        print()


        for tool in tool_call:
            if tool == 'respond':
                return tool_call[tool]['args']

            tool_call_str = f'/{tool} {tool_call[tool]['args']}'
            cmd_output = self.parse_command(tool_call_str)

            if tool_call[tool]['callback']:
                callback_command = f'/{plugin.callback_method} {cmd_output}'
                return self.parse_command(callback_command)
            else:
                return cmd_output

        return ''


    
if __name__ == '__main__':
    from config import *

    tester = DefaultParser(
        plugins=plugins
    )

    test_input = input('Enter command: ')
    while test_input != '/quit':
        print(f'Result: \n{tester.parse_command(test_input)}')
        test_input = input('Enter command: ')