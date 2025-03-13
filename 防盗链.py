#refer防盗链，溯源，当前本次请求的上一级是谁

#1.拿到contId
#2.拿到videoStatus返回的json. -> srcURL
#3.srcURL里面的内容进行修整,把systemTime的值换成contId就是正确的视频Url
#4.下载视频
import requests
#拉取视频的网址
url="https://www.pearvideo.com/video_1797772"
contId=url.split("_")[1]
videoStatusUrl=f"https://www.pearvideo.com/videoStatus.jsp?contId={contId}&mrd=0.4254"
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
    "Referer":url}
resp=requests.get(videoStatusUrl,headers=headers)
dic=resp.json()
srcUrl=dic["videoInfo"]["videos"]["srcUrl"]
systemTime=dic["systemTime"]
srcUrl=srcUrl.replace(systemTime,f"cont-{contId}")
#下载视频
with open("a.mp4",mode="wb") as f:
    f.write(requests.get(srcUrl).content)