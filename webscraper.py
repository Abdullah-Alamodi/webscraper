from bs4 import BeautifulSoup as bs
import requests

def get_links(url:str, load_to:str = None):
    """Extract the links from Absher website
    ========================================
    url: str -> add the url
    load_to: str -> text file to save out of the function to"""
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )
    
    r = requests.get(url=url, headers=headers)

    soup = bs(r.content)
    body = soup.find(class_="row list-unstyled list")


    links = []

    for link in soup.findAll("a"):
        links.append(url + link.get("href"))

    if load_to==None:
        print("The output:", links, "=============", "DONE SCRAPING", sep="\n")
    else:
        with open("./data.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(links))

