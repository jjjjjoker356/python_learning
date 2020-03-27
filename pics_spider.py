from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
import urllib.request
import ssl

class SPIDER():
    ssl._create_default_https_context = ssl._create_unverified_context

    def sle(a):
        time.sleep(a)

    def scroll(self, browser, length, counts):
        browser = browser
        for c in range(counts):
            js = 'window.scrollTo(' + str(0) + ', ' + str(c) + ')'
            c += length
            browser.execute_script(js)
            time.sleep(1)
    def spider(personlist, i):
        url0 = 'https://www.pornpics.com/?q='
        person = personlist[i]
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option('prefs', prefs)
        browser = webdriver.Chrome(options=options)
        SPIDER.sle(1)
        Search_Result_List_url = []                  #系列各自的url
        name = person
        search_name = name.replace(' ', '+')
        url = url0 + search_name
        browser.get(url)
        print('开始搜索'+name)
        SPIDER.sle(2)
        s = 0
        for s0 in range(40):
            js = 'window.scrollTo(' + str(0) + ', ' + str(s) + ')'
            s += 2000
            s0 += 1
            browser.execute_script(js)
            #print('\r'+'进度：' + str('%.2f' % (s0/1.2))+'%', end='')    # 1.2对应range=120

            SPIDER.sle(0.5)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')                  #解析html
        Search_Result_List = soup.find_all('a', "rel-link")        #搜索人名后出现的所有系列的<a>

        for a in Search_Result_List:                               #获取各个系列的href中的link，存入Search_Result_List_url
            c= a['href']
            Search_Result_List_url.append(c)
        Album_Link = Search_Result_List_url                        #所有系列的url
        final_url_link = []                                        #最终所有图片的url
        print('\n正在获取各图组！')
        ic = 0
        for url_album in Album_Link:                               #访问各图组
            browser.get(url_album)
            s = 0
            ic+=1
            for s0 in range(2):
                js = 'window.scrollTo(' + str(0) + ', ' + str(s) + ')'
                s += 5000
                browser.execute_script(js)
                time.sleep(0.1)
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


            perr = 100* ic/len(Album_Link)
            perrr= float('%.2f'%perr)
            jindu = '获取图组进度：' + str(perrr) + '%'
            print('\r'+ jindu, end='')
        print('')
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
            print('\r' + strc + '//**//**//' + '已用时间' + str(total_time_in_min) + '分钟' + str('%.2f'%total_time_in_sec) + '秒'
                  + '//**//**//' + '预计剩余时间为'+str(left_time_in_min)+'分钟' + str('%.2f'%left_time_in_sec)+'秒', end='')
        else:
            pass
        browser.close()

def main():
    person = input('输入搜索的人名（多个人名用逗号分割）:')
    personlist = person.split(',')
    print(personlist)
    for i in range(len(personlist)):
        person = personlist[i]
        SPIDER.spider(personlist,i)
        print('')
        print('已爬取'+person +'图组并存储于Applications/Pornpics/同名文件夹下')
        print('**********爬取完成**********')
        print('')
    print('********************所有爬取完成********************')

main()
