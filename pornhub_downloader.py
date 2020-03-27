from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
import urllib.request
import socket
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
    def spider(personlist, i, pagenum0=1, pagenum1=3, ifnew=0):
        pagenum1 = int(pagenum1)
        pagenum0 = int(pagenum0)
        ifnew=int(ifnew)
        url0 = 'https://www.pornhub.com/video/search?search='
        person = personlist[i]
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        #prefs = {'profile.managed_default_content_settings.images': 2}
        #options.add_experimental_option('prefs', prefs)
        browser = webdriver.Chrome(options=options)
        browser.get("https://www.pornhub.com")
        browser.find_element_by_id("headerLoginLink").click()
        try:
            browser.find_element_by_id("usernameModal").send_keys("2648054636@qq.com")
        except:
            browser.find_element_by_id("username").send_keys("2648054636@qq.com")
        try:
            browser.find_element_by_id("passwordModal").send_keys("9855GWei")
        except:
            browser.find_element_by_id("password").send_keys("9855GWei")
        time.sleep(2)
        try:
            browser.find_element_by_id("signinSubmit").click()
        except:
            browser.find_element_by_id("submit").click()
        SPIDER.sle(5)
        Search_Result_List_key = []                  #系列各自的url
        name = person
        search_name = name.replace(' ', '+')
        url1 = url0 + search_name

        if ifnew==0:
            for page_num in range(pagenum0, pagenum1+1):
                url = url1 + '&page=' + str(page_num)
                browser.get(url)
                print('开始搜索'+name + '的第' + str(page_num) + '页')
                SPIDER.sle(2)
                s = 0
                for s0 in range(2):
                    js = 'window.scrollTo(' + str(0) + ', ' + str(s) + ')'
                    s += 3000
                    s0 += 1
                    browser.execute_script(js)
                    #print('\r'+'进度：' + str('%.2f' % (s0/1.2))+'%', end='')    # 1.2对应range=120
                    SPIDER.sle(0.5)
                html = browser.page_source
                soup = BeautifulSoup(html, 'html.parser')                  #解析html
                search_result_list = soup.find_all('li', attrs={'data-entrycode': 'VidPg-premVid'})        #搜索包含视频url的li

                for li in search_result_list:                               #获取各个系列的href中的link，存入Search_Result_List_url
                    video_key_for_video = li['_vkey']
                    Search_Result_List_key.append(video_key_for_video)
            Keys_list = Search_Result_List_key                         #所有系列的key
            final_url_link = []                                        #最终所有视频的url
            final_video_name = []
            print('\n正在获取各视频！')
            #print(Keys_list)

            for key in Keys_list:                               #获取各视频
                full_url = 'https://www.pornhub.com/view_video.php?viewkey=' + key
                browser.get(full_url)
                video_soup = BeautifulSoup(browser.page_source, 'html.parser')
                target_a = video_soup.find('a', "downloadBtn")
                try:
                    download_url_for_each_video = target_a['href']
                    name_for_each_video = target_a['download']
                    final_url_link.append(download_url_for_each_video)
                    final_video_name.append(name_for_each_video)
                except:
                    pass
            path = '/Applications/Pornhub/' + person

            if os.path.exists(path):
                print('已存在' + person + '的文件夹')
            else:
                os.mkdir(path)
                print('已创建' + person + '的文件夹')
            i = 0

            urltoname = dict(zip(final_video_name, final_url_link))
            url_to_name_file = open(path + '/' + 'temp.txt', 'w+')
            print(urltoname, file=url_to_name_file)
            url_to_name_file.close()

        else:
            path = '/Applications/Pornhub/' + person
            file = open(path+'/'+'temp.txt', 'r')
            info_dict = eval(file.read())
            final_url_link = list(info_dict.values())
            final_url_link = final_url_link[0:]
            final_video_name = list(info_dict.keys())
            final_video_name = final_video_name[0:]
        browser.close()

        #retrieve所有视频

        ALL = len(final_url_link)
        total_time = 0

        socket.setdefaulttimeout(30)
        for i in range(1, 1+len(final_url_link)):
            start_time = time.time()

            url = final_url_link[i]
            name = final_video_name[i]

            path = '/Applications/Pornhub/' + person + '/'
            file_name = path + name + '.mp4'
            try:
                urllib.request.urlretrieve(url, filename=file_name)
            except socket.timeout:
                count = 1
                while count <= 5:
                    try:
                        urllib.request.urlretrieve(url, filename=file_name)
                        break
                    except socket.timeout:
                        err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                        print(err_info)
                        count += 1
                if count > 5:
                    print("downloading video failed!")

            except urllib.error.ContentTooShortError:
                urllib.request.urlretrieve(url, filename=file_name)
            except:
                pass
            per = float(float(i) / float(ALL) * 100)
            percent = str('%.2f' % per)
            strc = '下载进度：' + percent + '%' + '//**//**//' + '正在下载第' + str(i+1) + '部视频' + '//**//**//' + '共' + str(ALL+1) + '部视频'
            end_time = time.time()
            total_time = total_time + (end_time - start_time)

            total_time_in_min = int(total_time / 60)
            total_time_in_sec = total_time - 60 * total_time_in_min

            left_time = total_time * 100 / per - total_time
            left_time_in_min = int(left_time / 60)
            left_time_in_sec = left_time - 60 * left_time_in_min
            print('\r' + strc + '//**//**//' + '已用时间' + str(total_time_in_min) + '分钟' + str(
                '%.2f' % total_time_in_sec) + '秒'
                  + '//**//**//' + '预计剩余时间为' + str(left_time_in_min) + '分钟' + str('%.2f' % left_time_in_sec) + '秒',
                  end='')

def main():
    personlist = input('输入搜索的人名（多个人名用逗号分割）:')
    start = input('输入起始页码:')
    end = input('输入终止页码:')
    start = int(start)
    end = int(end)
    personlist = personlist.split(',')
    ifnew=input('是否从已有url文件开始:')
    ifnew=int(ifnew)
    print(personlist)
    for i in range(len(personlist)):
        person = personlist[i]
        SPIDER.spider(personlist, i, start, end, ifnew=ifnew)
        print('All Finished')
main()
