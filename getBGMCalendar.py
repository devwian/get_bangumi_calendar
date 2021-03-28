import json
import requests
import sys
import cfscrape
import datetime

baseurl = 'https://api.bgm.tv/calendar'

def get_bangumi():
	scraper = cfscrape.create_scraper() 
	info = scraper.get(baseurl).content.decode('utf-8')
	data = json.loads(info)
	#获取当前星期
	weekday = datetime.datetime.today().weekday()
	day = data[weekday]["items"]
	#钉钉MD换行前后各需要两个空格
	msge = '# '+data[weekday]["weekday"]['cn']+'  \n  '
	for i in day:
		if(len(i["name_cn"])==0):
			msge+=i["name"]+'  \n  '
		msge+=i["name_cn"]+'  \n  '
	return msge
	
def send_msg(url,msg):
	headers = {'Content-Type': 'application/json;charset=utf-8'}
	data = json.dumps({"msgtype": "markdown",
	"markdown":{"title":"BangumiTask",
		"text":msg},
	#提醒的电话号码
	"at":{"atMobiles": [],
	#是否提醒全体人员
	"isAtAll": False}})
	#POST请求
	r = requests.post(url,data,headers=headers)
	return r.text
	
if __name__ == '__main__':
    msg = get_bangumi()
    url = 'ding_link'                #此处为丁丁机器人的地址，参考技术手册创建
    #print(send_msg(url, msg))
