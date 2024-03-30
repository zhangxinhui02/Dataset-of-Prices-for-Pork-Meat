import json
import re

with open('qg_data.json', 'r', encoding='utf-8') as f:
    qg_data = json.load(f)
    print(f'Loaded {len(qg_data)} indexes from qg_data.json.')

for item in qg_data:
    if '价格汇总' not in item['table'][0][0]:
        qg_data.remove(item)
        continue

data = []
for item in qg_data:
    regions = {}
    if str(item['table'][1]) in ["['大区', '省份', '涨跌幅', '标准体重生猪', '140-180公斤', '简析']",
                                 "['大区', '省份', '涨跌幅', '140公斤以内', '140-180公斤', '简析']",
                                 "['大区', '省份', '涨跌幅', '140公斤以内', '140公斤以上', '简析']"]:
        for idx, row in enumerate(item['table']):
            if idx in [0, 1]:
                continue
            if len(row) != len(item['table'][1]):
                continue
            if row[1] == '':
                continue
            regions[row[1]] = row[3]
    elif str(item['table'][1]) in ["['省份', '涨跌幅', '140公斤以内', '140公斤以上', '简析']"]:
        for idx, row in enumerate(item['table']):
            if idx in [0, 1]:
                continue
            if len(row) != len(item['table'][1]):
                continue
            if row[0] == '':
                continue
            regions[row[0]] = row[2]
    data.append(
        {
            'date': item['date'],
            'price': regions
        }
    )


def extract_numbers(text):
    # 使用正则表达式查找所有匹配的数值
    numbers = re.findall(r'\d+\.\d+|\d+', text)
    float_numbers = []
    for number in numbers:
        float_numbers.append(float(number))
    return float_numbers


def get_average(float_numbers):
    return sum(float_numbers) / len(float_numbers)


for item in data:
    price = {}
    for region, price_str in item['price'].items():
        if len(extract_numbers(price_str)) == 0:
            continue
        else:
            price[region] = get_average(extract_numbers(price_str))
    item['price'] = price

with open('prices.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
