#!/usr/bin/env python3
# coding: utf-8

import json
import requests
import time
from urllib.parse import unquote


start_url_token = 'xxxxxxxxx'
max_depth       = 2
vis = {}
##重要说明
##重要说明
##重要说明
'''
start_url_token 是知乎用户的一个令牌
max_depth 是关系网络的最大深度
vis 是一个访问记录表0:从未访问过，1:正在访问没结束，2:已访问并结束
'''

myheaders = {
'Host': 'www.zhihu.com',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'DNT': '1',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'Cache-Control': 'max-age=0',
'TE': 'Trailers'
}


def get_url(url_token):
    '''
    url_token: str
    rtype: str
    '''
    url = 'https://www.zhihu.com/api/v4/members/' + url_token + '/followees?include=data[*].answer_count,'     'articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    return url

def query(url, begin, limit):
    '''
    可能可以考虑session
    '''
    myparams = {'limit': limit, 'offset': begin }
    return requests.get(url, params=myparams, headers=myheaders)

def get_following(url_token, depth, max_depth):
    '''
    url_token: str
    rtype str
    '''
    
    if depth > max_depth:
        return
    
    global vis
    vis['url_token'] = 1
    url = get_url(url_token)
    sess = requests.Session()
    sess.headers = myheaders
    response = sess.get(url)
    
    limit = 20
    offset = 0
    response.encoding='unicode'
    rejson = response.json()
    while True:
        with open(start_url_token+'.txt', 'a') as f:
                    f.write(response.text)
        following_num = rejson['paging']['totals']
        
        
        for elem in rejson['data']:
            new_token = elem['url_token']
            new_url = get_url(new_token)
            new_sess = requests.Session()
            print(url_token, '   ------->   ', new_token, '  第', depth, '级')
            print('用户：'+ elem['name'] + '  性别：' + str((lambda g: '男' if g else '女')(elem['gender'])) + '  简介：'+ elem['headline'])
            if new_token in vis:
                continue
            new_response = new_sess.get(new_url, headers = myheaders)
            try:
                get_following(new_token, depth+1, max_depth)
                
            except:
                pass
        offset += 20
        response = sess.get(get_url(url_token), params = {'limit': 20, 'offset': offset })
        rejson = response.json()
        
        response.encoding='utf-8'
        if rejson['paging']['is_end']:
            break

    vis['url_token'] = 2
    


if __name__ == '__main__':
    with open(start_url_token+'.txt', 'w') as f:
        pass
    get_following(start_url_token, 1, max_depth)

