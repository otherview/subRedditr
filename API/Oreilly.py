#-------------------------------------------------------------------------------
# Name:        O'reilly Recomendation
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     26-10-2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------


class Oreilly:
  
  def __init__(self):
    
    import RedditUsers as RedditUsers
    import RedditUser as RedditUser
    self.redditUsers = RedditUsers.RedditUsers()
    self.dataset = self.formatDataset()
    #redditUsers.saveDataset(dataset)
    

  def formatDataset(self):
    tmpDataset = {}
    
    for user in self.redditUsers.users:
      tmpDataset[user] = self.redditUsers.users[user].dataset
    
    return tmpDataset


# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson_old(prefs,p1,p2):
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

# Returns the Pearson correlation coefficient for p1 and p2 from the slides
def sim_pearson(prefs,p1,p2):
  from math import sqrt
  import numpy as np
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
  
  # Median of all preferences
  med1 = sum1/len([prefs[p1][it] for it in si])
  med2 = sum2/len([prefs[p2][it] for it in si])
  
  # Sum of the diference of item minus median times each other
  toSum1 = sum([prefs[p1][it]-med1 for it in si])
  toSum2 = sum([prefs[p2][it]-med2 for it in si])
  totalDenominator = toSum1*toSum2
 
  #End of denominator
  #Start of ? numerator ?
  # Sum of the products
  toSum1 = sum(np.array([pow(prefs[p1][it]-med1,2) for it in si]))
  toSum2 = sum(np.array([pow(prefs[p2][it]-med2,2) for it in si]))
  
  totalNumerator = sqrt(toSum1)*sqrt(toSum2)
  if totalNumerator == 0:
    return 0
  pearson = totalDenominator / totalNumerator
  
  return pearson


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

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

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]
  

def simpleRecomendation():
  import time,operator
  import Evaluation
  start_time = time.time()
  
  recomendationOreilly = Oreilly()
  
  user = 'dinojoe'
  testSubreddit = max(recomendationOreilly.dataset[user].iteritems(), key=operator.itemgetter(1))[0]
  
  
  print "For User: "+user+" Lets remove the most posted subreddit : "+testSubreddit
  recomendationOreilly.dataset[user].pop(testSubreddit)
  print "Recomendations: "
  print getRecommendations(recomendationOreilly.dataset,user)
  
  
  print "top Matches:"
  print topMatches(recomendationOreilly.dataset,user,n=5)
  print time.time() - start_time, "seconds"
  print "cenas"
  
def recomendationAndEvaluation(times):
  import Evaluation
  
  recomendationOreilly = Oreilly()
  evaluation = Evaluation.Evaluation()
  
  evaluation.removeRandomSubreddit(recomendationOreilly.dataset)
  
  
  for tmpUsr in evaluation.dataset:
    evaluation.addRecomendation(getRecommendations(evaluation.dataset,tmpUsr),tmpUsr)
    
  print "Round "+str(times)+" - Percentage of sucess: "+ str(evaluation.finalEvaluation())
  
  return
  
  
def recomendHowManyPosts(prefs,person,similarity=sim_pearson):
  totals={}
  simSums={}
  sumPerson = sum([prefs[person][it] for it in si])
  medPerson = sumPerson/len([prefs[person][it] for it in si])
  
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)
    # Average for the other
    sumOther = sum([prefs[other][it] for it in si])
    medOther = sumOther/len([prefs[other][it] for it in si])
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
  simpleRecomendation()
  
  #for times in range(0,9):
  #  recomendationAndEvaluation(times)
    
  return 

if __name__ == '__main__':
    main()