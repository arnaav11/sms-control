import subprocess

class ShellConnector:
    def __init__(self, allowed_commands: list, allow_piping: bool = False, allow_chains: bool = False, exe: str = '/bin/fish'):
        self.allowed_commands = allowed_commands
        self.allow_chains = allow_chains
        self.allow_piping = allow_piping
        self.executable = exe

    def run_command(self, command: str) -> subprocess.CompletedProcess[str]:
        output = subprocess.run(command, shell=True, text=True, executable=self.executable, capture_output=True)
        return output
    
    def run_command(self, command: str) -> subprocess.CompletedProcess[str]:
        output = subprocess.run(command, shell=True, text=True, executable=self.executable, capture_output=True)
        return output

    def allow_command(self, command: str) -> bool:
        if command.split()[0] not in self.allowed_commands:
            return False
        if '&' in command and not self.allow_chains:
            return False
        if '|' in command and not self.allow_piping:
            return False
        
        return True
    

if __name__ == '__main__':
    from config import allowed_shell_commands, shell

    tester = ShellConnector(allowed_shell_commands, exec=shell)

    test_command = input('Enter Command: ')

    if not tester.allow_command(test_command):
        print('\nCommand not allowed')
    else:
        output = tester.run_command(test_command)
        print(f'\n\nOutput:\n{output.stdout} \nReturn Code = {output.returncode}')
