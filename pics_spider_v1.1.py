

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
import urllib.request
import ssl
import threading


class SPIDER(threading.Thread):

    """图片爬取正式版1.1，多线程，非requests"""


    def __init__(self,current_name):
        super(SPIDER,self).__init__()
        self.current_name=current_name
        self.scroll_number=120
    def sle(self,a):
        time.sleep(a)

    def scroll(self, browser, length, counts):
        browser = browser
        for c in range(counts):
            js = 'window.scrollTo(' + str(0) + ', ' + str(c) + ')'
            c += length
            browser.execute_script(js)
            self.sle(1)
    def run(self):
        self.spider(self.current_name)
    def spider(self,current_name):
        url0 = 'https://www.pornpics.com/?q='

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(options=options)
        self.sle(1)
        search_result_list_url = []                  #系列各自的url
        search_name = self.current_name.replace(' ', '+')
        url = url0 + search_name
        browser.get(url)
        print('开始搜索'+self.current_name)
        self.sle(2)
        s = 0
        for s0 in range(30):
            js = 'window.scrollTo(' + str(0) + ', ' + str(s) + ')'
            s += 2000
            s0 += 1
            browser.execute_script(js)
            self.sle(1)                                                  #网快的话 1s应该就可以了

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')                  #解析html
        search_result_list = soup.find_all('a', "rel-link")        #搜索人名后出现的所有系列的<a>

        for a in search_result_list:                               #获取各个系列的href中的link，存入Search_Result_List_url
            c= a['href']
            search_result_list_url.append(c)
        album_link = search_result_list_url                        #所有系列的url
        final_url_link = []                                        #最终所有图片的url
        print('正在获取'+current_name+'各图组！')
        ic = 0
        for url_album in album_link:                               #访问各图组
            browser.get(url_album)
            s = 0
            ic+=1
            for s0 in range(2):
                js = 'window.scrollTo(' + str(0) + ', ' + str(s) + ')'
                s += 5000
                browser.execute_script(js)
                self.sle(0.1)
            html_album = browser.page_source
            soup_album = BeautifulSoup(html_album, 'html.parser')
            each_album_all_url = soup_album.find_all('a', "rel-link")   #每个系列中的所有link

            for link in each_album_all_url:                         #根据每个图组中每张图片的link获取href
                e = link['href']
                if e[:11] == 'https://cdn':
                    final_url_link.append(e)
                elif e[:11] == 'https://ima':
                    final_url_link.append(e)
                elif e[:11] == 'https://www':
                    pass
                else:
                    pass


            perr = 100* ic/len(album_link)
            perrr= float('%.2f'%perr)
            jindu = '获取'+self.current_name+'图组进度：' + str(perrr) + '%'
            print('\r'+ jindu, end='')
        print('')
        person = self.current_name
        path = '/Applications/Pornpics/' + person
        if os.path.exists(path) == True:
            print('已存在'+person+'的文件夹')
        else:
            os.mkdir(path)
            print('已创建'+person+'的文件夹')
        i = 0
        ALL = len(final_url_link)
        total_time = 0

        #file = open('picsurl.txt','w+')
        #print(final_url_link, file = file)
        #file.close()
        #exit()
        for links in final_url_link:
            start_time = time.time()
            url = links

            path = '/Applications/Pornpics/' + person + '/'
            i += 1
            file_name = path + person + str(i) + '.jpg'
            try:
                urllib.request.urlretrieve(url, filename=file_name)
            except:
                for t in range(5):
                    urllib.request.urlretrieve(url, filename=file_name)
                    break
                pass

            per = float(float(i)/float(ALL) * 100)
            percent = str('%.2f'%per)
            strc = '下载进度：'+percent+'%' + '//**//**//' + '正在下载第' + str(i) + '张图片'
            end_time = time.time()
            total_time = total_time + (end_time - start_time)

            total_time_in_min = int(total_time/60)
            total_time_in_sec = total_time - 60 * total_time_in_min

            left_time = total_time * 100 / per - total_time
            left_time_in_min = int(left_time/60)
            left_time_in_sec = left_time - 60*left_time_in_min
            print('\r' + person.title() + ':  ' + strc + '//**//**//' + '已用时间' + str(total_time_in_min) + '分钟' + str('%.2f'%total_time_in_sec) + '秒'
                  + '//**//**//' + '预计剩余时间为'+str(left_time_in_min)+'分钟' + str('%.2f'%left_time_in_sec)+'秒', end='')
        else:
            pass
        browser.close()
        print('')
        print('已爬取'+person +'图组并存储于Applications/Pornpics/同名文件夹下')
        print('**********爬取完成**********')
        print('')
def main():
    ssl._create_default_https_context = ssl._create_unverified_context

    thread = []              #线程池
    person = input('输入搜索的人名（多个人名用逗号分割）:')
    personlist = person.split(',')
    print(personlist)
    for person in personlist:
        t = SPIDER(person)
        thread.append(t)
        t.start()
    print('所有线程已开启')
    for t in thread:
        t.join()
    print('********************所有爬取完成********************')


main()