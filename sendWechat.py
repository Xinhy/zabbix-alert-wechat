#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests,json,sys,time

'''
1.通过企业微信自建应用发送消息通知，提前确认应用对接收者可见；
2.获取的企业微信token缓存到本地文件中，失效后重新获取，确认文件位置tokenPath
3.默认指定用户发送，如需要按标签、部门发送，调整请求payload即可
'''


tokenPath = '/usr/lib/zabbix/alertscripts/wechatToken.json'

def getToken(corpid,secret):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    data = {
        'corpid':corpid,
        'corpsecret':secret
    }
    response = requests.get(url=url,params=data,timeout=15)
    if response.json()['errcode'] != 0:
        return False
    else:
        token = response.json()['access_token']
        with open(tokenPath,'w') as f:
            f.write(response.text)
        return token

def sendMessage(sendee,agentid,subject,content):
    try:
        with open(tokenPath,'r') as f:
            token = json.loads(f.readline().strip())['access_token']
    except:
        token = getToken(corpid, secret)

    url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % token
    data = {
        'touser': sendee,      # 按成员发送，指定成员ID，多个接收者用‘|’分隔
        #'totag': sendee,      # 按标签发送，指定标签ID，多个接收者用‘|’分隔，群发使用（推荐）
        #'toparty': sendee,    # 按部门发送，指定部门ID，多个接收者用‘|’分隔
        'msgtype': 'text',     
        'agentid': agentid,
        'text': {
            'content': subject + '\n' + content
        }
    }
    response = requests.post(url=url,data=json.dumps(data,ensure_ascii=False).encode(),timeout=15)
    
    retry = 0
    while response.json()['errcode'] != 0 and retry < 5:
        time.sleep(10)
        retry += 1
        token = getToken(corpid, secret)
        if token:
            url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % token
            response = requests.post(url=url,data=json.dumps(data,ensure_ascii=False).encode(),timeout=15)


if __name__ == '__main__':
    
    corpid = '企业微信企业ID'   #企业微信企业ID
    agentid = '应用ID'          #应用ID
    secret = '应用密码'         #应用密码
    
    
    sendee = str(sys.argv[1])        #脚本传入的第1个参数，接收人ID，多个接收者用‘|’分隔
    subject = str(sys.argv[2])       #脚本传入的第2个参数，消息主题
    content = str(sys.argv[3])       #脚本传入的第3个参数，消息内容
    
    sendMessage(sendee,agentid,subject,content)

