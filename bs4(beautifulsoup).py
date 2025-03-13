#1.拿到页面源代码
#2.使用bs4进行解析，拿到具体数据
#beautifulsoup是通过标签查找数据
import requests
from bs4 import BeautifulSoup
import csv
url="http://hksclz.com/groceries/index"
resp=requests.get(url)

f=open("菜价.csv",mode="w",encoding="gbk")
csvwriter =csv.writer(f)
#解析数据
#1.把页面源代码交给Beautifulsoup进行处理，生成bs对象
page=BeautifulSoup(resp.text,"html.parser")#指定html的解析器
#2.从bs对象中查找数据
#find(标签,属性=值) 只找第一个
#find_all(标签,属性=值)找出所有的
#div=page.find("div",attrs={"class":"box_out_form box_out_form2"})
div=page.find("div", class_="box_out_form box_out_form2")#class是python的关键字
table=div.find("table")
#拿到所有的数据行
trs=table.find_all("tr")[1:] #扔掉第零行标题行
for tr in trs:
    tds=tr.find_all("td")#查找每行的所有列
    name=tds[1].text
    price=tds[2].text
    csvwriter.writerow([name,price])
f.close()
print("over!")