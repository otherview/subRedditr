#-------------------------------------------------------------------------------
# Name:        Recommendationr
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     26/11/2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     
#-------------------------------------------------------------------------------


class Recommendationr:
    def __init__(self,redditUsers):

        self.redditUsers = redditUsers
        self.dataset = self.formatDataset()


    def formatDataset(self):
        tmpDataset = {}
    
        for user in self.redditUsers.users:
            tmpDataset[user] = self.redditUsers.users[user].dataset
    
        return tmpDataset
    
    def pearsonSimilarity(self,dataset,person1,person2):
        import Pearson.Pearson as Pearson
        pearson = Pearson.Pearson()
        
       # print "scipy- "
       # print pearson.calculateSimSciPy(dataset,person1,person2)
       # print "oreilly -"
       # print pearson.calculateSim(dataset,person1,person2)
        return pearson.calculateSim(dataset,person1,person2)
        

        
    # Gets recommendations for a person by using a weighted average
    # of every other user's rankings
    def getRecommendations(self,person,similarity=pearsonSimilarity):
      
      prefs = self.dataset
      totals={}
      simSums={}
      for other in prefs:
        # don't compare me to myself
        if other==person: continue
        sim=similarity(self,prefs,person,other)
    
        # ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]:
     
          # only score movies I haven't seen yet
          if item not in prefs[person] or prefs[person][item]==0:
            # Similarity * Score
            totals.setdefault(item,0)
            totals[item]+=prefs[other][item]*sim  #multiplica o que o outro acha pela similiaridade que tem com ele
            # Sum of similarities
            simSums.setdefault(item,0)
            simSums[item]+=sim
    
      # Create the normalized list
      rankings=[(total/simSums[item],item) for item,total in totals.items()]
    
      # Return the sorted list
      rankings.sort()
      rankings.reverse()
      return rankings


def main():
    return

if __name__ == '__main__':
    main()