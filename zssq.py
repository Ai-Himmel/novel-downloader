import requests
import getopt
import sys
from urllib import quote

opt,argv=getopt.getopt(sys.argv[1:],'ho:s:')
name=''
keyword=''
for o,a in opt:
    if o=='-o':
        name=a
    if o=='-s':
        keyword=a

if keyword=='':
    print "-s option cannot be empty"
    exit(0)
try:keyword=keyword.decode('utf-8')
except:keyword=keyword.decode('gbk')
s=requests.get('http://api.zhuishushenqi.com/book/fuzzy-search?query='+keyword)
j=s.json()
print 'id name auther'
for i in xrange(len(j['books'])):
    print i,j['books'][i]['title'],j['books'][i]['author']
print 'please input book number'
n=int(raw_input())
if name=='':
    name=j['books'][n]['title']+'.txt'
s=requests.get('http://api.zhuishushenqi.com/atoc?view=summary&book='+j['books'][n]['_id'])
j=s.json()
print 'id name auther last chapter'

for i in xrange(len(j)):
    print i,j[i]['name'],j[i]['lastChapter']
print 'please input source number,recommend 716book'
n=int(raw_input())
s=requests.get('http://api.zhuishushenqi.com/atoc/%s?view=chapters'%j[n]['_id'])
j=s.json()
f=open(name,'w')
f.close()
a=len(j['chapters'])
t=0
for i in j['chapters']:
    t+=1
    s=requests.get('http://chapterup.zhuishushenqi.com/chapter/'+quote(i['link']))
    j_tmp=s.json()
    f=open(name,'a+')
    f.write(i['title'].encode('utf8')+'\n')
    f.write(j_tmp["chapter"]['body'].encode('utf8')+'\n')
    f.close()
    
    print '\r%.2f%%'%(float(t)*100/a),


