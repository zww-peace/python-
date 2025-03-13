#requests.get() 同步的代码 -> 异步操作aiohttp
import aiohttp
import asyncio
urls=[
    "https://www.umei.cc/d/file/20230906/40c9143511b058a6da7843458b52f319.jpg",
    "https://www.umei.cc/d/file/20230428/cf883de8e90a08d6c774c88330593588.jpg",
    "https://www.umei.cc/d/file/20230215/07686282057963876a24523d1a826bff.jpeg",
    "https://www.umei.cc/d/file/20230913/fe68e1f4915f7082c4a1b480fd573c95.jpg"
]
async def aiodownload(url):
    name=url.rsplit("/",1)[1] #从右边切，切一次，得到[1]位置的内容
    #aiohttp.ClientSession<=>requests
    #用with自动close
    async with aiohttp.ClientSession() as session: #requests
        async with session.get(url) as resp: #resp = requests.get()
            with open(name,mode="wb") as f: #创建文件
                f.write(await resp.content.read()) #读取内容是异步的，需要await挂起
            #resp.content.read()  #等价于requests中的resp.content
            #resp.text() #返回页面源代码
            #resp.json()
    #发送请求
    #得到图片内容
    #保存到文件
    print(name,"搞定")
async def main():
    tasks=[]
    for url in urls:
        tasks.append(asyncio.create_task(aiodownload(url)))
    await asyncio.wait(tasks)
if __name__ == "__main__":
    asyncio.run(main())