import time
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os

url = "https://haraj.com/"

file_format = {
                "csv": ".csv",
               "txt": ".txt",
               "text": ".txt",
               "json": ".json"
                }

def save_file(
        data,
        path_or_buf,
        save_format:str = "txt",
        mode:str="w",
        encoding:str = "utf-8"
        ):
    from pandas import DataFrame
    df = DataFrame.from_dict(data=data)

    if save_format == "csv":
        return df.to_csv(
            path_or_buf=path_or_buf,
            index=False,
            encoding=encoding,
            mode=mode
            )
    
    elif save_format == "json":
        return df.to_json(path_or_buf=path_or_buf)
    
    elif save_format == "excel":
        return df.to_excel(
            path_or_buf,
            sheet_name="WebData",
            index=False
            )

def get_haraj_links(
        url:str = url, 
        nu_of_pages = 10,
        save:bool = False,
        save_format:str = 'txt',
        mode:str= "w"
        ):
    """Extract the links of products and/or services from Haraj website

    Parameters
    ========================================
    url: str -> add the url of Haraj.com. The default url is the Haraj 
        homepage. You can add the url of any section if you need to scrape
        a specific products or services tags.
        Default : https://haraj.com/
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
    
    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    driver.get(url=url)
    
    if nu_of_pages == None:
        while True:
            # NOT RECOMMENDED for RAM < 6
            # Consumes both time and computational resources
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.1)
            driver.find_element(By.ID, "more").click()
            time.sleep(0.5)
    else: 
        for i in range(0, nu_of_pages):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.1)
                driver.find_element(By.ID, "more").click()
                time.sleep(0.5)
            except Exception as e:
                print(f"Warrnings: The loading took long time. Check the internert or check the error {e}")

    haraj_links = driver.find_elements(By.CLASS_NAME, "postTitle")
    haraj_links = [link.find_element(By.TAG_NAME, "a").get_attribute("href") for link in haraj_links]
    print(f"{len(haraj_links)} links were scrapped successfully.")

    if save==True:
        save_file("haraj_links", haraj_links, save_format=save_format, mode=mode)
        print(f"The haraj_links.{save_format} was saved to `{os.getcwd()}` directory.")

    return haraj_links



def get_haraj_details(url, 
                      save:bool = False, 
                      save_format:str = 'txt', 
                      save_method:str = "w"
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
    save_method: str -> w
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
        "phone_number": []
        }
    
    if isinstance(url, str):
        r = requests.get(url=url, headers=headers)
        soup = bs(r.content)
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
        driver.get(url=url)

        soup = bs(r.content)
        body = soup.find(class_="postMain") # body data it the url
        body1 = body.find(class_="post_header_wrapper") # post header wrapper class

        # Scrape the data
        ad_title = body1.find("h1").contents[0]
        seller_name = body1.find("a").find("span").contents[0]
        city = body.find(class_="city").contents[0]

        driver.find_element(By.CLASS_NAME, "contact").click()
        time.sleep(0.5)
        phone_number = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/a[2]')\
        .get_attribute("href")

        # append scraped data
        haraj_data["ad_title"].append(ad_title)
        haraj_data["seller"].append(seller_name)
        haraj_data["city"].append(city)
        haraj_data["phone_number"].append(phone_number)

    else:
        for link in url:
            r = requests.get(url=link, headers=headers)
            soup = bs(r.content)
            driver = webdriver.Edge(EdgeChromiumDriverManager().install())
            driver.get(url=link)

            soup = bs(r.content)
            body = soup.find(class_="postMain") # body data it the url
            body1 = body.find(class_="post_header_wrapper") # post header wrapper class

            # Scrape the data
            ad_title = body1.find("h1").contents[0]
            seller_name = body1.find("a").find("span").contents[0]
            city = body.find(class_="city").contents[0]

            driver.find_element(By.CLASS_NAME, "contact").click()
            time.sleep(0.5)
            phone_number = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/a[2]')\
            .get_attribute("href")

            # append scraped data
            haraj_data["ad_title"].append(ad_title)
            haraj_data["seller"].append(seller_name)
            haraj_data["city"].append(city)
            haraj_data["phone_number"].append(phone_number)
    print(f"{len(haraj_data)} elements were scrapped successfully.")

    if save==False:
        return haraj_data
    else:
        save_file("haraj_data", list(haraj_data), save_format, save_method)
        print(haraj_data)
        print(f"The haraj_data.{save_format} was saved to `{os.getcwd()}` directory.")


