#1.拿到主页面的源代码，然后提取到子页面的下载链接,href
#2.通过href拿到子页面的内容，从子页面中找到图片的下载地址 img -> src
#3.下载图片


import requests
from bs4 import BeautifulSoup
import time

url="http://umei.cc/bizhitupian/shoujibizhi/"
resp=requests.get(url)
resp.encoding="utf-8"

main_page=BeautifulSoup(resp.text,"html.parser")
div_list=main_page.find("div",class_="item_list infinite_scroll").find_all("div",class_="btns")
for div in div_list:
    a=div.find("a")
    href="http://umei.cc"+a.get("href")
    child_page_resp=requests.get(href)
    child_page_resp.encoding="utf-8"
    child_page_text=child_page_resp.text
    #从子页面中拿到图片的下载路径
    child_page=BeautifulSoup(child_page_text,"html.parser")
    img_src=child_page.find("div",class_="big-pic").find("img").get("src")
    #下载图片
    img_resp=requests.get(img_src)
    img_name=img_src.split("/")[-1]
    with open("img/"+img_name,mode="wb") as f:
        f.write(img_resp.content)
    print("over!",img_name)
    time.sleep(1)

print("all over!")
