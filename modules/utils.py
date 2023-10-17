import re
import os

supported_websites = ["haraj", "aqar", "gathern"]
file_format = ["csv", "json", "excel", "sql"]

def create_folder():
        path = os.path.join(os.getcwd(), "data")
        is_exist = os.path.exists(path)
        os.mkdir(path) if not is_exist else path

def checker(website_name:str=None, save_format:str=None, path_or_buf:str=None):
    if website_name in supported_websites:
        raise ValueError(f"The {website_name} website is not supported. Only following website are: \n {supported_websites}")
    if save_format not in file_format:
        raise ValueError(f"The {save_format} formate is not supported. Only following website are: \n {file_format}")
    if path_or_buf is not None:
        pattern = r"^([A-Z]:\\)?[A-Za-z0-9_]+(\\[A-Za-z0-9_]+)*$"
        match = bool(re.match(pattern, path_or_buf))
        assert bool(match) is True, f"Path does not match pattern: {path_or_buf}"


def extract_website_name(url):
    # define a regex pattern that matches the optional scheme, optional "www." prefix, website name, domain name, and top-level domain of a URL
    pattern = r"(?:https?://)?(?:www\.)?([a-z0-9-]+)\.[a-z0-9-]+"
    # search for the pattern in the text
    match = re.search(pattern, url)
    # if there is a match, get the website name group
    if match:
        website_name = match.group(1)
        # check if the website is supported
        checker(website_name=website_name)
        # return the website name
        return website_name
    # otherwise, raise a message telling the user to enter a valid website link
    else:
        raise ValueError("Please enter a valid website link.")

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

        checker(save_format=save_format)
        path_or_buf=checker(path_or_buf=path_or_buf)

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
            return df.to_json(path_or_buf=path_or_buf)
        
        elif save_format == "excel":
            return df.to_excel(
                path_or_buf,
                sheet_name="WebData",
                index=False
                )
        
        elif save_format == "sql":
            return sql_connect(database_url=database_url)
            