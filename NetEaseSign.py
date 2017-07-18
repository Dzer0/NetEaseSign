# coding:utf-8
import requests
import os
import smtplib
from email.mime.text import MIMEText
'''
netbase sign
type=1 web sign
type=0 phone sign
os travis-ci profile
return value
code：200 Sign Success
code: -2 Repeat sign
'''

mailto_list = os.getenv('mailtouser')
mail_host = 'smtp.163.com'
mail_user = os.getenv('mail_user')
mail_pass = os.getenv('mail_pass')
os_cookies = os.getenv('cookies')


def netbaseqiandao(typeid):
    cookies = {'MUSIC_U': os_cookies}
    url = 'http://music.163.com/api/point/dailyTask?type=%s&csrf_token=123' % typeid
    headers = {
        'Referer': 'http://music.163.com/discover',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.30 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }
    res = requests.post(url, cookies=cookies, headers=headers)
    sendmail(res.text)
    return res.text


def sendmail(conent):
    if '200' in conent or '-2' in conent:
        print('Sign Success')
    else:
        me = 'Root@admin.com'
        msg = MIMEText(conent, _subtype='html', _charset='utf-8')
        msg['Subject'] = 'You Session Expired!!!'
        msg['From'] = me
        msg['To'] = mailto_list
        try:
            s = smtplib.SMTP()
            s.connect(mail_host, 25)
            s.login(mail_user, mail_pass)
            s.sendmail(me, mailto_list, msg.as_string())
            s.close()
            return True
        except Exception as e:
            print(str(e))
            return False


if __name__ == '__main__':
    netbaseqiandao(0)
    netbaseqiandao(1)
# print(type("{'point': 2, 'code': 200}"))
