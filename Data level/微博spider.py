#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests

'''
这是新浪微博爬虫试验版
需要补充的地方：   1.登录微博后的uid
                2.保存登录状态的cookies
还有问题的地方：
                3.为了降低风险，建议设置sleep时间，每次操作之间时间要加长
                4.抓取简介中汉字冒号和英文冒号的区分问题还没有解决
                5.最好动态更新cookies
'''
#这里是字符串形式的本人新浪uid type: string
my_own_uid = ''


#type: dict
myheaders={'Host': 'weibo.cn',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate, br',
'Referer': 'https://weibo.cn/' + my_own_uid + '/fans',
'DNT': '1',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'Cache-Control': 'max-age=0'}

#这里的cookies在浏览器工具里面找一下然后填上去, type: dict
mycookies = {'':''}

#获取用户uid的函数，输入值是一个url，里面有uid
def get_uid(url):
    '''
    intype: string
    rtype: string
    '''
    M = re.search(r'[0-9]+', url)
    return M.group(0)

#这个函数已经废弃
def get_name(url):
    '''
    intype: string
    rtype: string
    '''
    return url.split('\xa0')[0]

#获取uid号用户的关注列表
def get_profile(uid):
    '''
    intype: string
    rtype: dict
    '''
    url = 'https://weibo.cn/' + uid + '/info'
    info = requests.get(url, headers = myheaders, cookies = mycookies)
    info.encoding='utf-8'

    info_soup = BeautifulSoup(info.text)
    profl = list(filter(lambda elem:elem.has_attr('class') and elem['class'] == ['c'], info_soup.find_all('div')))
    # M将会是一个处理后的简介字典
    # 这里有中文冒号的问题
    M = str(profl[2]).split('<br/>')
    M = M[1:-2]
    for i in range(len(M)):
        M[i] = M[i].split(':')
    return dict(M[0:2])


#计数器
num = 0

#这个函数的返回值还没有想好是什么
def get_following(uid, depth):
    '''
    intype: str, int
    rtype: 补充
    函数接收两个参数uid和depth，分别表示当前用户和距离开始用户的深度
    遍历每一个关注的用户，以此类推直至深度层数到达depth为止
    用dfs搜索
    '''
    if (depth > 2):
        return
    #计数器
    global num
    
    #获得关注用户的页数，weibo.cn一页十个用户
    url = 'https://weibo.cn/' + uid + '/follow';
    r0 = requests.get(url, headers = myheaders, cookies = mycookies)
    soup0 = BeautifulSoup(r0.text)
    #这里还有些未知的问题没解决，暂且用try except
    try:
        max_page = int(soup0.find_all('input')[4]['value'])
    except:
        max_page = 1
    
    #这里本应是range(1, max_page)的，为方便起见
    for i in range(1, 2):
        url = 'https://weibo.cn/' + uid + '/follow?page=' + str(i);
        #print(url, uid)
        #'''
        r = requests.get(url, headers = myheaders, cookies = mycookies)
        soup = BeautifulSoup(r.text)
        # A是所有table节点组，数据都在table节点组里
        A = soup.find_all('table')
        for ppl in A:
            # cont是用来获取uid的网页内容
            num = num + 1
            soup_finder = ppl.find_all('a');
            
            #这里我也不知道为什么
            if (len(soup_finder) < 3):
                continue
            
            cont = soup_finder[2]['href']
            following_uid = get_uid(cont)
            #print(soup_finder[1].text)
            following_name = soup_finder[1].text
            print(following_name, following_uid)
            dict_ans = get_profile(following_uid)
            dict_ans['me'] = uid
            dict_ans['following'] = following_uid
            dict_ans['following_name'] = following_name
            print(dict_ans)
            get_following(following_uid, depth+1)
        #'''
    
get_following(my_own_uid, 1)
print(num)




