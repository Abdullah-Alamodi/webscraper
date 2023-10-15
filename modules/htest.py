from scraper import Scraper

links = Scraper.get_haraj_links(nu_of_pages=3)
print(links)
# Scraper.get_haraj_details(links, save=True, save_format="csv")