import shlex
import subprocess

class ShellConnector:
    def __init__(self, allowed_commands: list):
        self.allowed_commands = allowed_commands

    def run_command(self, command: str) -> subprocess.CompletedProcess[str]:
        command_split = shlex.split(command)
        output = subprocess.run(command_split, shell=False, text=True, capture_output=True)
        return output

    def allow_command(self, command_split: list[str]) -> bool:
        return command_split and command_split[0] in self.allowed_commands
    

if __name__ == '__main__':
    from config import allowed_shell_commands, shell

    tester = ShellConnector(allowed_commands=allowed_shell_commands, exe=shell)

    test_command = input('Enter Command: ')

    if not tester.allow_command(test_command):
        print('\nCommand not allowed')
    else:
        output = tester.run_command(test_command)
        print(f'\n\nOutput:\n{output.stdout} \nReturn Code = {output.returncode}')
