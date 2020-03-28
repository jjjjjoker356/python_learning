
import json,requests
from bs4 import BeautifulSoup

def download_album_url(name, total=10):
    """ 下载某页面的信息 """
    url0 = 'https://www.pornpics.com/search/srch.php?q='+str(name)+'&limit=20&offset='
    root_url = []
    for i in range(total):
        url = url0 + str(20*i)
        web = requests.get(url)
        web.encoding = web.apparent_encoding
        for item in web.json():
            root_url.append(item['g_url'])
        print('\r'+'进度:'+str((i+1)*100/total)+'%', end='')
    return root_url


