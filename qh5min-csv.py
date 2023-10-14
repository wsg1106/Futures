import os
import struct
import math


# 根据二进制前两段拿到日期分时
def get_date_str(h1, h2) -> str:  # H1->0,1字节; H2->2,3字节;
    year = math.floor(h1 / 2048) + 2004  # 解析出年
    month = math.floor(h1 % 2048 / 100)  # 月
    day = h1 % 2048 % 100  # 日
    hour = math.floor(h2 / 60)  # 小时
    minute = h2 % 60  # 分钟
    if hour < 10:  # 如果小时小于两位, 补0
        hour = "0" + str(hour)
    if minute < 10:  # 如果分钟小于两位, 补0
        minute = "0" + str(minute)
    return str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute)


# 根据通达信.lc5文件，生成对应名称的csv文件
def stock_lc5(filepath, name, targetdir) -> None:
    # (通达信.lc5文件路径, 通达信.lc5文件名称, 处理后要保存到的文件夹)
    with open(filepath, 'rb') as f:  # 读取通达信.lc5文件，并处理
        file_object_path = targetdir + name + '.csv'  # 设置处理后保存文件的路径和名称
        file_object = open(file_object_path, 'w+')  # 打开新建的csv文件，开始写入数据
        title_list = "Date,Open,High,Low,Close,Open_interest,Volume,settlement_price\n"  # 定义csv文件标题
        file_object.writelines(title_list)  # 将文件标题写入到csv中

        while True:
            li2 = f.read(32)  # 读取一个5分钟数据
            if not li2:  # 如果没有数据了，就退出
                break
            data2 = struct.unpack('HHffffllf', li2)  # 解析数据
            date_str = get_date_str(data2[0], data2[1])  # 解析日期和分时

            data2_list = list(data2)  # 将数据转成list
            data2_list[1] = date_str  # 将list二个元素更改为日期 时:分
            del (data2_list[0])  # 删除list第一个元素
            for dl in range(len(data2_list)):  # 将list中的内容都转成字符串str
                data2_list[dl] = str(data2_list[dl])
            data2_str = ",".join(data2_list)  # 将list转换成字符串str
            data2_str += "\n"  # 添加换行
            file_object.writelines(data2_str)  # 写入一行数据
        file_object.close()  # 完成数据写入


# 设置通达信.day文件所在的文件夹
path_dir = 'd:\\new_tdxqh\\vipdoc\\ds\\fzline\\'
# 设置数据处理好后，要将csv文件保存的文件夹  注意python的语法，../ 的意思  lc5文件夹需要新建在qh-csv.py的上一级路径下
target_dir = '../lc5/'
# 读取文件夹下的通达信.day文件
listfile = os.listdir(path_dir)
# 逐个处理文件夹下的通达信.day文件，并生成对应的csv文件，保存到../day/文件夹下
for fname in listfile:
    stock_lc5(path_dir + fname, fname, target_dir)
else:
    print('The for ' + path_dir + ' to ' + target_dir + '  loop is over')
    print("文件转换已完成")