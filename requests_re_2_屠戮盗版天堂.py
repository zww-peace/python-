#1.定位到2020必看片
#2.从2020必看片中提取到子页面的链接地址
#3.进入子页面链接地址，拿到我们想要下载的地址

#网站做了一些措施使得.mp4的视频链接不能正常播放，必须下载他们的应用程序，需要想办法弄清楚背后的原理和解决方案
import requests
import re
import csv

f=open("data.csv",mode="w",newline="")
csvwriter = csv.writer(f)
domain="https://www.dytt8899.com/"
resp=requests.get(domain)
resp.encoding="gb2312"  #指定字符集
#print(resp.text)
obj1=re.compile(r"2025必看热片.*?<ul>(?P<ul>.*?)</ul>",re.S)
obj2=re.compile(r"<a href='/(?P<href>.*?)' title=.*?>(?P<name>.*?)</a>",re.S)
obj3=re.compile(r'◎片　　名　(?P<name>.*?)<br />.*?<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<href>.*?)">',re.S)
result1=obj1.finditer(resp.text) #从网页中获取ul,ul内有各种电影的链接
child_href_list=[]
for it in result1:
    ul=it.group('ul')
    #提取子页面链接地址
    result2=obj2.finditer(ul)  #从ul中提取所有<a>标签中的href
    for itt in result2:
        child_href_list.append(domain+itt.group("href")) #将所有子页面的href加入到列表中

#提取子页面的内容
for href in child_href_list:
    child_resp=requests.get(href) #进入每个电影的详细介绍界面
    child_resp.encoding="gb2312"
    result3=obj3.search(child_resp.text) #提取电影的名称和下载链接
    csvwriter.writerow((result3.group("name"),result3.group("href")))



