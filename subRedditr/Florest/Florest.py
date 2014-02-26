#-------------------------------------------------------------------------------
# Name:        Florest
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     10/01/2014
# Copyright:   (c) Pedro Gomes 2013
# Licence:     
#-------------------------------------------------------------------------------

class Florest:
    """Class for loading multiple types of database reddit users"""
    
    def __init__(self):
        """ Initiates a mother class for TreeData reddit Users """
        self.florest = {}
    
    def addTree(self,description):
        from TreeData import TreeData
        
        self.florest[description] = TreeData.TreeData(description)
        
        return self.florest[description]
    
    def get_Tree(self, description):
        return self.florest[description]
        
    

def main():
    pass


if __name__ == '__main__':
    main()
