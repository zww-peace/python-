#服务器渲染和客户端渲染
#服务器渲染:在服务器那边直接把数据和html整合在一起，统一返回给浏览器，在页面源代码中能看到数据
#客户端渲染:第一次请求只有html骨架，第二次请求拿到数据进行数据展示
#html第一次请求只能请求到网页的框架，第二次请求才能请求到网页的元素
#抓包工具，XHR请求用来过滤，找到发送html的第二次请求的包
import requests

url="https://movie.douban.com/j/chart/top_list"
#第二种方式封装参数，第一种是直接放在url中https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start=0&limit=20
#?后面是参数，前面是url
param={
    "type": "24" ,#双击+引用
    "interval_id": "100:90",
    "action": "",
    "start": 0,
    "limit": 20
}
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    'cookie': 'BAIDUID_BFESS=2D8E1997EF90EB305433E88CAF6DDADD:FG=1; __bid_n=193f33cf3b975365a7d0a1; BDUSS=zFiY25qYlpTM2w3NFBzeC1TNzcySjdGN0xra3VRaTN4T0xyNXk4QzhOSWoxSkJuRUFBQUFBJCQAAAAAAAAAAAEAAABeE9Ol0tTJz7~VsNe1xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNHaWcjR2lnb; BDUSS_BFESS=zFiY25qYlpTM2w3NFBzeC1TNzcySjdGN0xra3VRaTN4T0xyNXk4QzhOSWoxSkJuRUFBQUFBJCQAAAAAAAAAAAEAAABeE9Ol0tTJz7~VsNe1xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNHaWcjR2lnb; BIDUPSID=2D8E1997EF90EB305433E88CAF6DDADD; PSTM=1740569857; H_PS_PSSID=60271_61027_62114_62169_62176_62184_62186_62183_62203_62256_62262_62134; ZFY=hS2n9F25fbfa88zpQahCqBJqPvMexkaPahotMwARzCg:C; ab_sr=1.0.1_OGE2Mjk1ZThjYzUxZDliOTBkZjdiNjhiZmQ5MDM5NzQ2N2NkNTZmOGNmMmVlMmI2YmFkYWZjMmUwYjcyYWI5ZTAyODk2OWVjM2M2NDQwNTFmNzI4MDQ3YmI5MTY2NGVkOWMzMTVlYjk2ODFhMTcyMjQ0NWUyMGZkZWQ4NTlhYTc5NTU4NzNiYWU4ZWY1YzZiNDliMjkzOTg1YWQ5MzNmZA==; RT="z=1&dm=baidu.com&si=285a7ef7-3e64-47dd-8cda-372c77bc8231&ss=m7sgonc1&sl=7&tt=8nu&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=je9r"'
}
resp=requests.get(url=url,params=param,headers=headers)
print(resp.request.url)#输出请求的url
print(resp.request.headers)#输出请求头
print(resp.json())
resp.close() #关闭resp