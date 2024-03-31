import datetime
import time
import json
import requests
from bs4 import BeautifulSoup

# 获取总页数
url = 'https://www.caaa.cn/html/fw/market/zhu/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
max_page = int(soup.find('div', id='pages').contents[-3].text)
print(f'Max Page: {max_page}.\n')

index = []
for page in range(1, max_page + 1):
    print(f'Processing page {str(page)}/{str(max_page)}.')
    if page == 1:
        page_url = url
    else:
        page_url = url + f'{str(page)}.html'
    page_response = requests.get(page_url)
    page_soup = BeautifulSoup(page_response.content, 'html.parser')
    for item in list(page_soup.find('div', class_='ov').children)[3].ul:
        if str(item) == '\n':
            continue
        item = item.contents[1]
        item_date = item.find('div', class_='news_page_date df fldc jcc aic').text.split('\n')[1:3]
        item_date = datetime.date(int(item_date[1].split('-')[0]), int(item_date[1].split('-')[1]), int(item_date[0]))
        item_title = item.find('div', class_='news_title_fz ell').text
        item_url = item['href']
        index.append(
            {
                'date': item_date.strftime('%Y-%m-%d'),
                'title': item_title,
                'url': item_url
            }
        )
        print(f'\tGot data: {item_title}.')
        time.sleep(0.1)

print('Done.')
with open('index.json', 'w', encoding='utf-8') as f:
    json.dump(index, f, indent=4, ensure_ascii=False)
