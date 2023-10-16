from scraper import Scraper

# links = Scraper.get_haraj_links(nu_of_pages=3)
# print(links)
# Scraper.get_haraj_details(links, save=True, save_format="csv")

from utils import extract_website_name

urls = ["aqar.com", "https://haraj.com", "www.maroof.com", "aqar"]

for link in urls:
    print(extract_website_name(link))