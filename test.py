import pandas
import numpy as np
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False


# 为字典中的x添加统计数量的函数
def dict_add(the_dict, x):
    if x in the_dict.keys():
        the_dict[x] += 1
    else:
        the_dict[x] = 1


# 将字典转化为列表的函数
def dict_to_list(the_dict):
    the_list = []
    for key, value in zip(the_dict.keys(), the_dict.values()):
        the_list.append((int(value), key))
    return the_list


# 画直方图函数，传入的列表是二元列表，列表元素0为值，列表元素1为该值对应的对象名
def draw_bar(the_list, the_xlabel, the_ylabel, title, color=None, x_is_digit=False):
    # 先将数据列表转化为numpy的array
    the_array = np.array(the_list)
    # x轴刻度
    if x_is_digit:
        x = [int(i) for i in the_array[:, 1]]
    else:
        x = the_array[:, 1]

    # y轴刻度，如果不将y轴的刻度转为数字类型，则会画得很丑，不按数字的值大小来画
    y = [int(i) for i in the_array[:, 0]]

    plt.figure(figsize=(40, 20))
    plt.bar(x, y, color=color, width=0.5)
    plt.xlabel(the_xlabel)
    plt.ylabel(the_ylabel)
    plt.xticks(x, x, rotation=45)
    plt.title(title)
    plt.savefig(title + '.png')
    plt.show()


# 画散点图函数，传入一个numpy的array，并且该array每行的第一个元素是x轴数据，第二个元素是y轴数据
def draw_scatter(numpy_array, the_xlabel, the_ylabel, title):
    # x轴数据
    x_data = [int(i) for i in numpy_array[:, 0]]
    # y轴数据
    y_data = [int(i) for i in numpy_array[:, 1]]

    plt.figure(figsize=(40, 20))
    plt.scatter(x_data, y_data, marker='o', c='red')
    plt.xlabel(the_xlabel)
    plt.ylabel(the_ylabel)
    plt.xticks(range(0, len(x_data), 5), range(0, max(x_data), 5))
    plt.title(title)
    plt.savefig(title+'.png')
    plt.show()


# 将数据整合、按从小到大排序后输出为numpy的array
def get_numpy_array(data1, data2):
    the_list = []
    for x, y in zip(data1, data2):
        the_list.append([int(x), int(y)])
    the_list = sorted(the_list)
    return np.array(the_list)


if __name__ == '__main__':
    data = pandas.read_csv('data/movie250.csv', encoding='gbk')
    movie10 = data[:10]

    print('第一题，前十行数据：\n', movie10, '\n')

    # 下面是第二题
    area_dict = {}
    area_data = data['area']
    for x in area_data:
        temp_list = str(x).split(' ')
        has_china = False
        for item in temp_list:
            item_str = str(item)
            if '中国' in item_str:
                if has_china is False:
                    has_china = True
                    dict_add(area_dict, '中国')
            elif '香港' in item_str or '台湾' in item_str:
                if has_china is False:
                    has_china = True
                    dict_add(area_dict, '中国')
            else:
                dict_add(area_dict, item)

    area_list = dict_to_list(area_dict)

    # 将列表按照第一位元素（也就是上榜次数）排序
    area_list20 = sorted(area_list, reverse=True)[:20]

    print('第二题，统计上榜次数最多的20个国家：\n', area_list20)
    draw_bar(area_list20, '国家地区', '上榜次数', '豆瓣Top250影片的制片国家地区及其上榜次数情况直方图')

    # 下面是第三题
    cast_dict = {}
    cast_data = data['cast']
    for x in cast_data:
        temp_list = str(x).split("', '")
        for item in temp_list:
            dict_add(cast_dict, item)

    # 将字典转换为列表
    cast_list = dict_to_list(cast_dict)

    # 将列表按照第一位元素（也就是上榜次数）排序
    cast_list8 = sorted(cast_list, reverse=True)[:8]
    print('第三题，统计统计上榜次数最多的8名演员（按顺序排名）：\n', cast_list8)
    draw_bar(cast_list8, '演员名称', '上榜次数', '上榜次数最多的8名演员情况直方图', color=['r', 'g', 'b', 'y', 'r', 'g', 'b', 'y'])

    print('第四题，统计并分析排名与电影时长的关系：\n')
    time_num_array = get_numpy_array(data['num'], data['movie_duration'])
    draw_scatter(time_num_array, '电影排名', '电影时长', '电影时长与电影排名的关系散点图')

    time_times_dict = {}
    for x in data['movie_duration']:
        dict_add(time_times_dict, x)
    time_times_list = dict_to_list(time_times_dict)
    time_times_list = sorted(time_times_list, key=lambda temp: temp[1])
    draw_bar(time_times_list, '电影时长', '频率', '电影时长的频率分布直方图', x_is_digit=True)

    print('第五题，统计并分析排名与评论人数的关系：\n')
    comment_num_array = get_numpy_array(data['num'], data['comment_num'])
    draw_scatter(comment_num_array, '电影排名', '评论人数', '电影排名与评论人数的关系散点图')

    print('第六题，统计并分析排名与上映时间的关系：\n')
    num_init_year_array = get_numpy_array(data['num'], data['init_year'])
    draw_scatter(num_init_year_array, '电影排名', '上映时间', '电影排名与上映时间的关系散点图')
