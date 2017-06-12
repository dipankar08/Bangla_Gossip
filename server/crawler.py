ALL_SEEDS = [

{	"categories":"lifestyle",
	"url":'http://www.anandabazar.com/lifestyle?ref=archive-topnav',
	"a_xpath1": 'div.row' ,
	"a_xpath2": 'div.grid-item a',
	#Note we need 5 entry
	"data_xpath" : [ 
		['title','div#story_container','div.storypage_cover_story h1','text','join'],
		['fullstory','div#story_container','div.articleBody p','text','join'],
		['images','div#story_container','div.articleBody img','src',None],
	],
},

]




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


all = []
for s in ALL_SEEDS:
	now = getData(s.get('url'),s.get('a_xpath1'),s.get('a_xpath2'),s.get('data_xpath'),100);
	all += [process(a) for a in now]

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