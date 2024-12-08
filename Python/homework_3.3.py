import requests
from bs4 import BeautifulSoup

def fetch_and_parse(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        title = soup.title.string if soup.title else "No Title Found"
        print(f"Title of the page: {title}")
        
        links = [a['href'] for a in soup.find_all('a', href=True)]
        print(f"Found {len(links)} links on the page.")
        return links
    except requests.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    url = "https://ru.wikipedia.org/wiki/Lorem_ipsum"
    fetch_and_parse(url)
