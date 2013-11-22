import json
import time
data =[]
final_data = []
import urllib2
response = urllib2.urlopen('http://www.reddit.com/r/all/top.json')
html = response.read()
data.append(json.loads(html))
print "cenas"
for topic in data[0]['data']['children']:
    print "A ir buscar o "+'http://www.reddit.com'+topic['data']['permalink']+'comments.json'
    time.sleep(15)
    
    responseTopic = urllib2.urlopen('http://www.reddit.com'+topic['data']['permalink']+'comments.json')
    htmlTopic = responseTopic.read()
    final_data.append(json.loads(htmlTopic))
    print "cenas2"
print "cenas3"
for line in html:
    print line
    data.append(json.loads(line))
    print "ola"
    
