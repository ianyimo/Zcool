# -*- coding: UTF-8 -*-
#Author: Aym
#Site: http://iaym.ml
from bs4 import BeautifulSoup
import urllib.request,socket,re,sys,os,threading,requests,uuid
import chardet

# index
def startRequest(url):
    print("[Tips:]正在抓取 - %s " % url)
    res = requests.get(url)
    if res.status_code == 200:
        res_html = res.content.decode()
        doc = BeautifulSoup(res_html,'html.parser')
        work_box = doc.find('div', class_={'work-list-box'})
        card_box_list = work_box.find_all('div', class_={'card-box'})
        for item in card_box_list:
            getContent(item)
            # print (item)
    else:
        print("[文档获取失败][状态为%s] - %s，" % (url, res.status_code))

def getContent(item):
    title_content = item.find("a", class_={'title-content'})
    avatar = item.find('span', class_={'user-avatar'})
    if title_content is not None:
        title = title_content.text
        author = avatar.find("a")["title"]
        # author = ""
        href = title_content['href']
        # print(title_content)
        res = requests.get(href)
        if res.status_code == 200:
            img_list = ifpage(res.content.decode())
            path_str = "%s - %s" % (author, title)
            datasrc = "E:/Data/"
            if not os.path.exists(datasrc):
                os.mkdir(datasrc)
            path_str_mk = pathBase(datasrc + nameEncode(path_str))
            if path_str_mk is None:
                return
            else:
                for img_item in img_list:
                    downloadImg(img_item, path_str_mk)

        else:
            print("[文档获取失败][状态为%s] - %s，" % (href, res.status_code))
    else:
        return

def getDocImgLinks(html):
    doc = BeautifulSoup(html,'html.parser')
    work_box = doc.find("div", class_={'work-show-box'})
    revs = work_box.find_all("div", class_={'reveal-work-wrap'})
    img_list = []
    for item in revs:
        img = item.find("img")
        if img is not None:
            img_url = img["src"]
            img_list.append(img_url)
        else:
            print("[Tips:]：没有图片")
            continue
    return img_list

def ifpage(html):
    doc = BeautifulSoup(html,'html.parser')
    pageturning = doc.find("div", class_={'pageturning'})
    laypage_next = pageturning.find("a", class_={'laypage_next'})
    if laypage_next is not None:
        img_list = getlaypage(html)
    else:
        img_list = getDocImgLinks(html)
    return img_list

def getlaypage(html):
    doc = BeautifulSoup(html,'html.parser')
    work_box = doc.find("div", class_={'work-show-box'})
    revs = work_box.find_all("div", class_={'reveal-work-wrap'})
    pageturning = doc.find("div", class_={'pageturning'})
    laypage_next = pageturning.find("a", class_={'laypage_next'})
    workurl =  "https://www.zcool.com.cn"
    img_list = []
    for item in revs:
        img = item.find("img")
        if img is not None:
            img_url = img["src"]
            img_list.append(img_url)
        else:
            print("[Tips:]：没有图片")
            continue
    while laypage_next is not None:
        href = workurl + laypage_next['href']
        res = requests.get(href)
        if res.status_code == 200:
            res_html = res.content.decode()
            docs = BeautifulSoup(res_html,'html.parser')
            work_box = docs.find("div", class_={'work-show-box'})
            revs = work_box.find_all("div", class_={'reveal-work-wrap'})
            for item in revs:
                img = item.find("img")
                if img is not None:
                    img_url = img["src"]
                    img_list.append(img_url)
                else:
                    print("[Tips:]：没有图片")
                    continue
            pageturning = docs.find("div", class_={'pageturning'})
            laypage_next = pageturning.find("a", class_={'laypage_next'})
        else:
            print("[分页文档获取失败][状态为%s] - %s，" % (href, res.status_code))
    return img_list


def pathBase(file_path):
    file_name_s = file_path.split("/")
    file_name = file_name_s[len(file_name_s) - 1]
    file_name_s[len(file_name_s) - 1] = file_name
    path = "/".join(file_name_s)
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def nameEncode(file_name):
    file_stop_str = ['\\', '/', '*', '?', ':', '"', '<', '>', '|']
    for item2 in file_stop_str:
        file_name = file_name.replace(item2, '-')
    return file_name

def downloadImg(url, path):
    z_url = url.split("@")[0]
    hz = url.split(".")
    z_hz = hz[len(hz) - 1]
    res = requests.get(z_url)
    if res.status_code == 200:
        img_down_path = path + "/" + str(uuid.uuid1()) + "." + z_hz
        f = open(img_down_path, 'wb')
        f.write(res.content)
        f.close()
        print("[下载成功] -  %s" % img_down_path)
    else:
        print("[IMG下载失败][状态为%s] - %s，" % (z_url, res.status_code))
        
if __name__ == "__main__":
    threads = []
    user = "userid"
    word = "logo"
    #word = input('input:')
    for i in range(1, 2):
        # url = 'https://www.zcool.com.cn/u/'+user+'?myCate=0&sort=8&p='+(str(i))+''
        url = 'https://www.zcool.com.cn/search/content?word='+word+'&p='+(str(i))+''
        threads.append(threading.Thread(target=startRequest, args={url}))

    for item in threads:
        item.start()
