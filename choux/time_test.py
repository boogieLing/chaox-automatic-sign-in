# -*- coding:utf-8 -*-
from datetime import datetime

# 日期格式话模版
format_pattern = "%Y-%m-%d %H:%M:%S"
#format_pattern = "%d %H:%M"

# 具体日期 年/月/日 时/分/秒
#start_date = "2018-07-09 13:20:38"
start_date = "2020-04-10 18:22:28"
print(start_date) # datetime.datetime(2018, 10, 15, 11, 19, 52, 186250)
print(type(start_date)) # <type 'datetime.datetime'>

end_date = datetime.now()
print(end_date) # datetime.datetime(2018, 10, 15, 11, 19, 52, 186250)
print(type(end_date)) # <type 'datetime.datetime'>

# 将 'datetime.datetime' 类型时间通过格式化模式转换为 'str' 时间
end_date = end_date.strftime(format_pattern)
print(end_date, type(end_date)) # ('2018-10-15 11:21:44', <type 'str'>)

# 将 'str' 时间通过格式化模式转化为 'datetime.datetime' 时间戳, 然后在进行比较
difference = (datetime.strptime(end_date, format_pattern) - datetime.strptime(start_date, format_pattern))

# 可以获取天(days), 或者秒(seconds)
print(difference)

print(difference.seconds)
print(difference.days)




