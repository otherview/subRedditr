#-------------------------------------------------------------------------------
# Name:        RedditUserScrapper
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     17-10-2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class RedditUserScrapper:
    """Scrapes a user of reddit.com """


    def __init__(self):
        """ Initiates the RedditUsers"""
        import RedditUsers
        self.redditUsers = RedditUsers.RedditUsers()


    def scrapeUser(self, rdtUser,rescan=False):
        """ Scrapes www.reddit.com/user/rdtUser/(comments and submited)/.json """
        
        if self.redditUsers.users.has_key(rdtUser) and not rescan or rdtUser == "[deleted]":
                print "User: "+rdtUser+" already scanned!"
                return None
        self.scrapeUserComments(rdtUser)
        self.scrapeUserSubmits(rdtUser)
        
        self.redditUsers.saveUsers()
        
        return
      
        
    
    def scrapeUserComments(self,rdtUser):
        """ Scrapes www.reddit.com/user/rdtUser/comments/.json """
        import json,time, urllib2
        

        hdr = { 'User-Agent' : 'subreddit sugestion bot by /u/0view' }
        url = 'http://www.reddit.com/user/'+rdtUser+'/comments/.json?limit=100'
        tmpCollectedData = []
        collectedData = []
        
        while not tmpCollectedData and len(tmpCollectedData)<100:
            try:
                request = urllib2.Request(url, headers=hdr)
                response = urllib2.urlopen(request)
            except :
                print "BUGGGGG"
                return None
            html = response.read()
            tmpCollectedData.append(json.loads(html))
            collectedData.extend(tmpCollectedData[0]['data']['children'])
            lastOfPage = tmpCollectedData[0]['data']['after']
            tmpCollectedData = []
            if not lastOfPage :
                break
            url = 'http://www.reddit.com/user/'+rdtUser+'/comments/.json?limit=100&after='+lastOfPage
  

        for posted in collectedData:
            userPosted = posted['data']
            
            print "\n--- COMMENT User: "+ str(userPosted['author'])+"---"
            #for field in userPosted:
            #    if isinstance(userPosted[field],basestring):
            #        print (field +": "+userPosted[field]).encode('utf-8')
            #    else:
            #        print field +": "+str(userPosted[field])
            #print "\n"

            self.redditUsers.addPost(userPosted,"comment")
        
        
        return


    def scrapeUserSubmits(self,rdtUser):
            """ Scrapes www.reddit.com/user/rdtUser/submit/.json """
            import json,time, urllib2
            
            
    
            hdr = { 'User-Agent' : 'subreddit sugestion bot by /u/0view' }
            url = 'http://www.reddit.com/user/'+rdtUser+'/submitted/.json?limit=100'
            tmpCollectedData = []
            collectedData = []
            
            while not tmpCollectedData and len(tmpCollectedData)<100:
                
                request = urllib2.Request(url, headers=hdr)
                response = urllib2.urlopen(request)
                html = response.read()
                tmpCollectedData.append(json.loads(html))
                collectedData.extend(tmpCollectedData[0]['data']['children'])
                lastOfPage = tmpCollectedData[0]['data']['after']
                tmpCollectedData = []
                if not lastOfPage :
                    break
                url = 'http://www.reddit.com/user/'+rdtUser+'/submitted/.json?limit=100&after='+lastOfPage
      
    
            for posted in collectedData:
                userPosted = posted['data']
                
                print "\n--- SUBMIT Post from: "+ str(userPosted['author'])+"---"
                #for field in userPosted:
                #    if isinstance(userPosted[field],basestring):
                #        print (field +": "+userPosted[field]).encode('utf-8')
                #    else:
                #        print field +": "+str(userPosted[field])
                #print "\n"
                
                self.redditUsers.addPost(userPosted,"submit")
            
           
            return

        

def main():
    redditUserScapper = RedditUserScrapper()
    print "Scraper Initiated"
    with open("authors.txt") as filename:
        for line in filename:
            print "---> "+line.rstrip("\n")+" <---"
            redditUserScapper.scrapeUser(line.rstrip("\n"))
    #redditUserScapper.scrapeUser('sparktuga')
    print "cenas"
    

if __name__ == '__main__':
    main()
