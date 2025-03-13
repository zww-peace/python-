#requests.get请求url，请求的参数直接放在url里面
#requests.post请求url,请求的参数放在字典中，通过data参数传递
import requests
url = "https://fanyi.baidu.com/sug"
s=input("请输入你要翻译的英文")
dat= {
    "kw": s  #在负载中找到的
}
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    'cookie': 'BAIDUID_BFESS=2D8E1997EF90EB305433E88CAF6DDADD:FG=1; __bid_n=193f33cf3b975365a7d0a1; BDUSS=zFiY25qYlpTM2w3NFBzeC1TNzcySjdGN0xra3VRaTN4T0xyNXk4QzhOSWoxSkJuRUFBQUFBJCQAAAAAAAAAAAEAAABeE9Ol0tTJz7~VsNe1xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNHaWcjR2lnb; BDUSS_BFESS=zFiY25qYlpTM2w3NFBzeC1TNzcySjdGN0xra3VRaTN4T0xyNXk4QzhOSWoxSkJuRUFBQUFBJCQAAAAAAAAAAAEAAABeE9Ol0tTJz7~VsNe1xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNHaWcjR2lnb; BIDUPSID=2D8E1997EF90EB305433E88CAF6DDADD; PSTM=1740569857; H_PS_PSSID=60271_61027_62114_62169_62176_62184_62186_62183_62203_62256_62262_62134; ZFY=hS2n9F25fbfa88zpQahCqBJqPvMexkaPahotMwARzCg:C; ab_sr=1.0.1_OGE2Mjk1ZThjYzUxZDliOTBkZjdiNjhiZmQ5MDM5NzQ2N2NkNTZmOGNmMmVlMmI2YmFkYWZjMmUwYjcyYWI5ZTAyODk2OWVjM2M2NDQwNTFmNzI4MDQ3YmI5MTY2NGVkOWMzMTVlYjk2ODFhMTcyMjQ0NWUyMGZkZWQ4NTlhYTc5NTU4NzNiYWU4ZWY1YzZiNDliMjkzOTg1YWQ5MzNmZA==; RT="z=1&dm=baidu.com&si=285a7ef7-3e64-47dd-8cda-372c77bc8231&ss=m7sgonc1&sl=7&tt=8nu&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=je9r"'
}
#发送post请求，发送的数据必须在字典中，通过data参数传递
resp=requests.post(url,data=dat,headers=headers)
#将服务器返回的内容直接处理成json => dict
print(resp.json())
resp.close() #关闭resp