#根据特定顺序或属性，提取某类标签中的某一个
#li[1] a[@href='dapao']/text() ./相对查找 /从根查找 ./a/@href拿到属性值
from lxml import etree

tree=etree.parse("b.html")
#result=tree.xpath('/html/body/ul/li/a/text()')
#result=tree.xpath('/html/body/ul/li[1]/a/text()') #xpath从1开始数，[]表示索引
#result=tree.xpath("/html/body/ol/li/a[@href='dapao']/text()")#[@xxx=xxx]属性的筛选
#print(result)
ol_li_list=tree.xpath("/html/body/ol/li")
for li in ol_li_list:
    result=li.xpath("./a/text()")#在li中继续寻找，是相对查找
    print(result)
    result2=li.xpath("./a/@href")#拿到属性值:@属性
    print(result2)
print(tree.xpath("/html/body/ul/li/a/@href"))
#浏览器右键检查，元素界面，点击要选中的内容，右键copy，复制xpath
print(tree.xpath("/html/body/div[1]/text()"))
