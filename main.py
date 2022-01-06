import requests
from bs4 import BeautifulSoup
import json

persons_url_list = []

for i in range(0, 740, 20):
    url = f'https://www.bundestag.de/ajax/filterlist/en/members/453158-453158/h_a45203fd0f1592191f1bda63b5d86d72?limit=20&noFilterSet=true&offset={i}'
    print(url)

    q = requests.get(url)
    q = q.content

    soup = BeautifulSoup(q, 'lxml')
    persons = soup.find_all(class_='bt-open-in-overlay')

    for person in persons:
        person_page_url = person.get('href')
        persons_url_list.append(person_page_url)

with open('persons_url_list.txt', 'a') as file:
    for line in persons_url_list:
        file.write(f'{line}\n')


with open('persons_url_list.txt') as file:

    lines = [line.strip() for line in file.readlines()]
    c = 0
    json_response = []
    for line in lines:
        if c < 10:
            result = requests.get(line).text

            soup = BeautifulSoup(result, 'lxml')
            person = soup.find(class_='bt-biografie-name').find('h3').text
            person_names = person.strip().split(',')
            person_name = person_names[0]
            person_company = person_names[1].strip()

            sn_urls = []
            social_networks = soup.find_all(class_='bt-link-extern')

            for item in social_networks:
                sn_urls.append(item.get('href'))
                print(item)

            data = {
                'person_name': person_name,
                'person_company': person_company,
                'social_networks': sn_urls
            }
            json_response.append(data)
            c += 1


with open('list.json', 'w', encoding='UTF-8-sig') as file:
    json.dump(json_response, file, indent=4, ensure_ascii=False)
