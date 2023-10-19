import re
import os

supported_websites = ["haraj", "aqar", "sa", "gathern"]
file_format = ["csv", "json", "xlsx", "sql"]

def create_folder(path_or_buf):
        path_or_buf = os.path.join(os.getcwd(), "data")
        is_exist = os.path.exists(path_or_buf)
        if not is_exist:
            os.mkdir(path_or_buf)


def extract_website_name(url):
    # define a regex pattern that matches the optional scheme, optional "www." 
    # prefix, website name, domain name, and top-level domain of a URL
    pattern = r"(?:https?://)?(?:www\.)?([a-z0-9-]+)\.[a-z0-9-]+"
    # search for the pattern in the text
    match = re.search(pattern, url)
    # if there is a match, get the website name group
    if match:
        website_name = match.group(1)
        return website_name
    # otherwise, raise a message telling the user to enter a valid website link
    else:
        raise ValueError("Please enter a valid website link.")

def checker(url:str=None, save_format:str=None, path_or_buf:str=None, **kwargs):
    web_name = extract_website_name(url=url) if url!=None else None
    if web_name!=None and web_name not in supported_websites:
        raise ValueError(f"The {web_name} website is not supported. Only following website are: \n {supported_websites}")
    
    if save_format is not None and save_format not in file_format:
        raise ValueError(f"The {save_format} formate is not supported. Only following website are: \n {file_format}")
    
    if path_or_buf is not None:
        pattern = r"^[A-Z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]*$"
        match = bool(re.match(pattern, path_or_buf))
        assert bool(match) is True, f"Path {path_or_buf} does not match pattern: drive_name:\folder\file.{save_format}"

    if isinstance(url, str) and kwargs.get("aqar_pagination", True):
            # pattern is wather the input is the main url format or url\subdirectory format
            match = re.match(r'https://sa.aqar.fm/(\w+)(?:/(\d+))?', url)
            u_url = ""
            if match: # check if the regular expression matched anything
                try: # try to assign the values to the variables
                    section, page_number = match.groups()
                    page_number = 1 if page_number is None else page_number
                    u_url = f"https://sa.aqar.fm/{section}/"
                except Exception as e: # handle any errors that may occur
                    print(f"Error: {e}")
            
                return u_url
            else: # if the regular expression did not match anything
                return "https://sa.aqar.fm/عقارات/1"


def save_file(
            data,
            path_or_buf:str,
            save_format:str = "csv",
            mode:str="w",
            encoding:str = "utf-8",
            database_url: str = None
            ):
        from pandas import DataFrame
        from pandas.io import sql

        checker(save_format=save_format, path_or_buf=path_or_buf)
        create_folder(path_or_buf)


        df = DataFrame.from_dict(data=data)

        def sql_connect(database_url=database_url):
            if database_url==None:
                database_url = f"mysql+mysqlconnector://root:password@localhost:3306/{data}"
                
                # create a connection to local sql database
                con = sql.connect(database_url)
                return df.to_sql(con=con)

            else:
                database_url = database_url
                # create a conection to existinig sql database
                con = sql.connect(database_url)
                return df.to_sql(con=con)


        if save_format == "csv":
            return df.to_csv(
                path_or_buf=path_or_buf,
                index=False,
                encoding=encoding,
                mode=mode
                )
        
        elif save_format == "json":
            return df.to_json(
                path_or_buf=path_or_buf, 
                orient="records",
                date_format="iso",
                compression="infer",
                mode=mode,
                force_ascii=False,
                indent=4
                )
        
        elif save_format == "xlsx":
            return df.to_excel(
                path_or_buf,
                sheet_name="WebData",
                index=False
                )
        
        elif save_format == "sql":
            return sql_connect(database_url=database_url)
            