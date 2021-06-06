from re import T, findall
from bs4 import BeautifulSoup
import http
from requests.models import ProtocolError
import urllib3
import json
import csv

import requests
MAX_RETRIES = 20
url1 = 'https://indianfoodforever.com/'
url2 = 'https://www.bbcgoodfood.com/'
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
session.mount('https://', adapter)
session.mount('http://', adapter)
# for recipie page
'''html_text = requests.get(
    "https://www.indianfoodforever.com/soups/mulligtawney-soup.html").text
soup = BeautifulSoup(html_text, 'lxml')
# print(html_text.status_code)

title = soup.find('div', class_='inside-article').header.h1.text
print(title)
ingred = soup.find('div', class_='entry-content').ul.find_all('li')
[print(i.text) for i in ingred]'''

# for recipe collection page
'''html_text = requests.get(
    "https://www.indianfoodforever.com/snacks").text
soup = BeautifulSoup(html_text, 'lxml')

r_list = [i.div.header.h2.a['href'] for i in soup.find_all('article')]'''

# for home page


def scrapeUrl1():
    try:
        csvfile = open('recipieC.csv', 'w', newline='')
        obj = csv.writer(csvfile)
        hRow = ('Title', 'ingredients', 'URL')
        obj.writerow(hRow)
        r = session.get(url1).text
        soup = BeautifulSoup(r, 'lxml')

    except (ConnectionError, ProtocolError):
        pass
    else:
        rc_list = []
        '''[[rc_list.append(j.a['href']) for j in i.div.ul.find_all(
            'li')] for i in soup.find_all('aside', class_="widget_nav_menu")[3:5]+soup.find_all('aside', class_="widget_nav_menu")[6:]]'''
        [rc_list.append(j.a['href']) for j in soup.find(
            'aside', id="nav_menu-5").div.ul.find_all('li')[1:]]

        for lnk in rc_list:
            # try:
            html_text = session.get(lnk).text
            soup = BeautifulSoup(html_text, 'lxml')

            # except (ConnectionError, ProtocolError):
            # pass
            # else:
            for j in [i.div.header.h2.a['href'] for i in soup.find_all('article')]:
                # try:
                html_text1 = session.get(j).text
                soup1 = BeautifulSoup(html_text1, 'lxml')
                # print(html_text.status_code)

                # print(html_text1.content)

                # except (ConnectionError, ProtocolError):
                # pass

                # else:
                try:
                    title = soup1.find(
                        'div', class_='inside-article').header.h1.text

                    ingred = [i.text for i in soup1.find(
                        'div', class_='entry-content').find_all('ul')]
                    url = j
                except AttributeError:
                    pass
                else:

                    ing_list = ingred

                    rRow = (title, ing_list, url)
                    try:
                        obj.writerow(rRow)
                    except UnicodeEncodeError:
                        pass

    finally:
        csvfile.close()


def scrapeUrl2():
    try:
        csvfile = open('recipieA.csv', 'w', newline='')
        obj = csv.writer(csvfile)
        hRow = ('Title', 'ingredients', 'URL')
        obj.writerow(hRow)
        r = session.get("https://www.bbcgoodfood.com/") .text
        soup0 = BeautifulSoup(r, 'lxml')
    except (ConnectionError, ProtocolError):
        pass

    else:
        link0 = soup0.find(
            'div', class_="main-nav__sub-menu main-nav__mega-menu main-nav__mega-menu--cols-4").select('a[href]')

        for i in link0[::4]:

            html_text1 = session.get(
                "https://www.bbcgoodfood.com" + i['href']).text
            soup1 = BeautifulSoup(html_text1, 'lxml')

            link1 = soup1.find_all(
                'a', class_="standard-card-new__article-title qa-card-link")

            for k in link1:
                if "collection" in k['href']:
                    html_text2 = session.get(str(k['href'])).text
                    soup = BeautifulSoup(html_text2, 'lxml')
                    link_1 = soup.find_all(
                        'div', class_='col-md-12 template-article__row')
                    for j in link_1:
                        link_10 = j.find(
                            'a', class_="standard-card-new__article-title qa-card-link")
                        if(link_10 != None):

                            html_text2 = session.get(link_10["href"]).text
                            soup = BeautifulSoup(html_text2, 'lxml')
                            try:
                                recipie_name = soup.find(
                                    'h1', class_="post-header__title post-header__title--masthead-layout heading-1").text

                                #cook_prep_time = soup.find_all('time')
                                #cpTime = {}
                                #cpTime['cookTime'] = cook_prep_time[0].text
                                #cpTime['prepTime'] = cook_prep_time[1].text

                                ingred = soup.find('section', class_='recipe__ingredients').find_all(
                                    'a', class_='link link--styled')
                                ingred_ = []
                                for a in ingred:
                                    ingred_.append(a.text)
                            except AttributeError:
                                pass
                            else:

                                ing_list = ingred_

                                rRow = (recipie_name, ing_list,
                                        link_10["href"])
                                try:
                                    obj.writerow(rRow)
                                except UnicodeEncodeError:
                                    pass

                if "category" in k['href']:
                    html_text2 = session.get(str(k['href'])).text
                    soup = BeautifulSoup(html_text2, 'lxml')
                    link_1 = soup.find_all(
                        'div', class_='standard-card-new__main')
                    for j in link_1:
                        link = j.find(
                            'a', class_='standard-card-new__article-title qa-card-link')['href']
                        html_text2 = session.get(link).text
                        soup = BeautifulSoup(html_text2, 'lxml')
                        try:
                            recipie_name = soup.find(
                                'h1', class_="post-header__title post-header__title--masthead-layout heading-1").text

                            #cook_prep_time = soup.find_all('time')
                            #cpTime = {}
                            #cpTime['cookTime'] = cook_prep_time[0].text
                            #cpTime['prepTime'] = cook_prep_time[1].text

                            ingred = soup.find('section', class_='recipe__ingredients').find_all(
                                'a', class_='link link--styled')
                            ingred_ = []
                            for a in ingred:
                                ingred_.append(a.text)
                        except AttributeError:
                            pass
                        else:
                            ing_list = ingred_

                            rRow = (recipie_name, ing_list, link)
                            try:
                                obj.writerow(rRow)
                            except UnicodeEncodeError:
                                pass


n = int(input("Enter '1' for 'https://indianfoodforever.com/' \nEnter '2' for 'https://www.bbcgoodfood.com'\n"))
f = False
while(f != True):
    if(n == 1):
        print(f"Please wait! Scraping website {url1}")
        scrapeUrl1()

        f = True
    elif(n == 2):
        print(f"Please wait! Scraping website {url2}")
        scrapeUrl2()

        f = True
    else:
        print("Enter the proper input")
        n = int(input(
            "Enter '1' for 'https://indianfoodforever.com/' \nEnter '2' for 'https://www.bbcgoodfood.com'\n"))
