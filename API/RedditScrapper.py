#-------------------------------------------------------------------------------
# Name:        RedditScrapper
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     10-10-2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


class RedditScrapper:
    """ Searches reddit r/all for comments and creates users with their posts"""
    def __init__(self):
        import RedditUsers
        self.authors = []
        self.redditUsers = RedditUsers.RedditUsers()


    def startSearch(self, times=2):
        import json,time, RedditUsers

        data =[]
        final_data = []
        authors= []
        spinTime = 0
        import urllib2
        hdr = { 'User-Agent' : 'subreddit sugestion bot by /u/0view' }
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
                print "\n--- Thread---"
                print "autor :"+str(topicData['author'])
                print "id Thread :" + str(topicData['id'])
                print "subreddit Thread :" + str(topicData['subreddit'])
                print "score Thread :" + str(topicData['score'])
                print "#comment Thread :" + str(topicData['num_comments'])
                print "\n"

            for comment in final_data[0][1]['data']['children']:

                if comment['data'].has_key('author'):
                    comment_data = comment['data']
                    print "-- Commentario -- "
                    print "autor : "+str(comment_data['author'])
                    print "Comment Ups : "+str(comment_data['ups'])
                    print "Comment Downs : "+str(comment_data['downs'])

                    self.authors.append(str(comment_data['author']))
            if spinTime >= times :
                #self.redditUsers.saveUsers()
                return




def main():
    redditScrapper = RedditScrapper()
    redditScrapper.startSearch(times=10)
    with open("authors.txt","w") as filename:
        for auth in redditScrapper.authors:
            filename.write(auth+'\n')
            
    print "cenas"

if __name__ == '__main__':
    main()
