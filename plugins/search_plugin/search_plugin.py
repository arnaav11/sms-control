from plugins.plugin import Plugin
from plugins.search_plugin.search_connector import SearchConnector
from plugins.search_plugin.w3m_connector import W3MConnector


class SearchPlugin(Plugin):
    def __init__(self, search_url: str, exe: str = '/bin/fish'):
        super().__init__()
        
        self.search_connector = SearchConnector(base_url=search_url)
        self.w3m_connector = W3MConnector(exe=exe)

        self.commands = {
            'search': self.search,
            'web_fetch': self.web_fetch
        }

        self.tools = {
            'search': 'Search the web with a query. Takes the query/search as the arg',
            'web_fetch': 'Get contents of a webpage in plaintext. takes the URL as the arg'
        }

    def search(self, command: str) -> str:
        if not command:
            return 'No query was given'

        try:
            results = self.search_connector.get_search(command)

            result_str = ''

            for i in results:
                result_str += f'URL: {i['url']}'
                result_str += f'\nTitle: {i['title']}'
                result_str += f'\nSnippet: {i['content']}\n'
            
            return result_str


        except Exception as e:
            return f'An error occurred: {str(e)}'
        
    def web_fetch(self, command: str):
        if not command:
            return 'No URL provided'
        
        return self.w3m_connector.get_website(command)
