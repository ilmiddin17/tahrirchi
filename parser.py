import csv
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

n = 32
header = ['source_url', 'access_datetime ', 'content ']


def parser(url, i):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', class_='col-md-4 mb-25 l-item')
    for result in results:
        inner_url = 'https://kun.uz' + result.find('a', class_='news__title')['href']
        inner_page = requests.get(inner_url)
        inner_soup = BeautifulSoup(inner_page.content, 'html.parser')

        # Getting  content of news
        content = inner_soup.find('div', class_='single-content')
        p_tags = content.find_all('p')
        description = ''
        for tag in p_tags:
            description += tag.text

        # Write data to csv file
        writer.writerow([inner_url, datetime.now(), description])

        # Wait 3 sec to avoid getting blocked
        time.sleep(3)

    if i == n:
        print('Program has finished')
    else:
        # Get new url from Load more button
        new_url = 'https://kun.uz' + soup.find('a', class_='load-more__link')['href']
        i += 1
        parser(new_url, i)


with open('data.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    url = "https://kun.uz/uz/news/category/jamiyat"
    i = 0
    parser(url, i)