import time
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from utils import save_file

class Scraper:
    def __init__(self, Options) -> None:
        self.Options = Options()
        self.save_file = save_file()

    def get_haraj_links(
            url:str, 
            nu_of_pages = 10,
            save:bool = False,
            path_or_buf:str = "haraj_links",
            save_format:str = 'csv',
            mode:str= "w"
            ):
        """Extract the links of products and/or services from Haraj website

        Parameters
        ========================================
        url: str -> add the url of Haraj.com. You can add the url of any section
            if you need to scrape a specific products or services tags.
        nu_of_pages: number of pages that you want to extract links
            data (Number of scrolling). You can either write how many
            scrolls you need to scrape or write None for all links in a
            tags or Haraj website (HPC function andNOT RECOMMENDED for 
            RAM less then 6 GB).
        save: bool -> If True, the output of the function will be saved
            as file based on the `file_format`. If False, the function will 
            return the output as an object.
            Default : False
        save_format: str -> A file format that is saved when the `save` is 
            True. The accepted format are ['.csv', '.txt', '.xlsx']
            Default : txt
        save_method: str -> w
            w: write new or overwrite
            a: append
            for more details, refer to Python open function documentation"""
        options = Options()
        driver = webdriver.Chrome(options=options)
        driver.get(url=url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div/div[2]/div[5]/div/div/button').click()
        
        if nu_of_pages == None:
            while True:
                # NOT RECOMMENDED for RAM < 6
                # Consumes both time and computational resources
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
        else: 
            for i in range(0, nu_of_pages):
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.5)
                except Exception as e:
                    print(f"Warrnings: The loading took long time. Check the internert or check the error {e}")

        haraj_links = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='post-title-link']")
        haraj_links = [link.get_attribute("href") for link in haraj_links]
        print(f"{len(haraj_links)} links were scrapped successfully.")

        if save==True:
            save_file(data=haraj_links,
                    path_or_buf=f"{path_or_buf}.{save_format}", 
                    save_format=save_format,
                    mode=mode)
            print(f"The haraj_links.{save_format} was saved successfully.")
        else:
            return haraj_links



    def get_haraj_details(url, 
                        save:bool = False,
                        path_or_buf:str = "haraj_data", 
                        save_format:str = "csv", 
                        mode:str = "w"
                        ):
        """Extract the links from Absher website
        ========================================
        url: str or str list -> add the url
        save: bool -> If True, the output of the function will be saved
            as file based on the `file_format`. If False, the function will 
            return the output as an object.
            Default : False
        save_format: str -> A file format that is saved when the `save` is 
            True. The accepted format are ['.csv', '.txt', '.xlsx']
            Default : txt
        mode: str -> w
            w: write new or overwrite
            a: append
            for more details, refer to Python open function documentation"""
                
        headers = requests.utils.default_headers()
        headers.update(
            {
                'User-Agent': 'My User Agent 1.0',
            }
        )

        haraj_data = {
            "ad_title": [],
            "seller": [],
            "city": [],
            "description": [],
            "url": []
            }
        
        if isinstance(url, str):
            r = requests.get(url=url, headers=headers)
            soup = bs(r.content, features="html5lib")
            body = soup.find(class_="col-span-full md:col-span-3") # body data it the url)
            post_header = body.find(class_="flex w-full text-[#525762] dark:text-text-regular rounded-3xl") # post header wrapper class

            # Scrape the data
            ad_title = post_header.find("h1").contents[0]
            seller_name = post_header.find("a", {"data-testid": "post-author"}).get_text()
            city = post_header.find(class_="city").contents[0]
            desc = body.find("article").get_text().replace("\n", " ")

            # append scraped data
            haraj_data["ad_title"].append(ad_title)
            haraj_data["seller"].append(seller_name)
            haraj_data["city"].append(city)
            haraj_data["description"].append(desc)
            haraj_data["url"].append(url)

        else:
            from tqdm import tqdm
            for link in tqdm(url):
                try:
                    r = requests.get(url=link, headers=headers)
                    soup = bs(r.content, features="html5lib")
                    body = soup.find(class_="col-span-full md:col-span-3") # body data it the url)
                    post_header = body.find(class_="flex w-full text-[#525762] dark:text-text-regular rounded-3xl") # post header wrapper class

                    # Scrape the data
                    ad_title = post_header.find("h1").contents[0]
                    seller_name = post_header.find("a", {"data-testid": "post-author"}).get_text()
                    city = post_header.find(class_="city").contents[0]
                    desc = body.find("article").get_text().replace("\n", " ")


                    # append scraped data
                    haraj_data["ad_title"].append(ad_title)
                    haraj_data["seller"].append(seller_name)
                    haraj_data["city"].append(city)
                    haraj_data["description"].append(desc)
                    haraj_data["url"].append(url)

                except Exception as e:
                    print(f"{link} was not scrapped because:", e, sep="\n")
        
        print(f"{len(haraj_data['ad_title'])} elements were scrapped successfully.")

        if save==False:
            return haraj_data
        else:
            save_file(data=haraj_data,
                    path_or_buf=f"{path_or_buf}\\haraj_data.{save_format}", 
                    save_format=save_format,
                    mode=mode)
            print(haraj_data)
            print(f"The haraj_data.{save_format} was saved to `{path_or_buf}` directory.")

    def get_aqar_link():
        pass

    def get_aqar_details():
        pass

    def get_gatherin_link():
        pass

    def get_gatherin_details():
        pass

    def get_wasalt_link():
        pass

    def get_wasalt_details():
        pass

