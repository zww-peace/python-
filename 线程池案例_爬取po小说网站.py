import requests
from concurrent.futures import ThreadPoolExecutor
import re
import xlwt
from bs4 import BeautifulSoup

find_book_name = re.compile(r'<h4 class="bookname"><a href="(.*)">(.*)</a></h4>',re.S) #书的链接 书的名字
find_introduction=re.compile(r'<meta property="og:description" content="(.*?)" />',re.S) #书的简介
datalist=[]
count=0
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"}
#创建第二个线程池，用于每个页面中30条小说记录的并发访问
threadPool = ThreadPoolExecutor(max_workers=50, thread_name_prefix="test_")
def download_childpage(item): #访问页面中小说简介的子页面
    # 查找符合要求的字符串
    data = []  # 保存一部电影所有信息
    item = str(item)
    name = re.findall(find_book_name, item)[0][1] #从列表中取出+从元组中取出第一个分组
    namelink = re.findall(find_book_name, item)[0][0]#从列表中取出+从元组中取出第零个分组
    html2 = requests.get(namelink,headers=headers)
    html2.encoding="utf-8"
    introduction = re.findall(find_introduction, html2.text)#取出小说的详细简介
    data.append(name)
    if len(introduction) != 0:
        data.append(introduction[0])
    else:
        data.append('')
    data.append(namelink)
    datalist.append(data)
    print(f"{name} over!")
def download_onepage(url): #访问一个页面
    resp=requests.get(url,headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    #拿到每一条小说记录送入线程池处理
    for item in soup.find_all('div', class_="bookbox"):
        threadPool.submit(download_childpage,item)
    print(f"url over!")

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

if __name__ == "__main__":
    baseurl="https://www.po18m.com/sort/0/"
    # 创建第一个线程池，用于多页面之间并发访问(每个页面有50条小说介绍)
    with ThreadPoolExecutor(5) as t:
        for i in range(1,11):
            t.submit(download_onepage,f"{baseurl}{str(i)}.html")
    print("全部下载完毕")

    threadPool.shutdown(wait=True)
    savepath = "po18.xls"
    saveData(datalist,savepath)