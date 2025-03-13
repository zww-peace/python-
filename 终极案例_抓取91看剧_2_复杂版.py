#m3u8的url不在视频播放页面的网页源代码中，简单版的是在
#iframe是在网页中再嵌入一个网页
#搜索的视频页面源代码没有视频相关内容，通过iframe嵌入另外一个网页专门用来播视频
#右键点不了，可以通过F12或ctrl+u来获取页面源代码

#搜索视频页面源代码->iframe url->iframe页面源代码->m3u8 url->m3u8文件内容->index.m3u8 url->index.m3u8文件 存放视频的ts路径

"""
思路：
    1.拿到主页面的页面源代码，找到iframe的url
    2.从iframe的页面源代码中拿到m3u8文件
    3.下载第一层m3u8文件 -> 文件中存储第二层m3u8的url -> 下载第二层m3u8文件(视频存放路径)
    4.下载视频
    5.下载秘钥，进行解密操作
    6.合并所有ts文件为一个mp4文件
"""
import aiofiles
import requests
import re
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import os
#AES加解密
from Crypto.Cipher import AES

#找到iframe页面对应的url
def get_iframe_src(url):
    resp=requests.get(url)
    main_page = BeautifulSoup(resp.text,"html.parser")
    src = main_page.find("iframe").get("src") #找到iframe标签，获得src属性值
    #获得第一层iframe的url
    return src

#找到第一层m3u8的url
def get_first_m3u8_url(url):
    resp = requests.get(url)
    obj=re.compile(r'var main ="(?P<m3u8_url>.*?)"',re.S)
    m3u8_url = obj.search(resp.text).group("m3u8_url")
    #返回第一层m3u8的url
    return m3u8_url

#下载m3u8文件(第一层和第二层代码共用)
def download_m3u8_file(url,name):
    resp = requests.get(url)
    #将m3u8的文件内容写入name文件中
    with open(name,mode="wb") as f:
        f.write(resp.content)

#下载ts文件
async def download_ts(url,name,session):
    async with session.get(url) as resp:
        async with aiofiles.open(f"video2/{name}",mode="wb") as f:
            await f.write(await resp.content.read()) #把下载的内容写入到文件中
    print(f"{name}下载完毕")

#download上层的一个包装
async def aio_download(up_url): #up_url="https://boba.52kuyun.com/20170906/Moh219zV/hls/"
    tasks=[]
    async with aiohttp.ClientSession() as session: #提前准备好session
        async with aiofiles.open("越狱第一季第一集_second_m3u8.txt",mode="r",encoding="utf-8") as f:
            async for line in f:
                if line.startswith("#"):
                    continue
                #line就是xxxxxx.ts
                line = line.strip() #去掉没用的空格和换行
                #拼接真正的ts路径
                # https://boba.52kuyun.com/20170906/Moh219zV/hls/cFN8o3436000.ts
                ts_url = up_url+line
                task = asyncio.create_task(download_ts(ts_url,line,session))#创建任务
                tasks.append(task)

            await asyncio.wait(tasks) #等待任务结束
    print("全部下载完毕")

def get_key(url):
    resp=requests.get(url)
    return resp.text

async def dec_ts(name,key):
    aes = AES.new(key=key, IV=b"0000000000000000",mode=AES.MODE_CBC)
    async with aiofiles.open(f"video2/{name}",mode="rb") as f1: #读文件
        async with aiofiles.open(f"video2/temp_{name}",mode="wb") as f2: #解密，存入新文件
            bs = await f1.read()#从源文件读取内容
            await f2.write(aes.decrypt(bs))#把解密好的内容写入文件
    print(f"{name}处理完毕")


async def aio_dec(key):
    #解密
    tasks=[]
    async with aiofiles.open("越狱第一季第一集_second_m3u8.txt",mode="r",encoding="utf-8") as f:
        async for line in f:
            if line.startswith("#"):
                continue
            line=line.strip()
            #开始创建异步任务
            task = asyncio.create_task(dec_ts(line,key))
            tasks.append(task)
        await asyncio.wait(tasks)

def merge_ts():
    # mac: cat 1.ts 2.ts 3.ts > xxx.mp4
    # windows: copy /b 1.ts+2.ts+3.ts xxx.mp4
    lst=[]
    with open("越狱第一季第一集_second_m3u8.txt",mode="r",encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            line=line.strip()
            list.append(f"video2/temp_{line}")
    s=" ".join(lst) # 1.ts 2.ts 3.ts
    os.system(f"cat {s} > movie.mp4")
    print("搞定")
########################################################################
#windows是用\来分割文件夹!!!!!!!!!!!!!!!!!!!!!
#貌似路径中不能有中文
def windows_merge_ts():
    list=[]
    for i in range(1,12):
        list.append(f"video\{i}.ts")
    d=" + ".join(list)
    os.system(f'copy /b {d} video\movie2.ts')
#########################################################################
def main(url):
    #1.拿到主页面的页面源代码，找到iframe对应的url
    iframe_src = get_iframe_src(url)
    #2.拿到第一层的m3u8文件的下载地址
    first_m3u8_url = get_first_m3u8_url(iframe_src)
    #拿到iframe的域名
    #iframe_src = "https://boba.52kuyun.com/share/xfPs9NPHvYGhNzFp"
    iframe_domain = iframe_src.split("/share")[0]
    #拼接出第一层m3u8真正的下载路径
    first_m3u8_url = iframe_domain+first_m3u8_url
    #3.1下载第一层m3u8文件
    download_m3u8_file(first_m3u8_url,"越狱第一季第一集_first_m3u8.txt")
    #3.2下载第二层m3u8文件
    with open("越狱第一季第一集_first_m3u8.txt",mode="r",encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            else:
                line = line.strip() #去掉空白或换行符 hls/index.m3u8
                #准备拼接第二层m3u8的下载路径
                #https://boba.52kuyun.com/20170906/Moh219zV/ + hls/index.m3u8
                #https://boba.52kuyun.com/20170906/Moh219zV/hls/index.m3u8
                second_m3u8_url = first_m3u8_url.split("index.m3u8")[0] + line
                #下载第二层m3u8文件内容
                download_m3u8_file(second_m3u8_url,"越狱第一季第一集_second_m3u8.txt")
    # 4.下载视频
    second_m3u8_url_up = second_m3u8_url.replace("index.m3u8","")
    # 异步协程
    #tasks上层的一个包装
    asyncio.run(aio_download(second_m3u8_url_up))
    #5.1拿到秘钥
    key_url = second_m3u8_url_up+"key.key" #偷懒写法，正常应该去m3u8文件里去找
    key = get_key(key_url)
    #5.2解密
    asyncio.run(aio_dec(key))

    #6.合并ts文件为mp4文件
    merge_ts()


if __name__ == "__main__":
    url = "https://www.91kanju.com/vod-play/541-2-1.html"
    main(url)

