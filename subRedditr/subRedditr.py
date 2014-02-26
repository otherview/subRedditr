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
        from Florest import Florest 
        
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
    
    
    def evaluateRecomendRightSubReddit(self):
        import Evaluationr.Evaluationr as Evaluationr
        import Recommendationr.Recommendationr as Recommendationr
        
        self.recomendationr = Recommendationr.Recommendationr(self.redditUsers)
        self.evaluationr = Evaluationr.Evaluationr(self.redditUsers,self.recomendationr)
        
        print self.evaluationr.evaluateTopNSubredditRecomendations()
        
        
    def evaluateNumberOfPosts(self,user):
        import Evaluationr.Evaluationr as Evaluationr
        import Recommendationr.Recommendationr as Recommendationr
        
        self.recomendationr = Recommendationr.Recommendationr(self.redditUsers)
        self.evaluationr = Evaluationr.Evaluationr(self.redditUsers,self.recomendationr,)
        
        print self.evaluationr.evaluateNumberOfPosts(user)
        
        
    def create_Tree(self,description):
        return self.florest.addTree(description)
    
    
    
    def fetch_SubReddit(self,subReddit):
        subRedditUsers_Dataset = self.dataFetchr.fetchSubReddit(subReddit,depth=2)

        return subRedditUsers_Dataset
    
    def add_Users_To_Node(self,tree,subRedditName,users):
        
        tree.add_Users_To_Node(subRedditName,users)
        return
    
    def scrape_Tree_start_subReddit(self, TreeDescription, StartingSubReddit, StatusDepth, Depth = 5, ):
        
        def get_next_Subreddit(tmpTree,MaxSubRedditList,index=0):
            tmpMaxSubreddit = MaxSubRedditList[index]
        
            if tmpTree.tree.contains(tmpMaxSubreddit):
                CurrentIndex= index + 1
                return get_next_Subreddit(tmpTree,MaxSubRedditList,index=CurrentIndex)
            else:
                return tmpMaxSubreddit
        
        
        if StatusDepth == Depth:
            return
        else:
            treeDisc = TreeDescription
            tmpTree = self.florest.get_Tree(TreeDescription)
            statusDepth = StatusDepth +1
            newUsers = self.fetch_SubReddit(StartingSubReddit)
            new_Scrapped_Users = self.scrapeUsers(newUsers)
            tmpTree.add_node(str(StartingSubReddit))
            tmpTree.add_Users_To_Node(StartingSubReddit,new_Scrapped_Users)
            
            
            nextSubredditList = tmpTree.tree.get_node(StartingSubReddit).users.get_Most_Posted_Sub()
            self.scrape_Tree_width_subReddit(TreeDescription, str(StartingSubReddit),nextSubredditList )
            
            nextSubreddit = get_next_Subreddit(tmpTree, nextSubredditList)
            print "Subreddit mais postado -> "+str(nextSubreddit)
            self.scrape_Tree_start_subReddit( TreeDescription, nextSubreddit, statusDepth )
            
            
    def scrape_Tree_width_subReddit(self, TreeDescription, StartingSubReddit, SubRedditScrapeList ):    
            

        treeDisc = TreeDescription
        tmpTree = self.florest.get_Tree(TreeDescription)
        
        for subReddit_To_scrape in SubRedditScrapeList:
            if tmpTree.tree.contains(subReddit_To_scrape):
                pass
            else:
                print "SubReddit em Largura -> "+str(subReddit_To_scrape)
                newUsers = self.fetch_SubReddit(subReddit_To_scrape)
                new_Scrapped_Users = self.scrapeUsers(newUsers)
                tmpTree.add_node(str(subReddit_To_scrape), parent=str(StartingSubReddit))
                tmpTree.add_Users_To_Node(StartingSubReddit,new_Scrapped_Users)

        
        
        pass
    
    
    
def main():
    subRedditr = SubRedditr()
    #newUsers = subRedditr.fetchMoreUsers()
    #subRedditr.scrapeUsers(newUsers)
    #subRedditr.saveUsers()
    #subRedditr.getRecomendations('Popcom')   
    #subRedditr.evaluateRecomendRightSubReddit()
    #subRedditr.evaluateNumberOfPosts('Popcom')
    
    
    
    #Test Auto Scraper
    tree = subRedditr.create_Tree("Scraper Tree at r/Portugal")
    subRedditr.scrape_Tree_start_subReddit("Scraper Tree at r/Portugal","r/portugal",0)
    
    tree.save_To_File('R-Portugal-Tree.db')
    
    pass
    
    
    #Test Trees
    tree = subRedditr.create_Tree("1st Test Tree")
    
    tree.load_From_File('TestTree.db')
    
    allUsers = tree.get_users_from_subtree("r/Portugal")
    subRedditr.getRecomendations(u'turnusb',RedditUsers=allUsers)
    subRedditr.redditUsers = allUsers
    subRedditr.evaluateNumberOfPosts(u'turnusb')
    tree.add_node("r/Portugal")
    
    newUsers = subRedditr.fetch_SubReddit("r/Portugal")
    new_Scrapped_Users = subRedditr.scrapeUsers(newUsers)
    tree.add_Users_To_Node("r/Portugal",new_Scrapped_Users)
    
    
    tree.add_node("r/Brasil")
    newUsers = subRedditr.fetch_SubReddit("r/Brasil")
    new_Scrapped_Users = subRedditr.scrapeUsers(newUsers)
    tree.add_Users_To_Node("r/Brasil",new_Scrapped_Users)
    
    tree.add_node("r/Games",parent = "r/Portugal")
    newUsers = subRedditr.fetch_SubReddit("r/Games")
    new_Scrapped_Users = subRedditr.scrapeUsers(newUsers)
    tree.add_Users_To_Node("r/Games",new_Scrapped_Users)
    #
    #tree.add_node("r/IndieGaming", parent = "r/Brasil")
    #newUsers = subRedditr.fetch_SubReddit("r/IndieGaming")
    #new_Scrapped_Users = subRedditr.scrapeUsers(newUsers)
    #tree.add_Users_To_Node("r/IndieGaming",new_Scrapped_Users)
    print tree.tree.get_node("r/Portugal").users == tree.tree.get_node("r/Brasil").users
    
    tree.save_To_File('TestTree.db')
    
    
    import treelib
    for node in tree.tree.expand_tree(mode=treelib.Tree.ZIGZAG):
        print tree.tree[node].identifier
        print tree.tree[node].users
        print "------------------"
    tree.tree.show()
    return
    
if __name__ == '__main__':
    main()