# 1.找到未加密的参数                     #window.arsea(参数，xxx,xxx)(加密算法)
# 2.想办法把参数进行加密(必须参考网易的逻辑),params => encText(加密后的文本), encSecKey => encSecKey(秘钥)
# 3.请求到网易，拿到评论信息

# https://music.163.com/#/song?id=1325905146
# ctrl+F搜索页面源代码中的指定内容
# 源代码没有，利用抓包工具找到存储评论内容的包
# 包的url采用post方式，需要提供params和encSecKey，也就是加密后的内容和秘钥
# 为了找到加密的原数据以及加密算法，通过在抓包工具发起程序处，查找所有调用堆栈
# 本视频从最后一个core开始,一步一步向上层堆栈去找data是从哪个包从加密数据变成未加密数据的
# 源代码窗口查看作用域和调用堆栈，来定位到加密算法的代码和,找到未加密前的data
# 分析加密算法的代码，发现params是xxxxx.encText,encSecKey是xxxxx.encSecKey
# 而xxxxx是通过window函数生成的,而window = d
# 最终找到加密的d函数，d函数有四个参数d,e,f,g,其中d传的是原始data,e,f,g通过控制台console输出发现是定值
# d函数通过b函数生成encText,通过c函数生成encSecKey
# 而c函数参数是i,e,f,其中i是随机产生的16位字符串
# 通过将i固定，直接在原网页中搜索某个i以及对应的encSecKey来躲避分析c函数的加密算法
# 而b函数，通过两次加密，第一次将原始data,g作为参数加密,第二次将返回的内容和i加密，g,i都是秘钥
# 仿照b函数来写加密算法，模仿加密过程来得到encText也就是params

# 其中在分析代码，在某处设置断点，重新加载网页后，还需继续放开网页到comment/get的url,然后单步执行进行分析查看
# 在寻找encSecKey怎么生成，除了通过调用堆栈来一步步查找，也可以直接ctrl+F进行搜索定位





from Crypto.Cipher import AES
from base64 import b64encode
import requests
import json
url="https://music.163.com/weapi/comment/resource/comments/get?csrf_token="

# 请求方式是post
data = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "R_SO_4_1325905146",
    "threadId": "R_SO_4_1325905146"
    }
# 服务于d函数的，用于生成params和encSecKey
f = "0085ddee518103f1aef177d3031a0b2fbf1595fb7d5c70afabcc3f356e0bdede8b2e40adc751df9ece1a62750ad1d9cdff976ead0a6f992b16a22abf1339e2b644fddfde23271723e113712c03a07c770be3a251d5a49fd1a9745acb8cabafefcd1c65d4d1409f5f0243a4587a6ded88802afc0a57f23f641a26cbacb4fdd6bf3f"
g = "0CoJUm6Qyw8W8jud"
e = "010001"
i = "6KZswwDPlP3xmB2n" #手动固定的. ->人家函数中是随机的
def get_encSecKey(): #由于i是固定的，那么c()函数的结果就是固定的,生成的encSecKey是固定的，
    return "93c3ad9fc154a0f83b82e87b53bbffb6b19bf089477e2ff7b1da492850df36de20acda012878bc22e129866beccece5f52816b623fc5440fc2af4753a6706eaad770ffe11c091415ee9f7a342b003bca20ad8e90be14e273421b960d31cbcc0b2a0ace3da7ccf8b8d701324b6ffbc2a574eea4247d290c6487c6ad3de5555ff9"

#把data进行两次加密得到params
def get_params(data): #默认这里接收到的是字符串
    first = enc_params(data,g) # data经过两次加密得到params
    second = enc_params(first,i)
    return second # 返回的是params

#将data填充，使得长度为16的倍数
def to_16(data):
    pad = 16-(len(data))%16
    data += chr(pad)*pad
    return data

#模仿源代码b函数加密算法写的加密过程
def enc_params(data,key): #加密过程
    iv = "0102030405060708" #偏移量
    data = to_16(data)
    aes=AES.new(key=key.encode("utf-8"), IV=iv.encode("utf-8"),mode=AES.MODE_CBC) # 创建加密器
    bs = aes.encrypt(data.encode("utf-8")) #加密，加密的内容的长度必须是16的倍数，如果数据是“123456”，差10个，补10个chr(10)
    return str(b64encode(bs),"utf-8") # bs是二进制字节,需要转化成字符串返回

# 处理加密过程
"""
    function a(a = 16) { #返回随机的16位字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length, #Math.random()是生成(0,1)之间的随机数,*b.length表示最大取到64
            e = Math.floor(e), #下取整
            c += b.charAt(e); #取出b中一个随机字符追加到c上
        #返回随机的16位字符串
        return c
    }
    function b(a, b) { #a是要加密的内容
        var c = CryptoJS.enc.Utf8.parse(b) # b是秘钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708") #偏移量
          , e = CryptoJS.enc.Utf8.parse(a) # e是数据
          , f = CryptoJS.AES.encrypt(e, c, { # c是秘钥
            iv: d, # AES加密偏移量
            mode: CryptoJS.mode.CBC # CBC模式加密
        });
        return f.toString()
    }
    function c(a, b, c) { #c里面不产生随机数
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {          #d:数据,e:'010001',f:很长,g:'0CoJUm6Qyw8W8jud'
        var h = {} #空对象
          , i = a(16); #i就是16位的随机数，把i设置成定值
        
        h.encText = b(d, g) # g是秘钥
        h.encText = b(h.encText, i) #返回的就是params ,i是秘钥
        #如果把i固定,那么c产生的也是个定值
        #也就是encSecKey也是个定值
        h.encSecKey = c(i, e, f) #得到的就是encSecKey,e和f是定值，i是由a产生的随机数
        return h
        两次加密：
        数据+g => b => 第一次加密+i => b = params
        #####################源代码#########################
        
        return h.encText = b(d, g),
        h.encText = b(h.encText, i), 
        h.encSecKey = c(i, e, f),
        h

    }
"""

#发送请求，得到评论结果
resp = requests.post(url,data={
    "params" : get_params(json.dumps(data)), #将字典转化成字符串
    "encSecKey" : get_encSecKey()
})
print(resp.text)