import time
from bs4 import BeautifulSoup
import os
import urllib.request
import ssl
import threading
import requests


class SPIDER(threading.Thread):

    """图片爬取正式版1.1, requests, threading"""

    def __init__(self, current_name):
        super(SPIDER,self).__init__()
        self.current_name = current_name

    def run(self):
        self.spider(self.current_name)

    def download_album_url(self, name, total=10):
        """ 下载某人的图组url """
        url0 = 'https://www.pornpics.com/search/srch.php?q=' + str(name) + '&limit=20&offset='
        root_url = []
        for i in range(total):
            url = url0 + str(20 * i)
            try:
                web = requests.get(url)
            except:
                pass
            web.encoding = web.apparent_encoding
            for item in web.json():
                root_url.append(item['g_url'])
            print('\r' + '进度:' + str((i + 1) * 100 / total) + '%', end='')
        return root_url

    def download_img(self, url_list, path, person):
        i = 0
        total_len = len(url_list)
        total_time = 0
        path += '/'
        for links in url_list:
            start_time = time.time()
            url = links
            i += 1
            file_name = path + person + str(i) + '.jpg'
            try:
                urllib.request.urlretrieve(url, filename=file_name)
            except:
                for t in range(5):
                    urllib.request.urlretrieve(url, filename=file_name)
                    break
                pass

            per = float(float(i) / float(total_len) * 100)
            percent = str('%.2f' % per)
            strc = '下载进度：' + percent + '%' + '//**//**//' + '正在下载第' + str(i) + '张图片'
            end_time = time.time()
            total_time = total_time + (end_time - start_time)

            total_time_in_min = int(total_time / 60)
            total_time_in_sec = total_time - 60 * total_time_in_min

            left_time = total_time * 100 / per - total_time
            left_time_in_min = int(left_time / 60)
            left_time_in_sec = left_time - 60 * left_time_in_min
            print('\r' + person.title() + ':  ' + strc + '//**//**//' + '已用时间' + str(total_time_in_min) + '分钟' + str(
                '%.2f' % total_time_in_sec) + '秒'
                  + '//**//**//' + '预计剩余时间为' + str(left_time_in_min) + '分钟' + str('%.2f' % left_time_in_sec) + '秒',
                  end='')
        else:
            pass
        print('\n'+'已爬取' + person + '图组并存储于Applications/multithreads/同名文件夹下'+'\n'+'**********爬取完成**********'+'\n')

    def spider(self, current_name):
        person = current_name
        name = str(person)
        search_name = name.replace(' ', '+')
        album_link = self.download_album_url(search_name)                #所有系列的url
        final_url_link = []                                        #最终所有图片的url
        print('正在获取'+current_name+'各图组！')
        ic = 0
        for url_album in album_link:                               #访问各图组
            try:
                html = requests.get(url_album)
            except:
                pass
            ic += 1
            soup_album = BeautifulSoup(html.text, 'html.parser')
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
            perr = 100*ic/len(album_link)
            perrr= float('%.2f' % perr)
            jindu = '获取'+self.current_name+'图组进度：' + str(perrr) + '%'
            print('\r'+jindu, end='')
        print('')
        person = self.current_name
        path = '/Applications/multithreads/' + person
        if os.path.exists(path):
            print('已存在'+person+'的文件夹')
        else:
            os.mkdir(path)
            print('已创建'+person+'的文件夹')

        f=open(path+'/url_info.txt', 'w+')
        print(final_url_link, file=f)
        f.close()
        self.download_img(final_url_link, path, person)


def main():
    ssl._create_default_https_context = ssl._create_unverified_context

    thread = []              #线程池
    person = input('输入搜索的人名（多个人名用逗号分割）:')
    person_list = person.split(',')
    for person in person_list:
        t = SPIDER(person)
        thread.append(t)
        t.start()
    print('所有线程已开启')
    for t in thread:
        t.join()
    print('********************所有爬取完成********************')


main()
