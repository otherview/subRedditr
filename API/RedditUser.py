#-------------------------------------------------------------------------------
# Name:        RedditUser
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     10-10-2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class RedditUser:
    """Simple User class of reddit.com """


    def __init__(self,userName):
        """ Initiates a reddit User, with username """
        self.name = userName
        self.posts = {}
        self.posts['submit'] = {}
        self.posts['comment'] = {}
        self.dataset = {}
        self.commentTrack = {}
        


    def incrementDataset(self,subreddit,idThread):
        
        firstCommented = False
        firstTimeSubreddit = False
        if not self.dataset.has_key(subreddit):
            self.dataset[subreddit] = 1.0
            firstTimeSubreddit = True
            
                
        if not self.commentTrack.has_key(idThread):
            self.commentTrack[idThread] = 1.0
            firstCommented = True
            
        if not firstTimeSubreddit and not firstCommented:
            self.commentTrack[idThread] +=1.0
            self.dataset[subreddit] += 1.0/self.commentTrack[idThread]
        else:
            print "Follow up numa Thread (Valor minorizado)"
        

    def addSubmitPost(self, userPosted):
        """ Adds a submission of Users to the posting Historial """

        if not self.posts['submit'].has_key(userPosted['id']):
            self.posts['submit'][userPosted['id']] = userPosted
        else:
            print "Submission: Already added"
        self.incrementDataset(userPosted['subreddit'],"t3_"+userPosted['id'])
            
    def addCommentPost(self, userPosted):
        """ Adds a Comment post to Users comment Historial """

        if not self.posts['comment'].has_key(userPosted['id']):
            self.posts['comment'][userPosted['id']] = userPosted
        else:
            print "Comment: Already added"
        self.incrementDataset(userPosted['subreddit'],userPosted['link_id'])


    def getAllSubReddits(self):
        '''returns all the subreddits user submited content or commented'''
        
        tmpArray = []
        for submit in self.posts['submit']:
            subreddit = self.posts['submit'][submit]['subreddit']
            if not subreddit in tmpArray:
                tmpArray.append(subreddit)
                
        for comment in self.posts['comment']:
            subreddit = self.posts['comment'][comment]['subreddit']
            if not subreddit in tmpArray:
                tmpArray.append(subreddit)
        
        return tmpArray
            

    def getDataset(self):
        ''' for each subreddir posted, adds up 1 returns array with user::subreddit::Nsubmits+Ncomments'''
        tmpArray = []
        tmpArraySubRedditCounter = {}
        
        
        for submit in self.posts['submit']:
            subreddit = self.posts['submit'][submit]['subreddit']
            if not tmpArraySubRedditCounter.has_key(subreddit):
                tmpArraySubRedditCounter[subreddit] = 0
                
            tmpArraySubRedditCounter[subreddit] += 1
        
        for comment in self.posts['comment']:
            subreddit = self.posts['comment'][comment]['subreddit']
            if not tmpArraySubRedditCounter.has_key(subreddit):
                tmpArraySubRedditCounter[subreddit] = 0
                
            tmpArraySubRedditCounter[subreddit] += 1
        
        for subreddit in tmpArraySubRedditCounter:
            tmpArray.append([self.name,subreddit,tmpArraySubRedditCounter[subreddit]])
        
        return tmpArray
            

def main():
    pass

if __name__ == '__main__':
    main()
