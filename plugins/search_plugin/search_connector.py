import requests

class SearchConnector:
    def __init__(self, base_url: str):
        self.base_url = base_url


    def get_search(self, query: str, categories: str = 'general') -> dict[str, str]:
        params = {
            'q': query,
            'format': 'json',
            'categories': categories,
            'language': 'en-US'
        }

        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()['results']

if __name__ == '__main__':
    url = 'http://127.0.0.1:8888/search'
    conn = SearchConnector(base_url=url)

    query = input('Enter query: ')
    results = conn.get_search(query=query)

    print('\n\nResults: \n')
    print(f'Query: "{query}"\n')

    for i in results:
        print('-x-x-x-')
        print(f'URL: {i["url"]}')
        print(f'Title: {i["title"]}')
        print(f'Snippet: {i["content"]}')
        print('-x-x-x-\n')
