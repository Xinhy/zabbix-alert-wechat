# zabbix_alert_wechat

1.通过企业微信自建应用发送消息通知，提前确认应用对接收者可见;

2.获取的企业微信token缓存到本地文件中，失效后重新获取，确认文件位置tokenPath;

3.默认指定用户发送，如需要按标签、部门发送，调整请求payload即可;

4.使用Python3环境运行，不支持Python2
