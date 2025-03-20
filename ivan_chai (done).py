import requests
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://agrobazar.ru/herb/wholesale/ivan_chay/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3' }

response = requests.get(url , headers=headers)
r=response.text

soup = BeautifulSoup(r, 'html.parser')
price = soup.find_all('span', class_="pl-price")
place = soup.find_all('div', class_='pl-sale-place')
lp=list(price)
lpp=list(place)
one=len(list(price))
two=len(list(place))
prices=[]
places=[]

for i in range(1, one):
    price_text = lp[i].text.strip()
    prices.append(int(price_text.split()[0]))
print(prices)
for j in range(1, two):
    place_text = lpp[j].text.strip()
    st=place_text.split(' ')
    if st[1]=='продажи:\n':
        st[37]=st[37][:-1]
        places.append(st[37])
print(places)

mint=['иван-чай']*len(places)
print(mint)
dict = {'растение': mint, 'город': places, 'цена': prices}
df2 = pd.DataFrame(dict)
df2.drop(df2[df2['цена'] < 100].index, inplace=True)

list_cities = df2['город'].tolist()

def get_lat(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        map_links = soup.find_all('a', class_='mw-kartographer-maplink')
        if map_links:
            map_link = map_links[0]
            lat = float(map_link['data-lat'])
            return lat
        return None, None
    except:
        return None, None
def get_lon(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        map_links = soup.find_all('a', class_='mw-kartographer-maplink')
        if map_links:
            map_link = map_links[0]
            lon = float(map_link['data-lon'])
            return lon
        return None, None
    except:
        return None, None
lat=[]
lon=[]


for i in list_cities:
  url='https://ru.wikipedia.org/wiki/'+i
  lat.append(get_lat(url))
  lon.append(get_lon(url))
d = {'город': list_cities, 'долгота': lon, 'широта': lat}
df1 = pd.DataFrame(data=d)
merged_df = pd.merge(df1, df2, on='город', how='left')

df_cleaned = merged_df[merged_df['долгота'] != (None, None)]
df_cleaned.drop_duplicates(inplace=True)
print(df_cleaned)
