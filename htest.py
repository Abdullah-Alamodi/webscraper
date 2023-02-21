from haraj_scraper import get_haraj_details

with open("./haraj_links.txt", "r") as f:
    file = [link.replace(",", "") for link in f.readlines()]

print(get_haraj_details(file[0], save=True))