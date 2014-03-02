#-------------------------------------------------------------------------------
# Name:        DataFetchr
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     26/11/2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     
#-------------------------------------------------------------------------------

class DataFetchr:
    """Class for fetching web data, either new authors/reddit users or fetching scrapping their comments/posts"""
    """Editted to fetch in tree-style subreddits"""
    
    def __init__(self):
        self.authors = []
       
    
    def fetchMoreUsers(self,times=2):
        import json,time,urllib2
        
        data =[]
        final_data = []
        self.authors= []
        spinTime = 0
        
        hdr = { 'User-Agent' : 'subreddit sugestionr bot by /u/0view' }
        url = 'http://www.reddit.com/r/all/top.json?limit=1000&sort=top&t=day'
        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        html = response.read()
        data.append(json.loads(html))
        latestTopic = ""

        #Vai procurar cada topico
        for topic in data[0]['data']['children']:
            spinTime +=1
            if isinstance(topic,dict):
                print "A ir buscar o "+'http://www.reddit.com'+topic['data']['permalink']+'comments.json?limit=100'
                latestTopic = topic['data']['id']
                time.sleep(5)
                
                url = 'http://www.reddit.com'+topic['data']['permalink']+'comments.json'
                req = urllib2.Request(url, headers=hdr)
                responseTopic = urllib2.urlopen(req)
                htmlTopic = responseTopic.read()
                final_data.append(json.loads(htmlTopic))
                topicData = final_data[0][0]['data']['children'][0]['data']
                #print "\n--- Thread---"
                #print "autor :"+str(topicData['author'])
                #print "id Thread :" + str(topicData['id'])
                #print "subreddit Thread :" + str(topicData['subreddit'])
                #print "score Thread :" + str(topicData['score'])
                #print "#comment Thread :" + str(topicData['num_comments'])
                #print "\n"

            for comment in final_data[0][1]['data']['children']:

                if comment['data'].has_key('author'):
                    comment_data = comment['data']
                    #print "-- Commentario -- "
                    #print "autor : "+str(comment_data['author'])
                    #print "Comment Ups : "+str(comment_data['ups'])
                    #print "Comment Downs : "+str(comment_data['downs'])

                    self.authors.append(str(comment_data['author']))
            if spinTime >= times :
                return self.authors



    def scrapeUser(self,redditUsers,rdtUser,rescan=False):
        """ Scrapes www.reddit.com/user/rdtUser/comments/.json  and then www.reddit.com/user/rdtUser/submit/.json """
        import json, time, urllib2
        
        if redditUsers.users.has_key(rdtUser) and not rescan or rdtUser == "[deleted]":
                #print "User: "+rdtUser+" already scanned!"
                return None
        
        for typeCommentOrSubmit in ['comments','submitted']:
            
            hdr = { 'User-Agent' : 'subreddit sugestion bot by /u/0view' }
            url = 'http://www.reddit.com/user/'+rdtUser+'/'+typeCommentOrSubmit+'/.json?limit=100'
            tmpCollectedData = []
            collectedData = []
            
            while not tmpCollectedData and len(tmpCollectedData)<100:
                try:
                    request = urllib2.Request(url, headers=hdr)
                    response = urllib2.urlopen(request)
                except :
                    print "Internets Bugs"
                    return None
                html = response.read()
                tmpCollectedData.append(json.loads(html))
                collectedData.extend(tmpCollectedData[0]['data']['children'])
                lastOfPage = tmpCollectedData[0]['data']['after']
                tmpCollectedData = []
                if not lastOfPage :
                    break
                url = 'http://www.reddit.com/user/'+rdtUser+'/'+typeCommentOrSubmit+'/.json?limit=100&after='+lastOfPage
      
    
            for posted in collectedData:
                userPosted = posted['data']
                
                #print "\n--- COMMENT User: "+ str(userPosted['author'])+"---"   
                redditUsers.addPost(userPosted,typeCommentOrSubmit)
            
        
    def fetchSubReddit(self,subReddit,depth=5):
        """ Scrapes http://www.reddit.com/r/SUBREEDIT/top.json?limit=1000&sort=top&t=day for Users in a DEPTH number of top post"""
        import json,time,urllib2
        import sys
        reload(sys)
        sys.setdefaultencoding("utf-8")

        
        data =[]
        final_data = []
        self.authors= []
        spinTime = 0
        
        domain = u'http://www.reddit.com'
        hdr = { 'User-Agent' : 'subreddit sugestionr bot by /u/0view','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' }
        url = (u'/' + subReddit+'/top.json?limit=1000&sort=top&t=day').encode('utf-8')
        url = domain + url

        req = urllib2.Request(url, headers=hdr)
        response = urllib2.urlopen(req)
        html = response.read()
        data.append(json.loads(html))
        latestTopic = ""

        #Vai procurar cada topico
        for topic in data[0]['data']['children']:
            spinTime +=1
            if isinstance(topic,dict):
                print "A ir buscar o "+domain+topic['data']['permalink']+'comments.json?limit=100'
                latestTopic = topic['data']['id']
                time.sleep(1)
                
                url = (topic['data']['permalink']+'comments.json').encode('utf-8')
                url = urllib2.quote(url)
                url = domain + url
                
                req = urllib2.Request(url, headers=hdr)
                responseTopic = urllib2.urlopen(req)
                htmlTopic = responseTopic.read()
                final_data.append(json.loads(htmlTopic))
                topicData = final_data[0][0]['data']['children'][0]['data']
                #print "\n--- Thread---"
                #print "autor :"+str(topicData['author'])
                #print "id Thread :" + str(topicData['id'])
                #print "subreddit Thread :" + str(topicData['subreddit'])
                #print "score Thread :" + str(topicData['score'])
                #print "#comment Thread :" + str(topicData['num_comments'])
                #print "\n"

            for comment in final_data[0][1]['data']['children']:

                if comment['data'].has_key('author'):
                    comment_data = comment['data']
                    #print "-- Commentario -- "
                    #print "autor : "+str(comment_data['author'])
                    #print "Comment Ups : "+str(comment_data['ups'])
                    #print "Comment Downs : "+str(comment_data['downs'])

                    self.authors.append(str(comment_data['author']))
            if spinTime >= depth :
                return self.authors

        
        return 


def main():
    pass

if __name__ == '__main__':
    main()