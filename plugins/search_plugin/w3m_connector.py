import subprocess

from urllib.parse import urlparse
from urllib.request import Request, urlopen

class W3MConnector:
    def __init__(self, exe: str = '/bin/fish', timeout: int = 10):
        self.executable = exe
        self.timeout = timeout

    def get_website(self, url: str) -> str:
        if not self.validate_url(url):
            return ''

        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=self.timeout) as response:
            website_html = response.read()

        return self.parse_html(website_html)

    def validate_url(self, url: str) -> bool:
        parsed_url = urlparse(url.strip())
        return parsed_url.scheme in ("http", "https")

    def parse_html(self, html: str) -> str:
        w3m_output = subprocess.run(
            ["w3m", "-dump", "-T", "text/html"],
            input=html,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )

        return w3m_output.stdout
        
    

if __name__ == '__main__':
    # from config import shell

    conn = W3MConnector()

    url = input(f'Enter URL: ')
    website = conn.get_website(url=url)

    print(f'URL: {url}')
    print(f'Website contents: \n{website}')