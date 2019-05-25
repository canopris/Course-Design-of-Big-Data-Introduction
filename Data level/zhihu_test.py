#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import requests
import time
from urllib.parse import unquote
url = r'https://www.zhihu.com/api/v4/members/howard-h/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=10&limit=20'
#url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=40381004'


# In[2]:


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


# In[3]:


sess = requests.session()
sess.headers = myheaders
sess.cookies.update(sess.cookies)
r = sess.get(url)


# In[ ]:





# In[5]:


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
    
    url = get_url(url_token)
    sess = requests.Session()
    sess.headers = myheaders
    response = sess.get(url)
    
    limit = 20
    offset = 0
    
    while not response.json()['paging']['is_end']:
        following_num = response.json()['paging']['totals']
        offset += 20
        response = sess.get(get_url(url_token), params = {'limit': 20, 'offset': offset })
        
        for elem in response.json()['data']:
            new_token = elem['url_token']
            new_url = get_url(elem['url_token'])
            new_sess = requests.Session()
            new_response = new_sess.get(new_url, headers = myheaders)
            try:
                print(elem['url_token'], new_response.json()['paging'])
                get_following(new_token, depth+1, max_depth)
                time.sleep(2)
            except:
                pass
    


# In[6]:


get_url('1234')
get_following('howard-h', 1, 1)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




