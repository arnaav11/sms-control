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
            if command[0] in self.plugins[i].get_commands():
                method = self.plugins[i].get_commands()[command[0]]
                return method(args)

    
if __name__ == '__main__':
    from config import *

    tester = DefaultParser(
        plugins=plugins
    )

    test_input = input('Enter command: ')
    while test_input != '/quit':
        print(f'Result: \n{tester.parse_command(test_input)}')
        test_input = input('Enter command: ')