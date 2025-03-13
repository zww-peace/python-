#代理：原理是通过第三方的一个机器去发送请求
import requests
#https://www.zdaye.com/dayProxy/ip/336754.html  站大爷免费代理

proxies={
    "http":"http://39.104.27.89:9080"  #用https会报错
}
resp=requests.get("http://www.baidu.com",proxies=proxies)
resp.encoding="utf-8"
print(resp.text)