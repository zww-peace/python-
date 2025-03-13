#异步的没有多线程的快，但是比普通的快多了
#也不知是服务器那边问题，还是因为我爬的次数太多了，普通的慢的不行
import aiohttp
import requests
import re
import xlwt
from bs4 import BeautifulSoup
import asyncio
import time

find_book_name = re.compile(r'<h4 class="bookname"><a href="(.*)">(.*)</a></h4>',re.S) #书的链接 书的名字
find_introduction=re.compile(r'<meta property="og:description" content="(.*?)" />',re.S) #书的简介
datalist=[]
count=0

async def download_childpage(item): #访问页面中小说简介的子页面
    # 查找符合要求的字符串
    data = []  # 保存一部电影所有信息
    item = str(item)
    name = re.findall(find_book_name, item)[0][1] #从列表中取出+从元组中取出第一个分组
    namelink = re.findall(find_book_name, item)[0][0]#从列表中取出+从元组中取出第零个分组
    async with aiohttp.ClientSession() as session:
        async with session.get(namelink) as resp:
            introduction = re.findall(find_introduction, await resp.text())#取出小说的详细简介
    data.append(name)
    if len(introduction) != 0:
        data.append(introduction[0])
    else:
        data.append('')
    data.append(namelink)
    datalist.append(data)
    print(f"{name} over!")

async def download_onepage(url): #访问每个页面是异步的
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            tasks=[]
            # 拿每一条小说记录是异步的
            for item in soup.find_all('div', class_="bookbox"):
                tasks.append(asyncio.create_task(download_childpage(item)))
            await asyncio.wait((tasks))
    print(f"{url} over!")

def saveData(datalist,savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet = book.add_sheet('po18', cell_overwrite_ok=True) #创建工作表
    col = ("书名","简介","链接")
    for i in range(0,3):
        sheet.write(0,i,col[i])  #列名
    for i in range(len(datalist)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = datalist[i]
        for j in range(0,3):
            sheet.write(i+1,j,data[j])  #数据
    book.save(savepath) #保存

async def main():
    baseurl="https://www.po18m.com/sort/0/"
    tasks=[]
    for i in range(1,11):
        tasks.append(asyncio.create_task(download_onepage(f"{baseurl}{i}.html")))
    await asyncio.wait(tasks)

    savepath = "po18.xls"
    saveData(datalist,savepath)

if __name__ == "__main__":
    time1=time.time()
    asyncio.run(main())
    time2=time.time()
    print(time2-time1)