import pandas as pd
import requests
from bs4 import BeautifulSoup
# this was written in order to clean the data of ingrdients list.
rdata = pd.read_csv('recipieA.csv')

# print(rdata[:10])
MAX_RETRIES = 20
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
session.mount('https://', adapter)
session.mount('http://', adapter)
for i in range(rdata.shape[0]-1):

    if (len((rdata['ingredients'][i]).split(",")) < 5):

        url = rdata['URL'][i]
        html_text1 = session.get(url).text
        soup1 = BeautifulSoup(html_text1, 'lxml')
        # print(html_text.status_code)

        # print(html_text1.content)

        # except (ConnectionError, ProtocolError):
        # pass

        # else:
        try:
            rdata['ingredients'][i] = [j.text for j in soup1.find(
                'div', class_='entry-content').find_all('ul')]
            print(rdata['ingredients'][i])
        except AttributeError:
            pass

rdata.to_csv('recipieA.csv')
