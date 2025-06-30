#利用父子结点之间的关系进行查找，谁包着谁谁就是爹
#//后代，*通配符
#xpath是XML文档中搜索内容的一门语言
#html是xml的一个子集

from lxml import etree
xml="""
<book>
    <id>1</id>
    <name>开心</name>
    <price>1.23</price>
    <nick>臭豆腐</nick>
    <author>
        <nick id="10086">周大强</nick>
        <nick id="10010">周芷若</nick>
        <nick class="joy">周杰伦</nick>
        <nick class="jolin">蔡依林</nick>
        <div>
            <nick>绿茶</nick>
        </div>
        <span>
            <nick>白莲</nick>
        </span>
    </author>
    
    <partner>
        <nick id="ppc">paneoif</nick>
        <nick id="ppbc">fdjdkn</nick>
    </partner>
</book>
"""
tree=etree.XML(xml)
#result=tree.xpath("/book/name/text()") #/表示层级关系，第一个/表示根节点,text()拿文本
#result=tree.xpath("/book/author/nick/text()")
#result=tree.xpath("/book/author/div/nick/text()")
#result=tree.xpath("/book/author//nick/text()") #//后代
#result=tree.xpath("/book/author/*/nick/text()") # * 任意的节点，通配符，可以匹配div,也可以匹配span
result=tree.xpath("/book//nick/text()")#查找book中所有的后代
print(result)

