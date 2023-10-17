from scraper import Scraper as scraper

links = scraper.get_haraj_links(url="https://haraj.com", nu_of_pages=1)

path = "C:\\Users\\Opal-\\Documents\\abdullah\\data\\"
details = scraper.get_haraj_details(links[:10], save=True, path_or_buf=path)

print(details)