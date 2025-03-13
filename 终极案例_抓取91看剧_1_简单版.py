#前面介绍了视频网站的基本原理
#视频不是一个完整的视频，而是长度很短的切片组成，可能就几秒
#有一个.m3u8文件用来存储所有切片所在地址的url

#视频介绍了一种反爬机制
#在第一次访问网站资源时，服务器端会生成一个随机字符串，客户端拿着这个字符串去申请m3u8文件
#在有效时长内，客户端成功拿到m3u8文件

#91看剧网址进不去
#www.91zhuiju.cc用这个网址做的
#但是这个网址没设置反爬机制，m3u8直接抓包就能找到url，不需要从网页源代码提取带有相应字符串的m3u8文件
#天天影院 星辰影院

"""
流程
1.拿到.html的页面源代码
2.从源代码中提取到m3u8的url
3.下载m3u8
4.读取m3u8文件，下载视频
5.合并视频
"""
#https://svipsvip.ffzy-online5.com/20241010/33444_13c82439/2000k/hls/mixed.m3u8
#https://svipsvip.ffzy-online5.com/20241010/33444_13c82439/2000k/hls/dec14d6b3f8f5574d944ba2237eafed8.ts
import requests

url = "https://svipsvip.ffzy-online5.com/20241010/33444_13c82439/2000k/hls/mixed.m3u8"
resp = requests.get(url)
with open("video/动漫.m3u8", mode ="wb") as f:
    f.write(resp.content)
resp.close()
baseurl=url.rsplit("mixed.m3u8")[0]
n=1
with open("video/动漫.m3u8", mode="r", encoding ="utf-8") as f:
    for line in f:
        line=line.strip() #先去掉空格，空白，换行符
        if line.startswith("#"):#以#开头的是没用的消息，直接cotinue查看下一行
            continue
        #下载视频的片段
        child_url=baseurl+line #获取每一个ts的url
        resp2=requests.get(child_url)
        f=open(f"video/{n}.ts",mode="wb")
        f.write(resp2.content)
        n+=1
        resp2.close()
        print(f"{line} over!")


"""
import re
headers={
    ...
}
obj = re.compile(r"url:'(?P<url>.*?)',",re.S) #用来提取m3u8的url地址
url="https://www.91kanju.com/vod-play/54812-1-1.html"
resp=requests.get(url,headers=headers)
m3u8_url = obj.search(resp.text).group("url") #拿到m3u8的地址
resp.close()
"""