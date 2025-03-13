#新发地改版了
#海口市菜篮子产业集团
#1.如何提取单个页面的数据
#2.上线程池，多个页面同时抓取
import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor
f=open("data.csv",mode="w",encoding="utf-8",newline="")
csvwriter=csv.writer(f)
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"}
def download_one_page(url):
    resp=requests.get(url,headers=headers)
    #print(resp.text)
    html=etree.HTML(resp.text)
    #直接从源代码右键复制xpath，因为拿到的是列表，列表每一项都是一个对象
    #这里只有一个table所以列表中只有一个对象，用[0]把它取出来
    table=html.xpath("/html/body/div[2]/div/div[2]/div[1]/div[2]/div/table")[0]
    #trs=table.xpath("./tbody/tr")[1:]
    #去掉标题那一行，名称，价格...
    #从table对象中xpath拿到所有tr对象的列表
    trs = table.xpath("./tbody/tr[position()>1]")
    #遍历列表拿到每个tr对象
    for tr in trs:
        #一行就是一个tr对象
        #从tr中拿到所有的td的内容，结果还是存在列表中，只不过因为text()，列表中的每一项是字符串
        txt = tr.xpath("./td/text()")
        #把数据存放在文件中
        csvwriter.writerow(txt)
    print(url,"提取完毕!")

if __name__=="__main__":
    开一个有5个线程的线程池
    with ThreadPoolExecutor(5) as t:
        for i in range(1,11):
            #把下载任务提交给线程池
            t.submit(download_one_page,f"http://hksclz.com/groceries/report?page={i}")
    print("全部下载完毕")



