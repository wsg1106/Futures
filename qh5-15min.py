###为了达到跟通达信周期一样的k线效果，这里只用来做15分钟数据，其他周期另外合并

import os
import pandas as pd
from pandas import Timedelta

# 读取csv文件，返回pd.DataFrame对象
def import_csv(stock_code) -> pd.DataFrame:
    df = pd.read_csv(stock_code)
    #把date列设置为时间格式
    df['Date'] = pd.to_datetime(df['Date'])
    #把date列设置为索引
    df.set_index(['Date'], inplace=True)
    return df

# 用通达信小周期，生成大周期数据
def csv_resample(df, rule) -> pd.DataFrame:
    # 重新采样Open列数据
    #通常是由于在使用resample函数后，索引重新排列导致的。resample函数默认会对时间序列数据进行重新采样，并重新排序索引。
    df_open = round(df['Open'].resample(rule=rule, closed='right',label='right').first(), 2)
    df_high = round(df['High'].resample(rule=rule, closed='right',label='right').max(), 2)
    df_low = round(df['Low'].resample(rule=rule, closed='right',label='right').min(), 2)
    df_close = round(df['Close'].resample(rule=rule, closed='right',label='right').last(), 2)
    df_volume = round(df['Volume'].resample(rule=rule, closed='right',label='right').sum(), 2)
    # print("新周期数据已生成")
    # 生成新周期15分钟数据
    df_15t = pd.DataFrame()
    df_15t = df_15t.assign(Open=df_open)
    df_15t = df_15t.assign(High=df_high)
    df_15t = df_15t.assign(Low=df_low)
    df_15t = df_15t.assign(Close=df_close)
    df_15t = df_15t.assign(Volume=df_volume)
    # 去除空值
    df_15t = df_15t.dropna()
    
    
    #把df_15里面的Date列 由索引变回普通列
    df_15t.reset_index(inplace=True)
    
    # 根据 Date 列的日期进行升序排序
    df_15t['Date'] = pd.to_datetime(df_15t['Date'])  # 确保 Date 列是 datetime 类型
    df_15t = df_15t.sort_values(by='Date')

    # 创建一个新列'temp'，根据'Date'列中的时间是否大于15点进行赋值
    df_15t['temp'] = (df_15t['Date'].dt.hour > 15).astype(int)

    # 添加一个新列'DateDay'，该列包含了日期的天数部分
    df_15t['DateDay'] = df_15t['Date'].dt.date
    # 使用 custom_sort_key 列进行排序
    df_15t = df_15t.sort_values(by=['DateDay','temp'],ascending=[1,0])

    # 删除 temp列  DateDay列
    df_15t = df_15t.drop(['temp','DateDay'], axis=1)

    #把df_15t的Date恢复成索引
    df_15t.set_index("Date",inplace=True)
    
    return df_15t
    


# 根据通达信5分钟周期数据，生成其他周期数据
def lc5_resample(filepath, name, targetdir, rule) -> None:
    # (通达信.lc5文件路径, 通达信.lc5文件名称, 处理后要保存到的文件夹)
    # 设置处理后保存文件的路径和名称
    print("周期转换已开始: " + rule)
    file_object_path = targetdir + name.split('.')[0] + ".lc" + rule[:len(rule) - 1] + '.csv'
    df = import_csv(filepath)


    df = csv_resample(df, rule)
 
    df.to_csv(file_object_path)
    print("数据转换已完成: " + name)


def lc5_rule(rule):
    # 设置通达信5分钟周期数据文件所在的文件夹
    path_dir = 'D:/luckly/lc5/'
    # 设置要转换的新周期15分钟
    rule_cycle = rule
    # 设置数据处理好后，要将csv文件保存的文件夹
    target_dir = 'D:/luckly/lc/'
    # 读取文件夹下的通达信.lc5.csv文件
    listfile = os.listdir(path_dir)
    # 逐个处理文件夹下的通达信.lc5.csv文件，并生成对应的csv文件，保存到对应周期文件夹下
    for fname in listfile:
        lc5_resample(path_dir + fname, fname, target_dir, rule_cycle)
    else:
        print('The for ' + path_dir + ' to ' + target_dir + '  loop is over')
        print("文件转换已完成")


# 转换成新周期
#lc5_rule('10T')
lc5_rule('15T')
#lc5_rule('30T')
#lc5_rule('60T')