#-------------------------------------------------------------------------------
# Name:        DataViewwer
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     15/03/2014
# Copyright:   (c) Pedro Gomes 2014
# Licence:     
#-------------------------------------------------------------------------------


class DataViewer:
    
    
    def __init__(self, usersData):
        
        
        self.totalPostsMatrix = {}
        self.checkPostsMatrix = {}
        
        
        for user in usersData:
            for subreddit in usersData[user].dataset:
                
                if not self.totalPostsMatrix.has_key(subreddit):
                    self.totalPostsMatrix[subreddit] = {}
                    
                if not self.checkPostsMatrix.has_key(subreddit):
                    self.checkPostsMatrix[subreddit] = {}
                    
                if not self.totalPostsMatrix[subreddit].has_key(user):
                    self.totalPostsMatrix[subreddit][user] = 0.0
                    
                if not self.checkPostsMatrix[subreddit].has_key(user):
                    self.checkPostsMatrix[subreddit][user] = 0
                    
                self.totalPostsMatrix[subreddit][user] += round(usersData[user].dataset[subreddit],2)
                self.checkPostsMatrix[subreddit][user] = 1
        
        return
        
        
    def writeData(self, filenameBase="test"):
        import pandas as pd
        totalPostsMatrix = pd.DataFrame(self.totalPostsMatrix)
        checkPostsMatrix = pd.DataFrame(self.checkPostsMatrix)
        
        excelWriter = pd.ExcelWriter(filenameBase+'.xlsx')
        
        totalPostsMatrix.to_excel(excelWriter,'Total de Posts')
        checkPostsMatrix.to_excel(excelWriter,'Users Posted em Subreddits')
        
        excelWriter.save()
        
        return
        
        