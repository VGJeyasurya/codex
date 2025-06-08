import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from typing import List, Tuple


def crawl(url: str, max_pages: int = 5) -> List[Tuple[str, str]]:
    """Crawl a URL and return a list of (url, title) tuples."""
    visited = set()
    results = []
    queue = [url]

    while queue and len(visited) < max_pages:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        try:
            resp = requests.get(current, timeout=5)
            if 'text/html' not in resp.headers.get('Content-Type', ''):
                continue
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else ''
            results.append((current, title))
            for link in soup.find_all('a', href=True):
                absolute = urljoin(current, link['href'])
                if absolute.startswith(url) and absolute not in visited:
                    queue.append(absolute)
        except Exception:
            continue
    return results
