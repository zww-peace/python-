import requests
import re
import csv
url="https://movie.douban.com/top250"
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"}
resp=requests.get(url,headers=headers)
page_content=resp.text

#解析数据
obj=re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
               r'</span>.*?<p>.*?<br>(?P<year>.*?)&nbsp.*?<span '
               r'class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
               r'<span>(?P<num>.*?)人评价</span>',re.S)
result=obj.finditer(page_content)
f=open("data.csv",mode="w",newline="") #newline使得输出的.csv文件没有空行
csvwriter=csv.writer(f)
for it in result:
    dic=it.groupdict()
    dic['year']=dic['year'].strip()
    csvwriter.writerow(dic.values())
    # print(it.group("name"),end="\t")
    # print(it.group("score"), end="\t")
    # print(it.group("num"), end="\t")
    # print(it.group("year").strip())
f.close()
print("over!")