#!/usr/bin/env python
# coding: utf-8

# In[76]:


def mysplit(mystr, max_seperators, *args):
    '''
    intype: string, list
    rtype: list
    '''
    
    def match(substr, *args):
        '''
        substr: str, args:str
        rtype: int
        '''
        for s in args:
            if substr[:len(s)] == s:
                return len(s)
        return -1
    
    cnt = 0
    ret = []
    num = 0
    i = 0
    
    while i < len(mystr):
        match_len = match(mystr[i:], *args)
        if not match_len == -1:
            if cnt < i:
                ret.append(mystr[cnt:i])
                num = num + 1
                print(cnt)
            #print(i)
            i = i + match_len
            cnt = i
            if (num >= max_seperators):
                break
        i = i + 1
    
    if (not cnt == len(mystr)):
        ret.append(mystr[cnt:])
    return ret


# In[80]:


mysplit('12：3:4: 56：78', 5, '')


# In[12]:


def foo(gooo):
    def goo():
        print(3)
        gooo()
    return goo


# In[16]:


@foo
def time():
    print(10)


# In[61]:


def match(substr, *args):
        pass


# In[41]:


match('123456','1')


# In[75]:


len('：')


# In[ ]:




