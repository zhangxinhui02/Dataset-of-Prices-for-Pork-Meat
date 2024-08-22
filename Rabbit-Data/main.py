from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime
import json

price = {
    2024: [13.94, 14.38, 13.31, 13.65, 14.49, 14.37, 11.10, 14.06, 13.57, 12.86, 10.96, 11.13, 11.95],
    2023: [19.84, 21.00, 21.27, 20.85, 20.64, 20.86, 20.09, 19.50, 20.01, 19.87, 20.45, 20.29, 20.24, 21.04, 20.40,
           20.37, 20.38, 20.19, 21.09, 19.45, 20.35, 20.17, 19.50, 19.46, 18.04, 17.97, 18.15, 17.76, 18.47, 17.85,
           17.99, 18.93, 19.76, 16.66, 19.57, 19.49, 19.39, 19.48, 17.78, 19.20, 18.75, 18.74, 17.67, 16.07, 16.10,
           16.76, 16.58, 14.27, 14.80, 15.05, 13.85, 13.95],
    2022: [17.29, 16.10, 17.24, 17.66, 17.91, 17.12, 16.17, 17.87, 14.88, 17.29, 16.92, 16.41, 16.53, 16.55, 14.04,
           16.68, 16.42, 17.04, 15.60, 15.24, 15.24, 15.67, 16.30, 16.87, 16.72, 16.84, 16.83, 17.50, 18.96, 19.20,
           20.74, 20.70, 21.08, 21.60, 22.40, 22.55, 22.47, 21.39, 22.35, 22.49, 22.79, 22.22, 22.54, 22.93, 22.88,
           23.35, 23.11, 23.35, 20.33, 21.59, 21.11, 19.43]
}


def plot_date_series(dates_list, values_list, labels, title='Rabbit Price\nPrice(CNY)-Date'):
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
    plt.savefig('prices.png')

date = []
prices = []
summary = 0
count = 0
for i in range(2022, 2025):
    for j, k in enumerate(price[i]):
        summary += k
        count += 1
        date.append((datetime.datetime(i, 1, 1) + datetime.timedelta(weeks=j)).strftime('%Y-%m-%d'))
        prices.append(k)
print(f'The average price of rabbit: {summary / count}')
plot_date_series([date], [prices], ['全国'])
