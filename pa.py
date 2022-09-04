#-*- coding = utf-8 -*-
#@Time : 2022/9/3 0:30
#@Author : 苏嘉浩
#@File : pa.py
#@Software : PyCharm
import re
import requests
from bs4 import BeautifulSoup
import time
import pandas
import openpyxl
def getHtml(url,num):
    header = {"user-agent":
                  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
              }
    Html = requests.get(url+str(num), headers=header)
    if Html.status_code == 200 :
        return Html.text

def getlist(html):
    code =BeautifulSoup(html,"html.parser")
    findPicture = re.compile(r'<img decoding="async" src="(.*?)" style="position:absolute;top:0;left:0;bottom:0;right:0;box-sizing:border-box;padding:0;border:none;margin:auto;display:block;width:0;height:0;min-width:100%;max-width:100%;min-height:100%;max-height:100%;object-fit:cover"/>')
    findTitle = re.compile(r'<div class="_3_JaaUmGUCjKZIdiLhqtfr">(.*?)</div>')
    findTime = re.compile(r'<div class="_3TzAhzBA-XQQruZs-bwWjE">.*([0-9][0-9][0-9][0-9][0-9]*-[0-9]*-[0-9]*)</div>')
    findPeople = re.compile(r'<div class="_2gvAnxa4Xc7IT14d5w8MI1">.*([0-9][0-9][0-9][0-9]?)</div>')
    Itemlist = []
    for items in code.find_all('div',class_="_3gcd_TVhABEQqCcXHsrIpT"):
        item = []
        items = str(items)

        picture = re.findall(findPicture,items)[0]
        item.append(picture)

        Title = re.findall(findTitle,items)[0]
        item.append(Title)

        Itime = re.findall(findTime,items)[0]
        item.append(Itime)

        people = re.findall(findPeople,items)[0]
        item.append(people)

        Itemlist.append(item)
        print(item)
    return Itemlist

if __name__ == '__main__':
    header = ["图片","标题","时间","人数"]
    data = pandas.DataFrame(columns=header)
    url = "https://www.aquanliang.com/blog/page/"
    num = 1
    f = 1
    while f == 1:
        html = getHtml(url, num)
        List = getlist(html)
        data2 = pandas.DataFrame(List, columns=header)
        data = data.append(data2)
        num = num + 1
        print("正在爬取请稍后")
        time.sleep(2)
        if num == 60:
            break
    data.to_excel("圈量.xlsx",index=True)
