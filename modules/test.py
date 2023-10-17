import requests
from bs4 import BeautifulSoup as bs
from scraper import Scraper


headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)
r = requests.get(url="https://haraj.com/11124296862/%D9%85%D8%B1%D8%B3%D9%8A%D8%AF%D8%B3_%D9%81%D8%A7%D9%86", headers=headers)
soup = bs(r.content, features="html5lib")
body = soup.find(class_="col-span-full md:col-span-3") # body data it the url)
post_header = body.find(class_="flex w-full text-[#525762] dark:text-text-regular rounded-3xl") # post header wrapper class

# Scrape the data
ad_title = post_header.find("h1").contents[0]
seller_name = post_header.find("a", {"data-testid": "post-author"}).get_text()
city = post_header.find(class_="city").contents[0]

haraj_data = {
        "ad_title": [],
        "seller": [],
        "city": []
            }
# append scraped data
haraj_data["ad_title"].append(ad_title)
haraj_data["seller"].append(seller_name)
haraj_data["city"].append(city)

print(haraj_data)