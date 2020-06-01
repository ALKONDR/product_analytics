import pandas as pd
import requests
from tqdm import tqdm_notebook

from collections import Counter
import random


vacancies = []
vacancy_query = "product analyst"

for page_number in tqdm_notebook(range(100)):
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

cities = []

for vacancy in vacancies:
    try:
        cities.append(vacancy.get("area").get("name"))
    except:
        pass


city_counter = Counter(cities)
city_and_count = list(city_counter.items())


def random_cities_generator(city_count_array, n_samples=1):
    all_counts_sum = sum([x[1] for x in city_count_array])
    city_sampling_borders = []
    
    prefix_sum = 0
    for city in city_count_array:
        prefix_sum += city[1]
        city_sampling_borders.append(prefix_sum / all_counts_sum)
        
    answer_samples = []
    for i in range(n_samples):
        random_number = random.random()
        
        current_city = city_count_array[0][0]
        for i in range(len(city_sampling_borders)):
            current_city = city_count_array[i][0]
            
            if random_number < city_sampling_borders[i]:
                break
                
        answer_samples.append(current_city)
        
    return answer_samples

print(random_cities_generator(city_and_count, 100))
