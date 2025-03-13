#网页右键->检查->网络->重新刷新抓包->headers请求头,preview预览
import requests

query=input("请输入一个你喜欢的明星")
url=f"https://cn.bing.com/search?q={query}"

headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
}
resp=requests.get(url,headers=headers) #还有requests.post

print(resp.text) #拿到页面源代码
resp.close() #关闭resp