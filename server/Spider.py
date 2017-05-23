##########################################
#  This is a sinple spider implementation that support:
#  a) Auto pagination
#  b) Auto text extraction.
###########################################
import requests
from bs4 import BeautifulSoup
import pdb
from fake_useragent import UserAgent
ua = UserAgent()

def sm(msg):
    print '>>> ERROR: ',msg

def mget(s,t):
    if t == 'text':
        return s.text
    if t == 'href':
        return s['href']
    else:
        return s.get(t)
    
def getAttrListForXPath(soup, xpath1, xpath2=None, type=None,action=None):
    res = []
    if not soup:
        return res
    try:
        if xpath2 == None:
                res = [ mget(x,'href') for x in soup.select(xpath1) if x]
        else:
                for x in soup.select(xpath1):
                    if not x:
                        continue;
                    for y in x.select(xpath2):
                        res.append(mget(y,type))
        res = list(set(res))
        
        if action == 'join':
            return '\n'.join(res).strip()
        else:
            return res
    except Exception, e:
        print '[ERROR]  Parser issue in getAttrListForXPath'+str(e)
        return []

#url=> text in soup
def get_soup(url):
    try:
        headers = {'User-Agent': ua.random}
        print '[INFO]  Processing '+url
        data = requests.get(url).text
        return BeautifulSoup(data, 'html.parser')
    except:
        return None	
def makeabs(u1,u2):
    if u1[0] == '/':
        return u2[:u2[15:].find('/')+15]+u1
    else:
        return u1
def getAllUrls(url,p_limit):
    if p_limit ==0:
        return [url]
    else:
        return [url]

def getAriticalUrls(soup,a_xpath1,a_xpath2):
    return getAttrListForXPath(soup,'div.row','div.grid-item a','href')
    pass

# Note we need 5 entry for each xpath 
def getDataFromUrl(soup,xpaths):
    #pdb.set_trace();
    ans ={}
    for x in xpaths:
        ans[x[0]] = getAttrListForXPath(soup,x[1],x[2],x[3],x[4])
    return ans
    
    
"""
  One common extrenal libs
"""
def getData(url,a_xpath1, a_xpath2,f_data,a_limit=10,p_limit=1):
    ans =[]
    #1. First get all url to process
    for u0 in getAllUrls(url,p_limit):
        soup = get_soup(u0)
        #2. Get all artical url in this page
        for u2 in getAriticalUrls(soup,a_xpath1,a_xpath2):
            u3 = makeabs(u2,url)
            soup2 = get_soup(u3)
            data = getDataFromUrl(soup2,f_data)
            data['url'] = u3
            ans.append(data)
            if len(ans) > a_limit:
                break;
        if len(ans) > a_limit:
            break;
    return ans

    
#test
url='http://www.anandabazar.com/lifestyle?ref=archive-topnav'
a_xpath1= 'div.row' 
a_xpath2= 'div.grid-item a'
#Note we need 5 entry
data_xpath =[ 
            ['title','div#story_container','div.storypage_cover_story h1','text','join'],
            ['fullstory','div#story_container','div.articleBody p','text','join'],
            ['image','div#story_container','div.articleBody img','src',None],
        ]
print getData(url,a_xpath1,a_xpath2,data_xpath);