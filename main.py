import requests
import pandas
import os
import json
from pprint import pprint as print

# & Decimal to hex
def hexed(dec: int) -> str:
    return '#'+hex(dec)[2:].upper()


# & Converts json to python types (dict|list)
def json_to_dict(_json: bytes) -> dict|list:
    return json.loads(_json)


# & Products data to pandas data frame 
def json_to_df(products: list) -> pandas.DataFrame:
    data = {"name": [], 
            "id": [], 
            "product price": [],
            "delivery price": [],
            "total price": [],
            "return price": [],
            "brand": [], 
            "rating": [], 
            "color": []}
    for product in products:
        data["name"].append(product["name"])
        data["id"].append(product["id"])
        data["product price"].append(product["sizes"][0]["price"]["product"])
        data["delivery price"].append(product["sizes"][0]["price"]["logistics"])
        data["total price"].append(product["sizes"][0]["price"]["total"])
        data["return price"].append(product["sizes"][0]["price"]["return"])
        data["brand"].append(product["brand"])
        data["rating"].append(product["rating"])
        try: color = hexed(product["colors"][0]["id"])
        except IndexError: color = ""
        data["color"].append(color)

    return pandas.DataFrame(data)


# & Create files directory
def create_dir(dirname: str):
    os.makedirs(dirname, exist_ok=True)


# & Save pandas data frame as excel 
def save_df_exc(df: pandas.DataFrame, dirname: str, filename: str):
    df.to_csv(f"{dirname}/{filename}")


# & Get requests content
def get_req_cont(url: str, headers: dict[str:str] = {}) -> bytes:
    return requests.get(url, headers=headers).content


def main():
    dirname = "files"
    create_dir(dirname)
    query = input("Input the product name: ")
    url = f"https://search.wb.ru/exactmatch/sng/common/v5/search?ab_testing=false&appType=1&curr=rub&dest=36&query={query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false"
    content = get_req_cont(url)
    data = json_to_dict(content)["data"]["products"]
    df = json_to_df(data)
    save_df_exc(df, dirname, f"{query}.xlsx")


if __name__ == "__main__":
    main()