import pandas as pd
import requests
from tqdm import tqdm_notebook


vacancies = []
vacancy_query = "data scientist"

for page_number in tqdm_notebook(range(50)):
    try:
        response = requests.get("https://api.hh.ru/vacancies",
                                params={
                                    "text": vacancy_query,
                                    "page": page_number}
                               )
        json_response = response.json()

        vacancies += json_response["items"]
    except Exception as ex:
        print(ex)

moscow_counter = 0

for vacancy in vacancies:
    try:
        city = vacancy.get("area").get("name")
        
        if city == 'Москва':
            moscow_counter += 1
    except:
        pass

print(moscow_counter / len(vacancies))
