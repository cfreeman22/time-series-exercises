# importing libraries
import pandas as pd

import requests

def get_all(endpoint):
    """ Read all records on all pages """
    
    if endpoint not in ["sales", "items", "stores"]:
        return "Not available from this API. Check the documentation"
    
    host = "https://python.zgulde.net/"
    api = "api/v1/"

    url = host + api + endpoint

    response = requests.get(url)

    if response.ok:
        payload = response.json()["payload"]

        # endpoint should be "items", "sales", or "stores"
        contents = payload[endpoint]

        # Make a dataframe of the contents
        df = pd.DataFrame(contents)

        next_page = payload["next_page"]

        while next_page:
            # Append the next_page url piece
            url = host + next_page
            response = requests.get(url)

            payload = response.json()["payload"]

            next_page = payload["next_page"]    
            contents = payload[endpoint]

            df = pd.concat([df, pd.DataFrame(contents)])

            df = df.reset_index(drop=True)

    return df


def get_store_data():
    items = get_all("items")
    stores = get_all('stores')
    sales = get_all("sales")
    
    #merging store and sales
    sales_and_stores = pd.merge(sales, stores, how="inner",left_on="store",right_on="store_id")
    
    # all 3 dataframes into one
    all_stores_data = pd.merge(sales_and_stores,items,how="inner", left_on="item", right_on="item_id")
    
    # writing dataframe to csv
    all_stores_data.to_csv("all_stores_data.csv")
    
    return all_stores_data

    

