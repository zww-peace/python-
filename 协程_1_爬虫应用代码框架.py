import asyncio
async def download(url):
    print("准备开始下载")
    await asyncio.sleep(2) #网络请求 requests.get()不好使，得用aiohttp
    print("下载完成")
async def main():
    urls=[
        "http://www.baidu.com",
        "http://www.bilibili.com",
        "http:..www.163.com"
    ]
    tasks=[]
    for url in urls:
        tasks.append(asyncio.create_task(download(url)))
    await asyncio.wait(tasks)
if __name__=="__main__":
    asyncio.run(main())