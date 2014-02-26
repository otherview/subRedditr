#-------------------------------------------------------------------------------
# Name:        Pearson
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     26/11/2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     
#-------------------------------------------------------------------------------

class Pearson:
    """ Returns the Pearson correlation coefficient for p1 and p2 """
    def __init__(self):
        return
    
    
    def calculateSimSciPy(self,prefs,p1,p2):
        import scipy.stats as sim
        
         # Get the list of mutually rated items
        simDatasetP1=[]
        simDatasetP2=[]
        for item in prefs[p1]: 
          if item in prefs[p2]:
            simDatasetP1.append(prefs[p1][item])
            simDatasetP2.append(prefs[p2][item])
      
        # if they are no ratings in common, return 0
        if len(simDatasetP1)==0: return 0
        
        #prepare similarity arrays
        
        
        #print sim.pearsonr(simDatasetP1,simDatasetP2)
        
        return sim.pearsonr(simDatasetP1,simDatasetP2)[0] 
        
        
        
    def calculateSim(self,prefs,p1,p2):
    
        from math import sqrt
        # Get the list of mutually rated items
        si={}
        for item in prefs[p1]: 
          if item in prefs[p2]: si[item]=1
      
        # if they are no ratings in common, return 0
        if len(si)==0: return 0
      
        # Sum calculations
        n=len(si)
        
        # Sums of all the preferences
        sum1=sum([prefs[p1][it] for it in si])
        sum2=sum([prefs[p2][it] for it in si])
        
        # Sums of the squares
        sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
        sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	
        
        # Sum of the products
        pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
        
        # Calculate r (Pearson score)
        num=pSum-(sum1*sum2/n)
       # den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n)) # Isto esta a dar um NEGATIVO e nao devia
        den=sqrt(abs((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n)))
        if den==0: return 0
      
        r=num/den
      
        return r
        


  
    
    
    

