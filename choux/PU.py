import requests,json,time
import tkinter as tk
import re
#填入Cookie
headers={
  "Cookie": "thirdRegist=0; uname=116022018039; lv=1; fid=1430; _uid=87784973; uf=b2d2c93beefa90dc08b76128269a3c07062cb23a2132f0e38556544673a9eaf645256f6716d23a19b6c33d68f1d8da1ac49d67c0c30ca5047c5a963e85f110996b716f39cac22485ce71fc6e59483dd3ad4c2cfc9b1efcabe472e25a0864046cccbca3515b932eba; _d=1586333882859; UID=87784973; vc=6EAC8A90A07F85AE44E2F8B919C35711; vc2=B5BAE7A47CCFB8B5A74D9F8B439A5904; vc3=C8BapvCHxauFZhYcYiUkoHhxsN0c2FSt11OuuPHTv1q%2BvrfcGIpoRognjVMn0GN6NiQrFTdu0YyI1EegIDILjw24%2BNAPHqflVN4HwEy465gX%2F%2B8OzIoazlzCO1Zkuv2bpg9elm%2BO6GHOdlLvfkyoSg4pen70zSd%2FK7TGrLwrO%2Fw%3D56888266c820df0b11a65f7f3009cee7; xxtenc=62edf896e007019d1f6afc185d6d6500; DSSTASH_LOG=C_38-UN_124-US_87784973-T_1586333882860; JSESSIONID=ED25D1F0B3DA126BC485AE59B5BD3710; source=""; route=25c5b3ea765bd1e462f3554e01560f4d; tl=1",
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0"
}
#填入uid
#uid="87784973"
uid=re.search(r"_uid=\d+;",headers["Cookie"]).group()[5:-1]
#print(uid)

coursedata=[]
activeList=[]
course_index=0
speed=10
status=0
status2=0
activates=[]



def backclazzdata():
    global coursedata
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
    print("获取成功")  
    #print(coursedata)  
    printdata()
    

def printdata():
    global course_index,speed
    global get_acts
    index=1
    for item in coursedata:
        print(str(index)+".课程名称:"+item['name'])
        index+=1
    #course_index=int(input("请输入序号以设定监控课程"))-1
    get_acts=[int(temp)-1 for temp in input().split()]
    
    print("监控课程设定完成")
    speed=int(input("请输入监控频率"))
    print("监控频率设置完毕")
    res=input("输入start启动监控")
    if(res=="start"):
        startsign()
    else:
        printdata    



def taskactivelist(courseId,classId):
    global activeList
    url="https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId="+str(courseId)+"&classId="+str(classId)+"&uid="+uid
    res=requests.get(url,headers=headers)
    data=json.loads(res.text)
    activeList=data['activeList']
    #print(activeList)
    for item in activeList:
        if("nameTwo" not in item):
            continue
        if(item['activeType']==2 and item['status']==1):#未签到
            signurl=item['url']
            aid = getvar(signurl)
            if(aid not in activates):
                print("【签到】查询到待签到活动 活动名称:%s 活动状态:%s 活动时间:%s aid:%s"%(item['nameOne'],item['nameTwo'],item['nameFour'],aid))
                sign(aid,uid)   

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
        print("用户:"+uid+" 签到成功！")
        activates.append(aid)
        status=2
    else:
        print("签到失败")  
        activates.append(aid)  

def startsign():
    global status,status2
    status=1
    status2=1
    ind=1
    #print("监控启动 监控课程为:%s 监控频率为:%s"%(coursedata[course_index]['name'],str(speed)))
    #print(len(get_acts))
    for item in get_acts:
    	print("监控启动 监控课程为:%s 监控频率为:%s"%(coursedata[item]['name'],str(speed)))
    cnt=1
    while(cnt!=len(get_acts) ):
    #while(status!=0 and status2!=0):
        ind+=1
        #taskactivelist(coursedata[course_index]['courseid'],coursedata[course_index]['classid'])
        for item in get_acts:
        	taskactivelist(coursedata[item]['courseid'],coursedata[item]['classid'])
        	if(status==2) :
        		status=1
        		print("%s签到成功"%coursedata[item]['name'])
        		cnt+=1
        		get_acts.remove(item)
        		
        time.sleep(speed)
        if(status==1):
        	print(str(ind)+" [签到]监控运行中，未查询到签到活动")
        #if(status==1):
            #print(str(ind)+" [签到]监控运行中，未查询到签到活动")
        #elif(status==2):
            #print(str(ind)+" [新签到]监控运行中，未查询到签到活动")         
    print("任务结束")
    printdata()
if __name__ == '__main__':
	backclazzdata()
	window.mainloop()


