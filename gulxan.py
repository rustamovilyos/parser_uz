import csv
import os
import random
import re
import time

import fake_useragent
import requests
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random
link = 'https://gulxan.uz'
header = {'user-agent': user}
stop_words = ['(davomi)', 'hikoya', '(hikoya)', 'davomi bu yerda', ' Boshi bu yerda:', '(avar ertagi)',
              '(kichik badia)', 'Boshi bu yerda', 'Davomi', '(', ')'
              ]
class_list = ['item-112']


def find_stories():
    response = requests.get(link, headers=header).text
    soup = BeautifulSoup(response, 'lxml')
    nav_menu = soup.find('ul', class_='nav menu mod-list').find_next(
        'li', class_='item-112').find('a')

    time.sleep(1.332)
    return nav_menu.get('href')


def should_skip_text(text):
    # Проверяем, содержит ли текст какое-либо из стоп-слов
    for word in stop_words:
        if word in text:
            return True
    return False


def clean_text(text):
    p_tag = text.find('span').find_next('p')
    if p_tag.find('strong') or p_tag.find('em'):
        for strong_tag in p_tag.find_all(['strong', 'em']):
            strong_tag.decompose()  # Удаляем содержимое теги <strong> <em>

        new_tag = p_tag.get_text(strip=True)
        splited_text = re.split('[.!?:]', new_tag)
        print(splited_text)
        return splited_text
    splited_text = re.split('[.!?:]', p_tag.get_text(strip=True))
    print('1>>', splited_text)
    return splited_text


def get_story_text():
    file_exist = os.path.exists('gulxanuz.csv')
    for page in ['', '?start=100', '?start=200']:
        stories = requests.get(f"{link}{find_stories()}{page}", headers=header).text
        go_to_story_list = BeautifulSoup(stories, 'lxml')
        try:
            go_to_story_list.find('div', id='errorDescription').find_next('h2').find_next('span').get_text()
            print('404')
            continue
        except AttributeError:
            stories_list = go_to_story_list.find_all('div', class_='items-row')
            for links in stories_list:
                get_story_link = links.find('div', class_='column-1').find(
                    'p', class_='readmore').find('a').get('href')
                go_to_story = requests.get(f"{link}{get_story_link}", headers=header).text
                enter_to_story = BeautifulSoup(go_to_story, 'lxml')
                # go_to_fairy = requests.get(f'{link}{get_story_link}{}')
                # story_text = enter_to_story.find('span').get_text(strip=True).split('.')
                cleaned_story_text = clean_text(enter_to_story)
                # print('cleaned_story_text', cleaned_story_text)
                final_text = list(filter(None, cleaned_story_text))
                time.sleep(random.randint(2, 5))
                if not file_exist:
                    with open('gulxanuz.csv', 'a+') as article:
                        writers = csv.writer(article, delimiter='|')
                        if not should_skip_text(final_text) and final_text:
                            writers.writerow(final_text)
                else:
                    with open('gulxanuz.csv', 'a+') as article:
                        writers = csv.writer(article, delimiter='|')
                        if not should_skip_text(final_text) and final_text:
                            writers.writerow(final_text)


get_story_text()
