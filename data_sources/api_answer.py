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

vacancies_dataset = {
    "vacancy_name": [],
    "employer_name": [],
    "city": [],
    "salary": []
}

for vacancy in vacancies:
    vacancies_dataset["vacancy_name"].append(vacancy["name"])
    vacancies_dataset["employer_name"].append(vacancy["employer"]["name"])
    
    try:
        vacancies_dataset["city"].append(vacancy.get("address", {}).get("city", "no city"))
    except:
        vacancies_dataset["city"].append("no city")
        
    salary_from = None
    salary_to = None
    salary_currency = None
    
    try:
        salary_from = vacancy.get('salary', {}).get('from', None)
    except:
        pass
    
    try:
        salary_to = vacancy.get('salary', {}).get('to', None)
    except:
        pass
    
    try:
        salary_currency = vacancy.get('salary', {}).get('currency', None)
    except:
        pass

    
    if salary_currency != 'RUR' or (salary_from is None and salary_to is None):
        vacancies_dataset["salary"].append(None)
    elif salary_from is not None and salary_to is not None:
        vacancies_dataset["salary"].append((salary_from + salary_to) / 2.0)
    elif salary_from is not None:
        vacancies_dataset["salary"].append(salary_from)
    elif salary_to is not None:
        vacancies_dataset["salary"].append(salary_to)
    
vacancies_dataset = pd.DataFrame(vacancies_dataset)

print(vacancies_dataset.salary.mean())
