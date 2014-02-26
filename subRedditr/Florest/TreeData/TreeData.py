#-------------------------------------------------------------------------------
# Name:        TreeData
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     10/01/2014
# Copyright:   (c) Pedro Gomes 2014
# Licence:     
#-------------------------------------------------------------------------------


class TreeData:
    
    """Class for one type of database reddit users"""
    
    def __init__(self,description):
        import treelib
        
        self.tree = treelib.Tree()
        self.description = description
        self.currentNode = "root"
    
        return
    

    def add_node(self, subReddit, parent = None):
        
        if parent:
            if isinstance(parent,list):
                self.tree.create_node(subReddit,subReddit,parent.encode("utf-8")[0])
            else:
                self.tree.create_node(subReddit,subReddit,parent.encode("utf-8"))
            self.currentNode = subReddit
            return 
            
        if self.currentNode == "root":
            self.tree.create_node(subReddit,subReddit)
            self.currentNode = subReddit
            return
        
        
        if not self.tree.contains(subReddit):
            self.tree.create_node(subReddit,subReddit,self.currentNode)
            self.currentNode = subReddit
            return    
        
        subNode = self.tree.get_node(subReddit)
       

        return
    
    def add_Users_To_Node(self,subRedditName,scraped_Users):
        try:
            self.tree.get_node(subRedditName).users.addUsers( scraped_Users )
        except AttributeError:
           self.tree.get_node(subRedditName).users = scraped_Users
        return
        
        
    def get_users_from_subtree(self, tree ):
        import treelib
        import RedditUsers.RedditUsers as RedditUsers
        
        tmpRedditUsers = RedditUsers.RedditUsers()
        subtree = self.tree.subtree(tree)
        
        for node in subtree.expand_tree(mode=treelib.Tree.DEPTH):
            
            print str(node) +" users: - "+str(len(subtree.get_node(node).users.users))
            tmpUsers = subtree.get_node(node).users
            tmpRedditUsers.addUsers(tmpUsers)
            print "Current Users:" + str(len(tmpRedditUsers.users))
            
        return tmpRedditUsers
        
    
        
        
    def save_To_File(self, save_To_File):
        
        import treelib,json
        
        for node in self.tree.expand_tree(mode=treelib.Tree.DEPTH):
            line_Save_JSON = {}
            line_Save_JSON['id'] = self.tree[node].tag
            line_Save_JSON['bpointer'] = self.tree[node].bpointer
            line_Save_JSON['users'] = self.tree[node].users.toJSON()
            try:
                with open(save_To_File,'ab') as handle:
                    handle.write(json.dumps(line_Save_JSON)+'\n',)
                   
            except IOError as e:
                # you can print the error here, e.g.
                print(str(e))
            
    def load_From_File(self, load_from_File):
        
        import treelib,json
        import RedditUsers.RedditUsers as RedditUsers
        import RedditUsers.RedditUser.RedditUser as RedditUser
        
        try:
            with open(load_from_File,'r') as handle:
                for line in handle:
                
                    jsonLine = json.loads(line)
                    self.add_node(jsonLine['id'].encode("utf-8"), parent=jsonLine['bpointer'] )
                    self.tree.get_node(jsonLine['id']).users = RedditUsers.RedditUsers()
                    for user in jsonLine['users']:
                        redditUser = RedditUser.RedditUser(user)
                        redditUser.posts = json.loads(jsonLine['users'][user]['posts'])
                        redditUser.dataset = json.loads(jsonLine['users'][user]['dataset'])
                        redditUser.commentTrack = json.loads(jsonLine['users'][user]['commentTrack'])
                        self.tree.get_node(jsonLine['id']).users.users[user] = redditUser
                        
                    
            #    self.tree.get_node(jsonLine['id']).users.add
            #    self.users[lineUser['redditUser']] = RedditUsers.RedditUsers()$$$$%%%
                
                
                print "Load Tree Complete"
                   
        except IOError as e:
            # you can print the error here, e.g.
            print(str(e))
    
        
        pass
    
    
def main():
    
    treeData = TreeData("Cenas de teste")
    class SubORUser:
        def __init__(self,nome,data):
            self.name = nome
            self.data = data
            return
        def getName(self):
            return self.name
        
    sub = SubORUser("r/Portugal","{1:2}")
    usr1 = SubORUser("tipocenas","{1:3,1:4}")
    usr2 = SubORUser("coisas","{1:3,1:4,1:5,1:6}")
    sub2 = SubORUser("r/youtube","{z:alpha}")
    treeData.add_node(sub)
    treeData.add_node(usr1)
    treeData.add_node(usr2)
    treeData.add_node(sub2)
    
    pass

if __name__ == '__main__':
    main()