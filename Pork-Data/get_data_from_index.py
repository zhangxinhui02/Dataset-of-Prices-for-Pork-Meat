import json
import requests
from bs4 import BeautifulSoup

with open('index.json', 'r', encoding='utf-8') as f:
    index = json.load(f)
    print(f'Loaded {len(index)} indexes from index.json.')

qg_index = []
for item in index:
    if '价格早报' in item['title']:
        qg_index.append(item)
print(f'Got {len(qg_index)} indexes around full country.')

for idx, item in enumerate(qg_index.copy()):
    print(f'Processing data: {item["date"]} {item["title"]} ({idx+1}/{len(qg_index)})...')
    response = None
    while True:
        try:
            response = requests.get(item['url'])
        except requests.exceptions.ReadTimeout:
            continue
        break
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')

    # 初始化一个列表来存储所有行的数据
    data = []
    # 处理合并单元格的情况
    spans = {}

    for row in table.find_all('tr'):
        row_data = []
        cols = row.find_all(['td', 'th'])
        col_idx = 0

        for col in cols:
            # 检查是否有跨列
            colspan = int(col.get('colspan', 1))
            # 检查是否有跨行
            rowspan = int(col.get('rowspan', 1))

            # 处理跨行的情况
            while col_idx in spans:
                span_data, span_rowspan = spans[col_idx]
                row_data.append(span_data)
                if span_rowspan == 1:
                    del spans[col_idx]
                else:
                    spans[col_idx] = (span_data, span_rowspan - 1)
                col_idx += 1

            row_data.append(col.text.strip())
            col_idx += colspan

            # 如果当前单元格有跨行，记录下来
            if rowspan > 1:
                for i in range(col_idx - colspan, col_idx):
                    spans[i] = (col.text.strip(), rowspan - 1)

        # 处理行末尾的跨行单元格
        while col_idx in spans:
            span_data, span_rowspan = spans[col_idx]
            row_data.append(span_data)
            if span_rowspan == 1:
                del spans[col_idx]
            else:
                spans[col_idx] = (span_data, span_rowspan - 1)
            col_idx += 1

        data.append(row_data)

    qg_index[idx]['table'] = data

with open('qg_data.json', 'w', encoding='utf-8') as f:
    json.dump(qg_index, f, indent=4, ensure_ascii=False)
print('Done.')
