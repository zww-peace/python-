#1.通过session会话拿到cookie
#2.直接从浏览器复制cookie
#登录 -> 得到cookie
#带着cookie 去请求到书架url -> 书架内容

#必须得把上面的两个操作连起来
#我们可以使用session进行请求->session可以认为是一连串的请求，在这个过程中cookie不会丢失

#本实验未成功，原因是login包出现然后瞬间就消失了,代码一模一样，但是无法成功登录
import requests

#会话,知道之前的请求以及获得的cookie
session = requests.session()
data={
    "loginName":"xxxxxxxxxxx",
    "password":"buzhidao_123"
}
#1.登录
url="https://www.17k.com/ck/user/login"
resp=session.post(url,data=data)
print(resp.text)
#该网站用抓包工具时要在源代码中禁用断点，否则会一直卡在断点处，星球样子的图标禁掉

#2.拿书架上的数据
#刚才的那个session中是有cookie的
resp=session.get('https://user.17k.com/ck/author/shelf')
print(resp.json())

#这个能成功拿到数据
resp=requests.get('https://user.17k.com/ck/author/shelf',headers={
    "cookie":"GUID=30ad8e97-fec1-4959-8392-997779afcba9; c_channel=0; c_csc=web; acw_tc=1a0c640917410575968385318e003e33101df7eafe837c6342ed9a8b40bd4e; acw_sc__v2=67c66e3d7111c4def3e9fbb0591c4248ebeee388; BAIDU_SSP_lcr=https://cn.bing.com/; Hm_lvt_9793f42b498361373512340937deb2a0=1740642499,1741016331,1741057599; HMACCOUNT=55C6616D2524F5C7; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2230ad8e97-fec1-4959-8392-997779afcba9%22%2C%22%24device_id%22%3A%221954660b9ebaca-077f63beaf89d5-4c657b58-1327104-1954660b9ec1377%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22cn.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%2C%22first_id%22%3A%2230ad8e97-fec1-4959-8392-997779afcba9%22%7D; Hm_lpvt_9793f42b498361373512340937deb2a0=1741058192; accessToken=avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F07%252F27%252F88%252F104028827.jpg-88x88%253Fv%253D1741017213000%26id%3D104028827%26nickname%3Dnickbythe%26e%3D1756610354%26s%3D39bda5336329fd41; tfstk=gk6EaNMAZJeEDhBUrhvr_yBnioJpUp4b8TTWqgjkAeYHFWLkrgQ9VYsktV4y7aLBOpb5z47C5ebP2kKkrabyP6N_hMIpeL4fz-wfvIY0zebetYjgq3-vqlO3AgFDOL4blRGsjBUBEw1vOe0NjFKyqUxlrcqw439oKQDnsVY9qLvk-emGj3--tvDktlSMW3vkraAnBjTklA-2tu8vdMGbrjRkoMYZExovDBmRAbMmnOteTTjH7QRPQHReoC3HQLWh5gXCpCFt1LI1ga5loPGB-s-V7I1Uuv7VJ3bwdtq89CdlUT-O6zlyu_jCM_AaxJjwLeRwYBoEZp5lJTRdT0EAjpbOMEd36PKNdtOykCug-Gsw-I5PRPHkRsSG7I6s5x9cMNWyiKjyt4KgGY6RT4ckthKwllraYhmc8YflEtl-wBC9bEZLvbhJthKwllrZwbdpBh8bvkC..; ssxmod_itna=QqGx9ii=KiqGu7Dl4Yq0P+p3x2DUhhTx3oxYvvUtD/BbmDnqD=GFDK40ooS5+343oWm7p0oUK77pwKLlYRgD5LYiaPGLDmKDyKj2heDxhq0rD74irDDxD3Db8dDSDWKD9D0+8BnLuKGWDm+zDYHFDQys44DFuEKOq4i7DDvQOx07K9KxDG5xzbGoh2Go44DrO=BCFKyDpRx5fxG1K40HoidxfoO6ybizp9SLDU4ODlF2DCF1=4vpFn9z9x7PQj4PQYhNWDKrCQD5tG4xoh6W=BxPbgho10i4Av0DQ70KCm63eDDW/Bq54D==; ssxmod_itna2=QqGx9ii=KiqGu7Dl4Yq0P+p3x2DUhhTx3oxYvvtG9WoDBTP7jHGcDewiD==="})
print(resp.text)