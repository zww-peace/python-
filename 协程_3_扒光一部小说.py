#直接搜西游记百度小说就是视频里那个代码
#章节内部的内容
#https://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4306063500","cid":"4306063500|1569782244","need_bookinfo":1}
import json
import aiofiles
import requests
import asyncio
import aiohttp
"""
1.同步操作：访问getCatalog 拿到所有章节的cid和名称
2.异步操作：访问getChapterContent 下载所有的文章内容
"""
bookid = "4306063500"
async def aiodownload(cid,title):
    data={
        "book_id":bookid,
        "cid":f"{bookid}|{cid}",
        "need_bookinfo":1
    }
    data=json.dumps(data)
    url=f"https://dushu.baidu.com/api/pc/getChapterContent?data={data}"
    async with aiohttp.ClientSession() as session: #异步的requests
        async with session.get(url) as resp:
            dic=await resp.json()
            async with aiofiles.open(f"novel/{title}",mode="w",encoding="utf-8") as f:
                await f.write(dic["data"]["novel"]["content"]) #把小说内容写入文件

async def getCatalog(url):
    resp = requests.get(url)
    dic = resp.json()
    tasks=[]
    # item就是对应每一个章节的title和chapter_cid
    for item in dic["data"]["novel"]["items"]:
        title=item["title"]
        cid=item["cid"]
        #准备异步任务
        tasks.append(asyncio.create_task(aiodownload(cid,title)))
    await asyncio.wait(tasks)

if __name__ == "__main__":
    url='https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"'+bookid+'"}'
    asyncio.run(getCatalog(url))