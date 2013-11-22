#-------------------------------------------------------------------------------
# Name:        Evaluation O'reilly Recomendation
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     21-11-2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


class Evaluation:
    
    def __init__(self):
        
        self.recomendationDataset = {}
        self.dataset = {}
        self.removedSubreddit = {}
        pass
    
    def removeRandomSubreddit(self,dataset):
        import random

        
        for user in dataset:
            self.removedSubreddit[user] = random.choice( dataset[user].keys() )
            self.dataset[user] = dataset[user]
            self.dataset[user].pop(self.removedSubreddit[user])
       
        return
    
    def addRecomendation(self,recomendations, user):
        
        self.recomendationDataset[user] = recomendations
        
        return
    
    def finalEvaluation(self):
        precision = 0.0
        
        for user in self.dataset:
            if self.removedSubreddit[user] in [score[1] for score in self.recomendationDataset[user]]:
                precision +=1.0
                
        return precision/len(self.dataset)
            


def main():
   evaluation = Evaluation()
   
    

if __name__ == '__main__':
    main()