from Spider import getData,makeabs
import pdb
def process(a):
    res =a
    #res['title'] = res['title'].encode('utf-8')
    res['images'] = [ makeabs(i, a['url']) for i in a['images']]
    res['main_img'] =''
    if res['images']:
        res['main_img'] = res['images'][0]
    return res

url='http://www.anandabazar.com/lifestyle?ref=archive-topnav'
a_xpath1= 'div.row' 
a_xpath2= 'div.grid-item a'
#Note we need 5 entry
data_xpath =[ 
            ['title','div#story_container','div.storypage_cover_story h1','text','join'],
            ['fullstory','div#story_container','div.articleBody p','text','join'],
            ['images','div#story_container','div.articleBody img','src',None],
        ]

all = getData(url,a_xpath1,a_xpath2,data_xpath,100);
all = [process(a) for a in all]

#pdb.set_trace();
import requests
URL ='http://52.89.112.230/api/banglagossip2'
#FIX it remove duplicates...
for d in all:
    r = requests.post(URL, json={"url": d['url'],"_cmd":"search","_unicode":"True"})
    #pdb.set_trace()
    if r.status_code == 200 and len(r.json()['out']) == 0:
        print 'adding new...'
        d['_cmd'] ='post'
        d['_unicode'] ='True'
        r = requests.post(URL, json=d)
        print r.json()
    else:
        print 'duplicate found...'
    print 'duplicate found'
print r.json()