from bs4 import BeautifulSoup
import requests
def parse(response: requests.Response) -> dict:
    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.title
    links = []    
    
    for anchor_tag in soup.find_all('a'):
        href = anchor_tag.get('href')
        if href and href.startswith("http"):
            links.append(href)

    
    if title_tag:
        return {"title": title_tag.string , 'links': links}
    else:
        return{"title": None, "links": []}