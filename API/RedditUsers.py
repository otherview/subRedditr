#-------------------------------------------------------------------------------
# Name:        RedditUsers
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     10-10-2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class RedditUsers:
    """Complex Users class of reddit.com and Saves/loads to/from DB file """


    def __init__(self):
        """ Initiates a mother class for reddit Users """
        self.users = {}
        self.loadUsers()
        



    def addPost(self, userPosted,kind):
        """ Adds a post to Users posting Historial """
        import RedditUser
        
        if not self.users.has_key(userPosted['author']):
            self.users[userPosted['author']] = RedditUser.RedditUser(userPosted['author'])
            
        if kind == "comment":
            self.users[userPosted['author']].addCommentPost(userPosted)
            
        if kind == "submit":
            self.users[userPosted['author']].addSubmitPost(userPosted)

    def saveUsers(self):
        import pickle

        try:
            with open('redditUsers.db','wb') as handle:
                pickle.dump(self.users,handle)
        except IOError as e:
            # you can print the error here, e.g.
            print(str(e))

        return True

    def loadUsers(self):
        import pickle,os
        if os.path.exists('redditUsers.db'):
            try:
                with open('redditUsers.db','rb') as handle:
                    self.users = pickle.load(handle)
            except IOError as e:
                # you can print the error here, e.g.
                self.users = {}
                print(str(e))

        return True


    def getDataset(self,user):
        
        
        return self.users[user].getDataset()
    
    def getDatasetAllUsers(self):
        
        tmpArray = {}
        for user in self.users:
            tmpArray[user] = self.users[user].getDataset()
        
        return tmpArray
        
    def saveDataset(self, dataset):
        
        with open("datasetRedditUsers.db","wb") as filename:
            for user in dataset:
                for subreddit in user:
                    line = str(subreddit[0])+"::"+str(subreddit[1])+"::"+str(subreddit[2])+"\n"
                    print line
                    filename.write(line)
            
        
        
        return True



def main():
    redditUsers = RedditUsers()
    #redditUsers.addPost({'id':'joao','post':'123 123 123 123'})
    #redditUsers.saveUsers()
    #redditUsers.getDataset('0view')
    dataset = redditUsers.getDatasetAllUsers()
    redditUsers.saveDataset(dataset)
    print "cenas"


if __name__ == '__main__':
    main()
