import requests
from bs4 import BeautifulSoup as bs

with open("./data.txt", "r") as f:
    links = f.readlines()

"check if the link is the service link"
# for link in links:
#     if "1dmy" in link:
#         print(link)
#     else:
#         pass


headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)

r = requests.get(links[29])