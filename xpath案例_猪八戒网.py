#拿到页面源代码
#提取和解析数据
import requests
from lxml import etree
url="https://www.zbj.com/fw/?k=sass"
resp=requests.get(url)
#print(resp.text)
#解析
html = etree.HTML(resp.text)

#拿到每一个服务商的div
#直接复制xpath是/html/body/div[2]
#但是源代码中/body后面有一个div是被隐藏的hidden=True
#所以需要把div[2]改为div[1]
#倒数第二个div,div[2]表示的是大框，后面加上div表示拿出大框下的所有小框，所有div
divs = html.xpath("/html/body/div[1]/div/div/div[3]/div[1]/div[4]/div/div[2]/div/div[2]/div")
#divs是一个列表，列表中是每个div对象，通过for遍历拿到div对象
for div in divs:
    #当前已经是上面xpath中的最后面的div[1/2/3]了，所以在price完整单位xpath中，要从div[1/2/3]后面的部分开始截取
    #如果想要提取文本内容，需要加上/text()
    #文本字符串是放在列表中的，所以需要通过[0]来提取
    #列表中可能有多个字符串用逗号隔开,所以必要时需要通过join将所有字符串连接在一起
    price=div.xpath("./div/div[3]/div[1]/span/text()")[0].strip("¥")
    title="saas".join(div.xpath("./div/div[3]/div[2]/a/span/text()"))#功能
    com_name=div.xpath("./div/div[5]/div/div/div/text()")[0]#公司名称
    #location=div.xpath("./") 改版后没有找到地址信息
    print(price)
    print(title)
    print(com_name)
    print("---------------------------------------------------------------------------------")