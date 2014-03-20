#-------------------------------------------------------------------------------
# Name:        SubRedditr
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     26/11/2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     
#-------------------------------------------------------------------------------


class SubRedditr:
    
    def __init__(self):
        import DataFetchr.DataFetchr as DataFetchr
        import RedditUsers.RedditUsers as RedditUsers
        import Florest.Florest as Florest 
        
        self.dataFetchr = DataFetchr.DataFetchr()
        #self.redditUsers = RedditUsers.RedditUsers()
        self.florest = Florest.Florest()
 


    def fetchMoreUsers(self):
        return self.dataFetchr.fetchMoreUsers(times=1)
        
    def scrapeUsers(self,users):
        import RedditUsers.RedditUsers as RedditUsers
        scrapedUsers  = RedditUsers.RedditUsers()
        for user in users:
            print self.dataFetchr.scrapeUser(scrapedUsers,user)
        
        return scrapedUsers
    

    
    def saveUsers(self):
        self.redditUsers.saveUsers()
        
    def getRecomendations(self,user,RedditUsers):
        import Recommendationr.Recommendationr as Recommendationr
        
        self.recomendationr = Recommendationr.Recommendationr(RedditUsers)
        print self.recomendationr.getRecommendations(user)
        return
    
    
    def evaluateRecomendRightSubReddit(self,redditUsers):
        import Evaluationr.Evaluationr as Evaluationr
        import Recommendationr.Recommendationr as Recommendationr
        
        self.recomendationr = Recommendationr.Recommendationr(redditUsers)
        self.evaluationr = Evaluationr.Evaluationr(redditUsers,self.recomendationr)
        
        print self.evaluationr.evaluateTopNSubredditRecomendations()
        
        
    def evaluateNumberOfPosts(self,user,redditUsers):
        import Evaluationr.Evaluationr as Evaluationr
        import Recommendationr.Recommendationr as Recommendationr
        
        self.recomendationr = Recommendationr.Recommendationr(redditUsers)
        self.evaluationr = Evaluationr.Evaluationr(redditUsers,self.recomendationr)
        
        print self.evaluationr.evaluateNumberOfPosts(user)
        
        
    def create_Tree(self,description):
        return self.florest.addTree(description)
    
    
    
    def fetch_SubReddit(self,subReddit):
        subRedditUsers_Dataset = self.dataFetchr.fetchSubReddit(subReddit,depth=2)

        return subRedditUsers_Dataset
    
    def add_Users_To_Node(self,tree,subRedditName,users):
        
        tree.add_Users_To_Node(subRedditName,users)
        return
    
    
    
    def scrape_Tree_subReddit(self, TreeDescription, StartingSubReddit, Depth = 40):
        
        class pilhaTree:
            
            
            class pilhaElement:
                def __init__(self, startSubreddit, subRedditParent = False ):
                    self.name = startSubreddit
                    self.was_parsed = False
                    if ( subRedditParent):
                        self.parent = subRedditParent.name
                
                def getParent(self,):
                    return self.parent
                
               
                
            def __init__(self, startSubreddit):
                self.pilha = []
                tmpToParse_Subreddit = self.pilhaElement(startSubreddit)
                self.pilha.append(tmpToParse_Subreddit)
                
            
            def parsed(self, subReddit):
                index = self.pilha.index(subReddit)
                self.pilha[index].was_parsed = True
            
            def getNext(self):
                for subReddit in self.pilha:
                    if (not subReddit.was_parsed):
                        return subReddit
                return False
            
            def add_toParse_Subreddit(self, subReddit, subRedditParent):
                if not subReddit in [x.name for x in self.pilha]:
                    tmpToParse_Subreddit = self.pilhaElement(subReddit, subRedditParent)
                    self.pilha.append(tmpToParse_Subreddit)
                    return 1
                else:
                    return 0
                    
            
        tmpTree = self.florest.get_Tree(TreeDescription)
        statusDepth = 0
        
        
        pilha = pilhaTree(StartingSubReddit)
        nextSubReddit = pilha.getNext()
        
        while nextSubReddit and statusDepth != Depth :
            
            
            statusDepth = statusDepth +1
            newUsers = self.fetch_SubReddit(nextSubReddit.name)
            new_Scrapped_Users = self.scrapeUsers(newUsers)
            if statusDepth == 1:
                tmpTree.add_node(str(nextSubReddit.name))  
            else:
                tmpTree.add_node(str(nextSubReddit.name),parent=str(nextSubReddit.getParent()))
                
            pilha.parsed(nextSubReddit) 
            tmpTree.add_Users_To_Node(nextSubReddit.name,new_Scrapped_Users)
            
            nextSubRedditCounter = 0
            for unParsedSubR in tmpTree.tree.get_node(nextSubReddit.name).users.get_Most_Posted_Sub():
                nextSubRedditCounter +=pilha.add_toParse_Subreddit(unParsedSubR, nextSubReddit)
                if(nextSubRedditCounter ==3):
                    break
                
                
                
            nextSubReddit = pilha.getNext()
        
        
      
    
    
    
def main():
    testTree = test_Create_Scrape_SubReddit()
    
    #testTree = test_Load_Tree()
    
    test_dataViewer(testTree)
    
    #testTree = test_recomendation_user()


    return


def test_Create_Scrape_SubReddit():
    '''Test Auto Scraper'''
     
    subRedditr = SubRedditr()
    treeDescription = "Scraper Tree at Best Topic of Today"
    tree = subRedditr.create_Tree(treeDescription)
    
    subRedditr.scrape_Tree_subReddit(treeDescription,"r/technology")
    tree.save_To_File('Best-Today-Tree.db')
    return tree
    
def test_Load_Tree():
    subRedditr = SubRedditr()
    treeDescription = "Scraper Tree at Best Topic of Today"
    tree = subRedditr.create_Tree(treeDescription)
    tree.load_From_File('Best-Today-Tree.db')
    return tree
    
def test_recomendation_user():
    
    subRedditr = SubRedditr()
    treeDescription = "Scraper Tree at Best Topic of Today"
    tree = subRedditr.create_Tree(treeDescription)
    tree.load_From_File('Best-Today-Tree.db')
    
    subRedditr.getRecomendations('xxsilence',tree.tree.get_node("r/portugal").users)
    subRedditr.evaluateRecomendRightSubReddit(tree.tree.get_node("r/portugal").users)
    subRedditr.evaluateNumberOfPosts('xxsilence',tree.tree.get_node("r/portugal").users)
    
    return tree

def test_dataViewer(treeData):
    '''Data Viewer Test'''
    
    from DataViewer.DataViewer import DataViewer
    dataViewer = DataViewer(treeData.tree.get_node("r/technology").users.users)
    dataViewer.writeData("apenas_r_technology")
    
    return 
    
if __name__ == '__main__':
    main()