import fake_useragent
import requests
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random
site_link = 'http://www.guncha.uz/uz'
header = {'user-agent': user}


def find_category():
    category_response = requests.get(site_link, headers=header).text
    category_soup = BeautifulSoup(category_response, 'lxml')
    nav_menu = None
    for index in range(2, 4):
        nav_menu = category_soup.find('div', class_='cols clearfix').find('ul').find_all('li')[index].find_next(
            'a')
        if nav_menu:
            break
        return nav_menu.get('href')


print(find_category())


def get_article_text():
    for a in range(1, 3):
        print(find_category(), a)

# get_article_text()
