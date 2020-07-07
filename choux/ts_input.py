# -*-coding:utf8-*-
 
# 用空格获取输入数据的两种方法， map()的返回值是一个迭代器
#num1 = list(map(int, input().strip().split()))
num2 = [int(temp) for temp in input().split()]
print(num2)
