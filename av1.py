# coding:utf-8
import requests
import re
import os
import lxml
import chardet
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import sys
import threading

reload(sys)
sys.setdefaultencoding('utf-8')

url_start='http://btdb.me'
#url_now = url_start + '/list/NDRA-019-s1d-1.html'
url_searchat = 'http://www.neihan8.com/'
url_provider='http://www.neihan8.com/tags/fanhao/0.html'

header={'User_Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
my_sender = 'xiaolifangan@qq.com'
my_pass='unhslrdguvnobehi'
my_user = '252504406@qq.com'
#http://www.cilizhu1.com/fanhao/index_2.html -52
#There is a site that offers the NO of the av :http://www.neihan8.com/tags/fanhao/
title = []  #标题列表
href = []  #内涵吧主页面列表
p = []  #原始番号列表
CargoID = []  #番号列表
url_list = []  #搜索域名列表
magnect = []  #磁力链接列表
threads = []


class av:
    def __init__(self):
        self.flag = False
        self.url = None
        self.href=None

    def Getsuburl(self,url):
        try:
            r = requests.get(url, headers=header)
            html = r.text
            soup = BeautifulSoup(html)
            T1 = soup.find('h3', attrs={'class': 'T1'})
            href_start = T1.find('a').get('href')
            href = url_start + href_start
            self.url = href
            self.flag = True
            t = requests.get(self.url, headers=header)
            html0 = t.text
            soup = BeautifulSoup(html0)
            dl = soup.find('dl', attrs={'class': 'BotInfo'})
            p = dl.find_all('p')
            soup1 = BeautifulSoup(str(p))
            a = soup1.find('a')
            self.href = a.get('href')
            magnect.append(self.href)
        except Exception as e:
            print e


def Getid(url):
    try:
        k=1  #后面去番号空格的变量
        r = requests.get(url, headers=header)
        # r.encoding = r.apparent_encoding
        html = r.text
        soup1 = BeautifulSoup(html)
        h3_list = soup1.find_all('h3')
        soup2 = BeautifulSoup(str(h3_list))
        a_list = soup2.find_all('a')
        for i in a_list:
            href.append(url_searchat + i.get('href'))
            title.append(i.get('title'))
        if href:
            try:
                for i in href:
                    if re.match('http://www.neihan8.com//av', i):
                        t = requests.get(i, headers=header)
                        t.encoding = t.apparent_encoding
                        html1 = t.text
                        soup3 = BeautifulSoup(html1)
                        p_list = soup3.find_all('p', attrs={'style': 'TEXT-ALIGN: center'})
                        for ii in p_list:
                            # print chardet.detect(ii.text.strip().split('号')[-1])
                            c=ii.text.strip().split('号')[-1]
                            CargoID.append(c)
                    else:
                        break
            except Exception as q:
                print q
        else:
            print 'No more href'
    except Exception as e:
        print e


def mail(message):
    ret = True
    try:
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = formataddr(["FromRunoob", my_sender])
        msg['To'] = formataddr(["阿蛮", my_user])
        msg['Subject'] = '2017-11-13'

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    except Exception as e:
        ret = False
        print e
    return ret


if __name__ == '__main__':
    try:
        time1 = time.clock()
        A=av()
        Getid(url_provider)
        # f=open('fo.txt','wb+')
        # for i in CargoID:
        #     if i:
        #         print i
        #         f.write(i+'\r\n')
        # f.close()
        for i in CargoID:
            if i:
                # print i
                url_list.append(url_start+'/list/'+i+'-s1d-1.html')
        for l in url_list:
            print l
            # t=threading.Thread(target=A.Getsuburl(l))
            # threads.append(t)
            A.Getsuburl(l)
        # for k in magnect:
        #     print k
        # for i in magnect:
        #     f.write(i + '\r\n')
        # f.read()
        # f.close()
        time2 = time.clock()
        print time2-time1
    except Exception as e:
        print e

        # ret = mail(A.href)
        # if ret:
        #     print "Sending successfully " + time.ctime()
        #     time.sleep(300)
        # else:
        #     print "Sending failed " + time.ctime()
# if __name__ == '__main__':
#     for t in threads:
#         t.setDaemon(True)
#         t.start()
#     t.join()
