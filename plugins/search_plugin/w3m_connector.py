import subprocess

class W3MConnector:
    def __init__(self, exe: str = '/bin/fish'):
        self.executable = exe

    def get_website(self, url: str) -> str:
        result = subprocess.run(f'w3m -dump "{url}"', shell=True, text=True, executable=self.executable)
        return result.stdout
    

if __name__ == '__main__':
    # from config import shell

    conn = W3MConnector()

    url = input(f'Enter URL: ')
    website = conn.get_website(url=url)

    print(f'URL: {url}')
    print(f'Website contents: \n{website}')