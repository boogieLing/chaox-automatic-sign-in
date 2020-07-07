import requests,json,time
import tkinter as tk
from tkinter import messagebox
import re
import os
import threading
from datetime import datetime

# 日期格式话模版
format_pattern = "%Y-%m-%d %H:%M"
#填入Cookie
headers={
  "Cookie": "unkown",
  #"Cookie": "thirdRegist=0; uname=116022018039; lv=1; fid=1430; _uid=87784973; uf=b2d2c93beefa90dc08b76128269a3c07062cb23a2132f0e38556544673a9eaf645256f6716d23a19b6c33d68f1d8da1ac49d67c0c30ca5047c5a963e85f110996b716f39cac22485ce71fc6e59483dd3ad4c2cfc9b1efcabe472e25a0864046cccbca3515b932eba; _d=1586333882859; UID=87784973; vc=6EAC8A90A07F85AE44E2F8B919C35711; vc2=B5BAE7A47CCFB8B5A74D9F8B439A5904; vc3=C8BapvCHxauFZhYcYiUkoHhxsN0c2FSt11OuuPHTv1q%2BvrfcGIpoRognjVMn0GN6NiQrFTdu0YyI1EegIDILjw24%2BNAPHqflVN4HwEy465gX%2F%2B8OzIoazlzCO1Zkuv2bpg9elm%2BO6GHOdlLvfkyoSg4pen70zSd%2FK7TGrLwrO%2Fw%3D56888266c820df0b11a65f7f3009cee7; xxtenc=62edf896e007019d1f6afc185d6d6500; DSSTASH_LOG=C_38-UN_124-US_87784973-T_1586333882860; JSESSIONID=ED25D1F0B3DA126BC485AE59B5BD3710; source=""; route=25c5b3ea765bd1e462f3554e01560f4d; tl=1",
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0"
}
# #填入uid
# #uid="87784973"
# uid=re.search(r"_uid=\d+;",headers["Cookie"]).group()[5:-1]
# #print(uid)
tmp_cookies="''"
tmp_user_agent="''"
if (os.path.exists("chou_config.r0")==True) :
    f = open("chou_config.r0","r")   #设置文件对象
    line = f.readline()
    line = line[:-1]
    r_pos= 0
    while line:             #直到读取完文件
        line = f.readline()  #读取一行文件，包括换行符
        print(line)
        line = line[:-1]     #去掉换行符，也可以不去
        if r_pos==0:
            tmp_cookies=line
        elif r_pos==1:
            tmp_user_agent=line
        r_pos+=1
        if line=="__END__" :
            break
    f.close() #关闭文件
else:
    with open("chou_config.r0","w") as f :
        f.writelines("__BEGIN__\n")
        f.writelines("\"unknown\"\n")
        f.writelines("\"Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0\"\n")
        f.writelines("__END__")
        tmp_cookies="\"unknown\""
        tmp_user_agent="\"Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0\""
    f.close() #关闭文件

##############文件初始化############################
coursedata=[]
activeList=[]
course_index=0
speed=10
status=0
status2=0
activates=[]
already_sel=[]
######################################################
#实例化object
window = tk.Tk()
window.title('Choux killer')
window.geometry('335x520')
window.resizable(0,0)
 
f_8 = tk.Frame(window)
f_8.place(x=100,y=375)
var_4 = tk.StringVar()
l_5 = tk.Label(f_8, width=30,textvariable=var_4)
l_5.pack()
######################################################
f_9 = tk.Frame(window)
f_9.place(x=20,y=410)
l_4 = tk.Label(f_9, width=10, text='Cookies:')
l_5 = tk.Label(f_9, width=10, text='User-agent:')
l_4.pack()
l_5.pack()

f_10 = tk.Frame(window)
f_10.place(x=150,y=410)
cookies = tk.StringVar()
entry_1 = tk.Entry(f_10,width=20,textvariable=cookies)
entry_1.insert(0,tmp_cookies)
entry_1.pack()

user_agent = tk.StringVar()
entry_2 = tk.Entry(f_10,width=20,textvariable=user_agent)
entry_2.insert(0,tmp_user_agent)
entry_2.pack()
######################################################
headers["Cookie"]=cookies.get()
headers["User-Agent"]=user_agent.get()
uid="00000000"
tmp_uid=re.search(r"_uid=\d+;",headers["Cookie"])
if tmp_uid:
    uid=tmp_uid.group()[5:-1]
    print(uid)
else :
    uid="00000000"

###################################################### 
def backclazzdata():
    global coursedata
    global speed
    url="http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"
    res=requests.get(url,headers=headers)
    cdata=json.loads(res.text)
    if(cdata['result']!=1):
        print("课程列表获取失败")
        return 0
    for item in cdata['channelList']:
        if("course" not in item['content']):
            continue
        pushdata={}
        pushdata['courseid']=item['content']['course']['data'][0]['id']
        pushdata['name']=item['content']['course']['data'][0]['name']
        pushdata['imageurl']=item['content']['course']['data'][0]['imageurl']
        pushdata['classid']=item['content']['id']
        coursedata.append(pushdata)
    var_4.set("获取成功")  
    #print(coursedata)  
    #printdata()
    return coursedata

def taskactivelist(courseId,classId):
    global activeList
    global already_sel
    url="https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId="+str(courseId)+"&classId="+str(classId)+"&uid="+uid
    res=requests.get(url,headers=headers)
    data=json.loads(res.text)
    activeList=data['activeList']
    #print(activeList)
    for item in activeList:
        if("nameTwo" not in item):
            continue
        if(item['activeType']==2 and item['status']==1):
            signurl=item['url']
            aid = getvar(signurl)
            if(aid not in activates):
                var_4.set("【签到】查询到待签到活动 活动名称:%s 活动状态:%s 活动时间:%s aid:%s"%(item['nameOne'],item['nameTwo'],item['nameFour'],aid))
                print("【签到】查询到待签到活动 活动名称:%s 活动状态:%s 活动时间:%s aid:%s"%(item['nameOne'],item['nameTwo'],item['nameFour'],aid))
                sign(aid,uid)
                #return #此处删除return就可以同时签到   

def getvar(url):
    var1 = url.split("&")
    for var in var1:
        var2 = var.split("=")
        if(var2[0]=="activePrimaryId"):
            return var2[1]
    return "ccc"    

  

def sign(aid,uid):
    global status,activates
    url="https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId="+aid+"&uid="+uid+"&clientip=&latitude=-1&longitude=-1&appType=15&fid=0"
    res=requests.get(url,headers=headers)
    if(res.text=="success"):
        var_4.set("用户:"+uid+" 签到成功！")
        activates.append(aid)
        status=2
    else:
        var_4.set("签到失败")  
        activates.append(aid)  

def startsign( sp ):
    global status,status2
    
    status=1
    status2=1

    for item in already_sel:
        var_4.set("监控课程为:%s 监控频率为:%s"%(coursedata[item]['name'],str(sp)))
        print("监控课程为:%s 监控频率为:%s"%(coursedata[item]['name'],str(sp)))
    for item in already_sel:
        var_4.set("课程未签到:%s"%(coursedata[item]['name']))
        print("课程未签到:%s"%(coursedata[item]['name']))
        taskactivelist(coursedata[item]['courseid'],coursedata[item]['classid'])
        if( status==2 ):#操作成功
            print("课程签到成功:%s"%(coursedata[item]['name']))
            var_4.set("课程签到成功:%s"%(coursedata[item]['name']))
            already_sel.remove(item)
            return 1
    return 0   

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 打包进线程（耗时的操作）
#@staticmethod
def thread_it(func, *args):
    t = threading.Thread(target=func, args=args) 
    t.setDaemon(True)  
    t.start()           # 启动
    # t.join()          # 阻塞--会卡死界面！

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
f_1 = tk.Frame(window)
f_1.place(x=150,y=10)

f_2 = tk.Frame(window)
f_2.place(x=150,y=220)

f_3 = tk.Frame(window)
f_3.place(x=150,y=190)
f_4 = tk.Frame(window)
f_4.place(x=237,y=190)
var_1 = tk.StringVar()  # 创建变量，用var1用来接收鼠标点击具体选项的内容
var_2 = tk.StringVar()
l_1 = tk.Label(f_1, width=20, text='Selection waited')
l_2 = tk.Label(f_2, width=20, textvariable=var_2)

l_1.pack()
l_2.pack()

lb = tk.Listbox(f_1,width=20,height=7)  #5条信息
lc = tk.Listbox(f_2,width=20,height=3)  #5条信息

index=1
try:
    for item in backclazzdata():
        lb.insert('end',str(index)+":"+item['name'])
        index+=1
except Exception as e :
    print(e)
    
start_time = tk.StringVar()
entry_3 = tk.Entry(f_2,width=20,textvariable=start_time)
entry_3.pack()
start_time.set(datetime.now().strftime(format_pattern))#显示启动时间
#target_time=start_time.get()

lb.pack()
lc.pack()
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def print_selection():
    global already_sel
    value = lb.get(lb.curselection())   # 获取当前选中的文本
    #var_1.set(value)  # 为label设置值
    number_now=int(re.search(r"\d+",value).group())-1
    #print(already_sel,number_now)
    if(number_now not in already_sel):
        already_sel.append(number_now)
        lc.insert('end',value)
    #print(already_sel)
    lenth=len(already_sel) 
    var_2.set( "Selecetd:"+str(lenth) )
    
    return value
    
def clear_list():
    lc.delete(0, 'end')
    already_sel.clear()
    var_2.set( "Selecetd:"+str(0) )
    
b1 = tk.Button(f_3, text='ADD', width=6, height=1, command=print_selection)
b1.pack()
b2 = tk.Button(f_4, text='ClEAR', width=6, height=1, command=clear_list)
b2.pack()    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
f_5 = tk.Frame(window)
f_5.place(x=-15,y=10)

speed_v = tk.StringVar()
def print_selection_s(v):
    l_3.config(text='Speed selected ' + v)
    #speed=v #这是没用的！
    
l_3 = tk.Label(f_5, width=20, text='Speed(s)')
s = tk.Scale(f_5, from_=10, to=360, length=318, 
            showvalue=1,
            tickinterval=36, 
            resolution=10, 
            variable=speed_v,  # 绑定变量
            command=print_selection_s)
l_3.pack()
s.pack()
######################################################
def write_in_config():
    with open("chou_config.r0","w") as f :
        f.writelines("__BEGIN__\n")
        f.writelines(cookies.get())
        f.writelines("\n")
        f.writelines(user_agent.get())
        f.writelines("\n")
        f.writelines("__END__")
    f.close() #关闭文件
    headers["Cookie"]=cookies.get()
    headers["User-Agent"]=user_agent.get()
    index=1
    try:
        for item in backclazzdata():
            lb.insert('end',str(index)+":"+item['name'])
            index+=1
    except Exception as e :
        print(e)
######################################################

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
f_6 = tk.Frame(window)
f_6.place(x=20,y=370)

#f_7 = tk.Frame(window)
#f_7.place(x=150,y=375)
#var_3 = tk.StringVar()
#l_4 = tk.Label(f_7, width=20,textvariable=var_3)
def go_start():
    speed=int(speed_v.get())
    while(True):
        #var_3.set("Speed is %d s, done :%d"%(speed,cnt))
        target_time=start_time.get()
        now_time=datetime.now()
        now_time=now_time.strftime(format_pattern)
        #通过格式化模式转换为 'str' 时间
        print("target time is %s\t"%(target_time))
        print("now time is %s\t"%(datetime.now().strftime(format_pattern)))
        difference = (datetime.strptime(now_time, format_pattern) - datetime.strptime(target_time, format_pattern))
        print(difference.seconds)
        if(difference.days<0 ):#days<0是未到时间
            var_4.set("未开始监控")
            time.sleep(60)#一分钟检测一次呗
            continue
        
        if(startsign(speed)!=0 and len(already_sel)==0):
            break
        var_4.set("Waiting number:%s"%(str(already_sel)))
        time.sleep(speed)
    
def go_s(event=None):
    thread_it(go_start)

b3 = tk.Button(f_6, text='START', width=10, height=1, command=go_s)
b3.pack()
#l_4.pack()

f_11 = tk.Frame(window)
f_11.place(x=20,y=470)
b4 = tk.Button(f_11, width=33,  command=write_in_config)
b4.pack()
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def fun_Info(event):
    messagebox.showinfo('Arter Infomation',\
                        "Autor:R0\nEmail:boogieling_o@qq.com\nCopyright © 2020 Ling rights reserved.")
if __name__ == '__main__':
    #backclazzdata()
    window.bind("<Tab>",fun_Info)#响应按键
    
    
    window.mainloop()


