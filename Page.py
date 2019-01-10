# -*- coding: UTF-8 -*-
#Author: Aym
#Site: http://iaym.ml
from bs4 import BeautifulSoup
import urllib.request,requests,os,uuid

def startRequest(url,headers):
    print (url)
    res = requests.get(url,headers=headers)
    if res.status_code == 200:
        res_html = res.content.decode()
        doc_html = BeautifulSoup(res_html,'html.parser')
        author_info = doc_html.find("div",class_={'author-info'})
        author_title = author_info.find("a",class_={'title-content'})
        author = author_title['title']
        title_details = doc_html.find("div",class_={'details-contitle-box'})
        title = title_details.find('h2').get_text()
        getContent(doc_html,author,title.strip())
    else:
        print("%s - %s" % (url, res.status_code))

def getContent(item,author,title):
    img_list = getPage(item)
    print ("共%s张" % len(img_list))
    dir_str = "E:/Aym/"
    if not os.path.exists(dir_str):
        # print ("创建...")
        os.mkdir(dir_str)
    path_str = "%s - %s" % (author,title)
    path_str_mk = pathBase(dir_str + nameEncode(path_str))
    if path_str_mk is None:
        print ("%s 目标文件夹不存在" % path_str_mk)
        return
    else:
        for img_item in img_list:
            downloadImg(img_item,path_str_mk)
    

def getPage(html):
    pageturning = html.find("div", class_={'pageturning'})
    laypage_next = pageturning.find("a", class_={'laypage_next'})
    if laypage_next is not None:
        print ("存分")
        img_list = getLaypage(html)
    else:
        print ("无分")
        img_list = getDocImgLinks(html)
    return img_list

def getLaypage(html):
    work_box = html.find("div", class_={'work-show-box'})
    revs = work_box.find_all("div", class_={'reveal-work-wrap'})
    pageturning = html.find("div", class_={'pageturning'})
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
        i = 1
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
            i=i+1
        else:
            print("[分页文档获取失败][状态为%s] - %s，" % (href, res.status_code))
    print ("共%s页" % i)
    return img_list

def getDocImgLinks(html):
    work_box = html.find("div", class_={'work-show-box'})
    revs = work_box.find_all("div", class_={'reveal-work-wrap'})
    img_list = []
    for item in revs:
        img = item.find("img")
        if img is not None:
            img_url = img["src"]
            img_list.append(img_url)
        else:
            print("Tips:没有图片")
            continue
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
    for items in file_stop_str:
        file_name = file_name.replace(items, '-')
    return file_name

def downloadImg(url,path):
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
    url = "https://www.zcool.com.cn/work/ZMTgyNTkwMTY=.html"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
    startRequest(url,headers)
