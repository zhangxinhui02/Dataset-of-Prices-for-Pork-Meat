import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

with open('prices.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

after = []
for price in data:
    if price['date'].startswith('2023') or price['date'].startswith('2024'):
        after.append(price)

for price in after:
    price['avr'] = sum(list(price['price'].values())) / len(price['price'].values())

count = 0
for price in after:
    count += price['avr']
print(f'The average price: {count/len(after)}')

with open('after.json', 'w', encoding='utf-8') as f:
    json.dump(after, f, ensure_ascii=False, indent=4)


def plot_date_series(dates_list, values_list, labels, title='Pork Price\nPrice(CNY)-Date'):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置中文字体为微软雅黑
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
    plt.figure(figsize=(15, 8))  # 设置图形的大小

    for dates, values, label in zip(dates_list, values_list, labels):
        # 将日期字符串转换为matplotlib的日期格式
        dates = [mdates.datestr2num(date) for date in dates]
        plt.plot_date(dates, values, '-', label=label)  # 绘制曲线

    # 设置图形的标题和坐标轴标签
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price(CNY)')

    # 设置日期格式
    plt.gca().tick_params(axis='x', labelsize=7)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # 设置日期间隔，此处为每5天显示一个刻度
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=20))
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记以避免重叠

    # 显示图例
    plt.legend()

    # 自动格式化日期标签，以防它们重叠
    plt.gcf().autofmt_xdate()

    # 显示图形
    # plt.show()
    plt.savefig('after-prices.png')


plot_date_series([[price['date'] for price in after]],
                 [[price['avr'] for price in after]],
                 ['avr'])
