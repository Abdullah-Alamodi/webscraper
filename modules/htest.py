from scraper import scraper

# links = scraper.get_haraj_links(url="https://haraj.com/", nu_of_pages=3)

# details = scraper.get_haraj_details(links, save=True, save_format="json")
 
# scraper.get_aqar_link("https://sa.aqar.fm", 0)

# from bs4 import BeautifulSoup

# html = '''<div class="listing_LinkedListingCard__5SRvZ" href="/%D8%A7%D8%B3%D8%AA%D8%B1%D8%A7%D8%AD%D8%A9-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1/%D8%A7%D9%84%D9%85%D8%B2%D8%A7%D8%AD%D9%85%D9%8A%D8%A9/%D8%AD%D9%8A-%D8%B4%D8%AE%D9%8A%D8%A8/%D8%B6%D8%B1%D9%85%D8%A7-5299726"><div class="listingCard_listingCard__NpqM0"><div class="listingCard_content__SLJJG"><div class="listingCard_top__nVn1L"><h4 class="listingCard_title__45XgY listingCard_truncatedText__otzLq "><a href="/%D8%A7%D8%B3%D8%AA%D8%B1%D8%A7%D8%AD%D8%A9-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1/%D8%A7%D9%84%D9%85%D8%B2%D8%A7%D8%AD%D9%85%D9%8A%D8%A9/%D8%AD%D9%8A-%D8%B4%D8%AE%D9%8A%D8%A8/%D8%B6%D8%B1%D9%85%D8%A7-5299726">استراحة للإيجار في ضرما</a></h4></div><div class="listingCard_price__N5eJ4">'''

# soup = BeautifulSoup(html, 'html.parser')

# # Find the 'a' tag
# link = soup.find('a')

# # Extract the href attribute
# url = link.get('href')

# print("https://sa.aqar.fm"+url)

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

url = 'https://sa.aqar.fm/%D9%81%D9%84%D9%84-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%BA%D8%B1%D8%A8-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%AD%D9%8A-%D8%B7%D9%88%D9%8A%D9%82/%D8%B4%D8%A7%D8%B1%D8%B9-%D9%85%D8%AD%D9%85%D8%AF-%D8%A8%D9%86-%D8%A3%D8%AD%D9%85%D8%AF-%D8%A7%D9%84%D9%82%D8%B3%D8%B7%D9%84%D8%A7%D9%86%D9%8A-%D8%AD%D9%8A-%D8%B7%D9%88%D9%8A%D9%82-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6-%D9%85%D9%86%D8%B7%D9%82%D8%A9-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6-5577567'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)