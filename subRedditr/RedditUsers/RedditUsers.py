#-------------------------------------------------------------------------------
# Name:        RedditUsers
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     10-10-2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     
#-------------------------------------------------------------------------------

class RedditUsers:
    """Complex Users class of reddit.com and Saves/loads to/from DB file """


    def __init__(self):
        """ Initiates a mother class for reddit Users """
        self.users = {}
        #Dont Load Users, the Tree will load them
        #self.loadUsers()
        


    def addUsers(self,redditUsers):
        for user in redditUsers.users:
            self.users[redditUsers.users[user].name] = redditUsers.users[user]

    def addPost(self, userPosted,kind):
        """ Adds a post to Users posting Historial """
        import RedditUser.RedditUser as RedditUser
        
        if not self.users.has_key(userPosted['author']):
            self.users[userPosted['author']] = RedditUser.RedditUser(userPosted['author'])
            
        if kind == "comments":
            self.users[userPosted['author']].addCommentPost(userPosted)
            
        if kind == "submitted":
            self.users[userPosted['author']].addSubmitPost(userPosted)

    def saveUsers(self):
        import json
        try:
            with open('redditUsers.db','wb') as handle:
                for user in self.users:
                    handle.write(json.dumps({'redditUser':user,'commentTrack':json.dumps(self.users[user].commentTrack),'dataset':json.dumps(self.users[user].dataset),'posts':json.dumps(self.users[user].posts)})+"\n")
        except IOError as e:
            # you can print the error here, e.g.
            print(str(e))

        return
    

    def loadUsers(self):
        import json,os
        import RedditUser.RedditUser as RedditUser
        
        if os.path.exists('redditUsers.db'):
            try:
                with open('redditUsers.db','rb') as handle:
                    for line in handle:
                        lineRead = line
                        lineUser = json.loads(lineRead)
                        redditUser = RedditUser.RedditUser(lineUser['redditUser'])
                        redditUser.commentTrack = json.loads(lineUser['commentTrack'])
                        redditUser.dataset = json.loads(lineUser['dataset'])
                        redditUser.posts = {}
                        redditUser.posts['comments'] = json.loads(lineUser['posts'])['comments']
                        redditUser.posts['submitted'] = json.loads(lineUser['posts'])['submitted']
                        self.users[lineUser['redditUser']] = redditUser

                    
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

    def toJSON(self):
        import json
        
        returnJSON = {}
        for user in self.users:
            returnJSON[user] = {'redditUser':user,'commentTrack':json.dumps(self.users[user].commentTrack),'dataset':json.dumps(self.users[user].dataset),'posts':json.dumps(self.users[user].posts)}
        
    
        return returnJSON
    
    def get_Most_Posted_Sub(self):
        tmpDataset =  {}
        for user in self.users:
            for tmpReddit in self.users[user].dataset:
                
                if tmpDataset.has_key(tmpReddit):
                    tmpDataset[tmpReddit] += 1 
                else:
                    tmpDataset[tmpReddit] = 1 + (1 - 1 / self.users[user].dataset[tmpReddit])
                
        
        
        print "Lista de Subreddits em Votacao:"
        print tmpDataset
        print "Apenas selecionar os que tem alguma interseccao entre utilizadores"
        tmpDataset = dict(("r/"+k, v) for k, v in tmpDataset.items() if v>1.0)
        print "Se sao muitos vamos filtrar os primeiros 3"
        maxSubreddits = [sub for sub in sorted(tmpDataset, key = tmpDataset.get)]
        maxSubreddits.reverse()
        if len(maxSubreddits) < 3:
            print "MUITOS POUCOS PARA INTERSECAO"
            print maxSubreddits[0]
        else:
            for sub in maxSubreddits[:3]:
                print sub +" -  %f" % tmpDataset[sub]
        
        return maxSubreddits[:3]
        


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
