from haraj_scraper import get_haraj_links, get_haraj_details

links = get_haraj_links(nu_of_pages=1)
print(links)
get_haraj_details(links, save=True, save_format="csv")