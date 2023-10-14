###用15分钟数据来转换60分钟数据  
###由于通达信的60分钟K线数据不是整小时  说跨越自然小时的时，所以不能用resample函数实现

import os
import pandas as pd
#from pandas import Timedelta

# 读取csv文件，返回pd.DataFrame对象
def import_csv(stock_code) -> pd.DataFrame:
    df_15t = pd.read_csv(stock_code)  
    #pd.to_datetime(df[‘date’])： 将读取的数据的”date“列的值转换成日期”YY-MM-DD“形式；
    #df[“索引字符串”]: 可以返回满足条件的数据，但只想筛选一个索引时，需用切片形式如，df[“索引字符串”：“索引字符串”]
    #df.set_index(‘date’):将属性”date“设置为索引，但这个函数返回一个dateframe数据并不改变原始的数据   
    df_15t['Date'] = pd.to_datetime(df_15t['Date'])
    df_15t.set_index(['Date'], inplace=True)
    return df_15t

# 用通达信小周期，生成大周期数据
def csv_resample(df_15t,rule) -> pd.DataFrame:
     '''
    由于resample函数采样是自然小时，跟通达信的不一致  所以使用groupby函数合并来做，
    把两个15分钟数据合并成一个30分钟数据即可
    
    '''
     df_60t=df_15t
     #df_30t['Date'] = pd.to_datetime(df_30t['Date'])
     #把df_15里面的Date列 由索引变回普通列
     df_60t.reset_index(inplace=True)

     # 将Date列转换为日期时间类型，只保留年月日
     df_60t['DateDay'] = pd.to_datetime(df_60t['Date']).dt.date

     # 按照日期分组并统计行数
     date_counts = df_60t.groupby('DateDay').size().reset_index(name='count')

     # 根据条件设置temp列的值
     df_60t['temp'] = 0  # 默认为0
     # 对于行数为23的情况，设置temp为23
     df_60t.loc[df_60t['DateDay'].isin(date_counts[date_counts['count'] == 23]['DateDay']), 'temp'] = 23
     # 对于行数为15的情况，设置temp为15
     df_60t.loc[df_60t['DateDay'].isin(date_counts[date_counts['count'] == 15]['DateDay']), 'temp'] = 15

     # 创建合并规则函数
     def merge_rows(group):
         return pd.Series({
             'Date': group['Date'].iloc[-1],
             'Open': group['Open'].iloc[0],
             'High': group['High'].max(),
             'Low': group['Low'].min(),
             'Close': group['Close'].iloc[-1],
             'Volume': group['Volume'].sum()
         })

     # 筛选出DateDay列相同且temp列等于23或15的行
     mask = (df_60t['temp'] == 23) | (df_60t['temp'] == 15)

    # 使用groupby函数将前20行或前12行的数据每4行合并成一行，剩下3行合并成一行
     df_60t = df_60t[mask].groupby(['DateDay', 'temp', df_60t[mask].groupby('DateDay').cumcount() // 4]).apply(merge_rows).reset_index(drop=True)

    #把df_30t的Date恢复成索引
     df_60t.set_index("Date",inplace=True)
     return df_60t

#第二步
# 根据通达信5分钟周期数据，生成其他周期数据
def lc15_resample(filepath, name, targetdir, rule) -> None:
    # (通达信.lc5文件路径, 通达信.lc5文件名称, 处理后要保存到的文件夹)
    # 设置处理后保存文件的路径和名称
    print("周期转换已开始: " + rule)
    file_object_path = targetdir + name.split('.')[0] + ".lc" + rule[:len(rule) - 1] + '.csv'
    
    df_15t = import_csv(filepath)
    df_60t = csv_resample(df_15t,rule)
    df_60t.to_csv(file_object_path)
    print("数据转换已完成: " + name)

#第一步  
def lc15_rule(rule):
    # 设置通达信15分钟周期数据文件所在的文件夹，里面最好只有15分钟的数据文件
    path_dir = 'D:/luckly/lc5/'
    # 设置要转换的新周期
    rule_cycle = rule
    # 设置数据处理好后，要将csv文件保存的文件夹
    target_dir = 'D:/luckly/lc/'
    # 读取文件夹下的通达信.lc5.csv文件
    listfile = os.listdir(path_dir)
    # 逐个处理文件夹下的通达信.lc5.csv文件，并生成对应的csv文件，保存到对应周期文件夹下
    for fname in listfile:
        lc15_resample(path_dir + fname, fname, target_dir, rule_cycle)
    else:
        print('The for ' + path_dir + ' to ' + target_dir + '  loop is over')
        print("文件转换已完成")





# 转换成新周期，可以设置为10分钟，15分钟 ，30分钟，60分钟  通达信没有10分钟K线图
#lc5_rule('10T')
#15分钟转换数据正确
#lc5_rule('15T')
#lc15_rule('30T')
lc15_rule('60T')