import time
import requests
import os
import urllib.request
import ssl
import threading
from bs4 import BeautifulSoup

'''kat dior,holly michaels,kali renee,lynna nilsson,harmony wonder,
   '''
ssl._create_default_https_context = ssl._create_unverified_context
BASEDIR = '/Applications/Pornpics/'
#BASEDIR = os.getcwd() + '/pornpics/'     #发布版本
temp_str = '目前存在目录'+BASEDIR+'下, 若要更改请输入新文件夹路径: '
c_dir = input(temp_str)
if c_dir:
    BASEDIR = temp_str

'''
if os.path.exists(BASEDIR):
    pass
else:
    os.mkdir(BASEDIR)
'''


def create_dir(person, rpath=BASEDIR):
    path = rpath + person
    if os.path.exists(path):
        print('已存在' + person + '的文件夹')
    else:
        os.mkdir(path)
        print('已创建' + person + '的文件夹')


def save_flag(person, flag):
    file = open(BASEDIR + person + '/flag.txt', 'w+')
    print(flag, file=file)
    file.close()


def load_flag(person, rpath=BASEDIR):
    path = rpath + person
    file = open(path+'/'+'flag.txt', 'r+')
    flag = int(file.read())
    file.close()
    return flag


def getTopPornstars(maxium_page=10):
    """获取前十页的女星"""
    _name = []
    _num = []
    tname = []
    tnum = []
    url0 = 'https://www.pornpics.com/pornstars/'
    for i in range(maxium_page):
        url = url0+str(i)+'/'
        try:
            web = requests.get(url)
            web.encoding = web.apparent_encoding
            soup = BeautifulSoup(web.text,'html.parser')
            tname = soup.find_all(name="span", attrs={"class": "m-name"})
            _name += tname
            tnum = soup.find_all(name="i", answer={"class": "icon icon-galleries"})
            _num += tnum
        except:
            pass
    answer = zip(tname, tnum)
    #raise ValueError('Can't find any pornstar')
    return answer


def download_album_url(name, total=8):
    """ 下载某人的图组url """
    url0 = 'https://www.pornpics.com/search/srch.php?q='+str(name)+'&limit=20&offset='
    root_url = []
    for i in range(total):
        url = url0 + str(20*i)
        for j in range(5):
            try:
                web = requests.get(url)
                web.encoding = web.apparent_encoding
                for item in web.json():
                    root_url.append(item['g_url'])
                print('\r'+'正在获取图组: 已获取'+str(i*20+20)+'组', end='')
                #print('\r'+'进度:'+str((i+1)*100/total)+'%', end='')
                break
            except:
                pass
    return root_url


def save_img(image_url, person, err_list, rpath=BASEDIR):
    path = rpath + person + '/'
    file_name_01 = image_url.split('/')[-1]
    file_name = path + file_name_01
    try:
        urllib.request.urlretrieve(image_url, filename=file_name)
    except urllib.error.URLError:
        err_list.append(image_url)
    except OSError:
        print(file_name)
        pass


def spider(person, rpath=BASEDIR):
    """下载每个图组中包括的图片的url"""
    name = str(person)
    search_name = name.replace(' ', '+')

    create_dir(person=person)

    album_link = download_album_url(search_name)                       #所有系列的根url

    final_url_link = []                                        #最终所有图片的url
    print('\n正在获取各图组！')
    ic = 0
    for url_album in album_link:                               #访问各图组
        try:
            html = requests.get(url_album)

            ic += 1
            soup_album = BeautifulSoup(html.text, 'html.parser')
            each_album_all_url = soup_album.find_all('a', "rel-link")   #每个系列中的所有link

            for link in each_album_all_url:                         #根据每个图组中每张图片的link获取href
                e = link['href']
                if e[:11] == 'https://cdn':
                    final_url_link.append(e)
                elif e[:11] == 'https://ima':
                    final_url_link.append(e)
                else:
                    pass

            perr = 100*ic/len(album_link)
            perrr= float('%.2f' % perr)
            jindu = '获取各图组进度：' + str(perrr) + '%'
            print('\r'+jindu, end='')
        except requests.exceptions.ProxyError:

            pass


    uf = open(BASEDIR + person + '/all_urls.txt', 'w+')
    print(final_url_link, file=uf)
    uf.close()
    print('')
    i = 0
    total_len = len(final_url_link)
    total_time = 0

    error_list = []
    for links in final_url_link:
        start_time = time.time()

        save_img(links, person=person, err_list=error_list)
        i += 1
        per = float(float(i)/float(total_len) * 100)
        percent = str('%.2f' % per)
        strc = '下载进度：'+percent+'%' + '//**//**//' + '正在下载第' + str(i) + '张图片'
        end_time = time.time()
        total_time = total_time + (end_time - start_time)

        total_time_in_min = int(total_time/60)
        total_time_in_sec = total_time - 60 * total_time_in_min

        left_time = total_time * 100 / per - total_time
        left_time_in_min = int(left_time/60)
        left_time_in_sec = left_time - 60*left_time_in_min
        print('\r' + strc + '//**//**//' + '已用时间' + str(total_time_in_min) + '分钟' + str('%.2f' % total_time_in_sec) + '秒'
              '//**//**//'+'预计剩余时间为'+str(left_time_in_min)+'分钟' + str('%.2f'%left_time_in_sec)+'秒', end='')
    f = open(BASEDIR + person + '/error_url.txt', 'w+')
    print(error_list, file=f)
    f.close()
    #下载失败的重新尝试
    print('')
    print('下载失败%d张' % len(error_list))
    print('正在继续下载')
    j = 0
    path = rpath + person + '/'
    for image_url in error_list:
        file_name_01 = image_url.split('/')[-1]
        file_name = path + file_name_01
        j += 1
        for i in range(5):
            try:
                print('\r' + '正在下载第%d张' % j, end='')
                urllib.request.urlretrieve(image_url, filename=file_name)
                break
            except:
                pass

'''
    st_time = time.time()
    while True:
        threads = []
        current_url_album = final_url_link[:10]
        for image_url in current_url_album:
            threads.append(threading.Thread(target=save_img, args=(image_url, person)))
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            threads = []
        final_url_link = final_url_link[10:]
        if len(final_url_link) == 0:
            break

    ed_time = time.time()
    print('多线程耗时：', str(ed_time-st_time))
'''


def main():
    person = input('输入搜索的人名（多个人名用逗号分割）:')
    person_list = person.split(',')
    for person in person_list:

        spider(person)
        print('')
        print('已下载'+person +'图组并存储于Pornpics中同名文件夹下')
        print('**********下载完成**********')
        print('')

    if not len(person_list) == 1:
        print('********************所有下载完成********************')


if __name__ == '__main__':
    main()
