#-------------------------------------------------------------------------------
# Name:        Evaluationr
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     26/11/2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     
#-------------------------------------------------------------------------------


class Evaluationr:
    
    def __init__(self, redditUsers, recomendationr):
        
        self.recomendationDataset = {}
        self.dataset = {}
        self.removedSubreddit = {}
        
        self.redditUsers = self.getInDataset(redditUsers)
        self.recomendationr = recomendationr
        
        
        
        return
    
    def getInDataset(self,redditUsers):
        tmpDataset = {}
        
        for user in redditUsers.users:
            tmpDataset[user] = redditUsers.users[user].getUserSubreddits()
        
        return tmpDataset
    
    def evaluateTopNSubredditRecomendations(self):
        
        self.predictionDataset  = {}
        self.deleted = {}
        
        for user in self.redditUsers:
            
            self.removeTopNSubreddit(user)
        
        for user in self.redditUsers:
            self.predictionDataset[user] = self.recomendationr.getRecommendations(user)
        
        totals = self.getTotalsPredicted() 
        
        return totals
    
    
   
    
    def removeTopNSubreddit(self,user,n=5):

        self.deleted[user] = {}
        
        toRemove = sorted(self.redditUsers[user].iteritems(), key=lambda x:x[1])[-n:]
        for rem in toRemove:
            self.deleted[user] = rem
            self.redditUsers[user].pop(rem[0])
        
        return

    def getTotalsPredicted(self):
        totals = 0.0
        totalsLen = 0.0
        for user in self.redditUsers:
            for subreddit in self.deleted[user]:
                totalsLen+=1.0
                if subreddit in [subredditName[1] for subredditName in self.predictionDataset[user]] :
                    totals +=1.0
        return totals/totalsLen


    def evaluateNumberOfPosts(self,user):
        self.predictionDataset  = {}
        self.deleted = {}
        self.removeTopNSubreddit(user)
        self.predictionDataset[user] = self.recomendationr.getRecommendations(user)
        
        return

def main():
   evaluationr = Evaluationr()
   
    

if __name__ == '__main__':
    main()