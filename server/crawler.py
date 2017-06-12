ALL_SEEDS = [

{	"categories":"lifestyle",
	"url":'http://www.anandabazar.com/lifestyle?ref=archive-topnav',
	"a_xpath1": 'div.row' ,
	"a_xpath2": 'div.grid-item a',
	#Note we need 5 entry
	"data_xpath" : [ 
		['title','div#story_container','div.storypage_cover_story h1','text','join'],
		['fullstory','div#story_container','div.articleBody p','text','join'],
		['images','div#story_container','img','src',None],
	],
    "ignoreimg":["adblocker"]
},
{	"categories":"science",
	"url":'http://www.anandabazar.com/others/science?ref=archive-topnav',
	"a_xpath1": 'div.row' ,
	"a_xpath2": 'div.grid-item a',
	#Note we need 5 entry
	"data_xpath" : [ 
		['title','div#story_container','div.storypage_cover_story h1','text','join'],
		['fullstory','div#story_container','div.articleBody p','text','join'],
		['images','div#story_container','img','src',None],
	],
    "ignoreimg":["adblocker"]
},
{	"categories":"travel",
	"url":'http://www.anandabazar.com/travel?ref=science-OtherSec',
	"a_xpath1": 'div.row' ,
	"a_xpath2": 'div.grid-item a',
	#Note we need 5 entry
	"data_xpath" : [ 
		['title','div#story_container','div.storypage_cover_story h1','text','join'],
		['fullstory','div#story_container','div.articleBody p','text','join'],
		['images','div#story_container','img','src',None],
	],
    "ignoreimg":["adblocker"]
},
{	"categories":"entertainment",
	"url":'http://www.anandabazar.com/entertainment?ref=travel-topnav',
	"a_xpath1": 'div.row' ,
	"a_xpath2": 'div.grid-item a',
	#Note we need 5 entry
	"data_xpath" : [ 
		['title','div#story_container','div.storypage_cover_story h1','text','join'],
		['fullstory','div#story_container','div.articleBody p','text','join'],
		['images','div#story_container','img','src',None],
	],
    "ignoreimg":["adblocker"]
},
{	"categories":"women",
	"url":'http://www.anandabazar.com/women?ref=strydtl-searchresult-topnav',
	"a_xpath1": 'div.row' ,
	"a_xpath2": 'div.grid-item a',
	#Note we need 5 entry
	"data_xpath" : [ 
		['title','div#story_container','div.storypage_cover_story h1','text','join'],
		['fullstory','div#story_container','div.articleBody p','text','join'],
		['images','div#story_container','img','src',None],
	],
    "ignoreimg":["adblocker"]
},

]




from Spider import getData,makeabs
import pdb
import re
def process(a,s):
    res =a
    #res['title'] = res['title'].encode('utf-8')
    res['images'] = [ makeabs(i, a['url']) for i in a['images']]
    #Seeting main im is trickey. 
    res['main_img'] =''
    if res['images']:
        for i in res['images']:
            for j in s.get('ignoreimg'):
                if j in i:
                    continue;
                res['main_img'] = i;
                break;
    res['categories'] = s.get('categories')
    if res['fullstory']:
        res['fullstory'] = re.sub("\n+","\n",res['fullstory']).strip();
        res['fullstory'] = re.sub("[ \t]+"," ",res['fullstory'])
    return res


all = []
for s in ALL_SEEDS:
	now = getData(s.get('url'),s.get('a_xpath1'),s.get('a_xpath2'),s.get('data_xpath'),30);
	all += [process(a,s) for a in now]

#pdb.set_trace();
import requests
URL ='http://52.89.112.230/api/banglagossip2'
#FIX it remove duplicates...
for d in all:
	d['_cmd'] = 'create'
	r = requests.post(URL, json=d)
    #pdb.set_trace()
	if r.status_code == 200:
		res = r.json();
		print res['status'],res['msg']
	else:
		print 'Internal error..'