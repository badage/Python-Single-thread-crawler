#-*_coding:utf8-*-
import requests
import re

class spider(object):
    def __init__(self):
        print(u'开始爬取内容。。。')

#getsource用来获取网页源代码
    def getsource(self,url):
        html = requests.get(url)
        return html.text

#changepage用来生产不同页数的链接
    def changepage(self,url,total_page):
        now_page = int(re.search('pageNum=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('pageNum=\d+','pageNum=%s'%i,url,re.S)
            page_group.append(link)
        return page_group
#geteachclass用来抓取每个课程块的信息
    def geteachclass(self,source):
        everyclass = re.findall('(<li id.*?</li>)',source,re.S)
        return everyclass
#getinfo用来从每个课程块中提取出我们需要的信息
    def getinfo(self,eachclass):

        info = {}
        info['title'] = re.search('title="(.*?) alt=',eachclass,re.S).group(1)
        info['content'] = re.search('<p style="height: 0px; opacity: 0; display: none;">(.*?)</p>',eachclass,re.S).group(1)
        timeandlevel = re.findall('<em>(.*?)</em>',eachclass,re.S)
        info['classtime'] = timeandlevel[0]
        info['classlevel'] = timeandlevel[1]
        info['learnnum'] = re.search('"learn-number">(.*?)</em>',eachclass,re.S).group(1)
        return info
#saveinfo用来保存结果到info.txt文件中
    def saveinfo(self,classinfo):
        f = open('info.txt','w',encoding='utf-8')
        for each in classinfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('content:' + each['content'] + '\n')
            f.writelines('classtime:' + each['classtime'] + '\n')
            f.writelines('classlevel:' + each['classlevel'] + '\n')
            f.writelines('learnnum:' + each['learnnum'] +'\n\n')
        f.close()

if __name__ == '__main__':

    classinfo = []
    url = 'http://www.jikexueyuan.com/course/?pageNum=1'
    myspider = spider()
    all_links = myspider.changepage(url,20)
    for link in all_links:
        print (u'正在处理页面：' + link)
        html = myspider.getsource(link)
        everyclass = myspider.geteachclass(html)
        for each in everyclass:
            info = myspider.getinfo(each)
            classinfo.append(info)
    myspider.saveinfo(classinfo)


