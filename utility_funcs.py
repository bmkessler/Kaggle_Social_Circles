# -*- coding: utf-8 -*-
"""
Created on Wed May 21 07:43:03 2014

@author: bmkessle
"""

import networkx as nx

def read_nodeadjlist(filename):
  G = nx.Graph()
  for line in open(filename):
    e1, es = line.split(':')
    G.add_node(int(e1))
    es = es.split()
    for e in es:
      if e == e1: continue
      G.add_edge(int(e1),int(e))
  return G

def readfeaturelist(filename):
    """
    reads a featurelist file and returns a list of the feature names
    """
    with open(filename) as f:
        out = []        # list of feature names
        for line in f:
            out.append(line.strip())
        return out
        
def readfeatures(featurefile):
    """
    reads a featurefile consisting of userid feature;value feature;value
    returns a list where index is user id, elements are dictionaries 
    of features as keys pointing to list of values maybe should be sets
    """
    with open(featurefile) as f:
        out = [] 
        for line in f:
            tokens = line.split()
            profile = {}  # empty profile for the user
            for tok in tokens[1:]:
                feature,val = tok.rsplit(';',1)
                val = int(val)
                if feature not in profile:
                    profile[feature]=[val]
                else:
                    profile[feature].append(val)
            out.append(profile)
        for i in range(len(out)):
            assert out[i]['id'][0] == i  # check that each line was read and placed in the correct place in the list
        return out
        
def featurematch(profile1,profile2,feature):
    """
    returns how well profile1 and profile2 match on a given of feature
    currently returns the number of items they have in common for that given feature
    """
    return len(set(profile1[feature]).intersection(set(profile2[feature]))) if feature in profile1 and feature in profile2 else 0

def matchvector(profile1,profile2,featurelist):
    """
    given two profiles and a featurelist, returns the similarity vector for the two
    profiles where each entry is the number of entries they have in common for that feature,
    i.e. returns 2 if they went to the same two school ids
    """
    out = []
    for feature in featurelist:
        out.append(featurematch(profile1,profile2,feature))
    return out

def weighteddotproduct(vector1,vector2,weight=None):
    """
    returns the dot product of vector1 and vector2 with weight vector weight (normalized)
    """
    if not weight:
        weight = ones(len(vector1))
    return np.inner(vector1,np.multiply(weight,vector2))/mean(weight)
    
def userfeatures(profile):
    """  Returns a list of the features contained in the user profile """
    return [f for f in profile]
	
def usermatch(profile1,profile2):
    """ returns the match vector for profile2 using only profile1 features as a reference """
    return matchvector(profile1,profile2,userfeatures(profile1))
	
def readcirclefile(circlefile):
    """
    reads a circle for a given user consisting of circleDD: user1 user2 user3 ...
    and returns a dictionary of the circle['number']=[user1,user2,user3]
    """
    with open(circlefile) as f:
        circles = {} 
        for line in f:
            tokens = line.split()
            circleID = int(tokens[0].split('circle')[1].split(':')[0])
            circles[circleID] =[]
            for tok in tokens[1:]:
              if int(tok) not in circles[circleID]:
                circles[circleID].append(int(tok))
        return circles

from munkres import Munkres

def cost_function(pred_circles,true_circles):
    """
    An efficient implementation of the cost function between predicted circles and ground truth circles
    
    Parameters
    ----------
    pred_circles: a dictionary
      keys are circle labels (unused for calculation) and values are lists of users (any object) in the circle
    
    true_circles: a dictionary
      keys are circle labels (unused for calculation) and values are lists of users (any object) in the circle
      
    Returns
    -------
    min_diff: int
      the error achieved for optimal assignment of the circles between the predicted and true inputs
    
    Notes
    -----
    This function works by computing the symmetric difference (sum of type I and type II errors) between each 
    circle in the predicted and true list and then minimizing the assignment error between the lists using the
    Hungarian algorithm via the munkres module: 
    
    http://software.clapper.org/munkres/ 
    http://github.com/bmc/munkres.git
    
    For further background on the assignment problem see: 
    http://en.wikipedia.org/wiki/Assignment_problem
    http://en.wikipedia.org/wiki/Hungarian_algorithm      
    """
    # convert the circle dictionaries into a list of sets
    pred_circle_list,true_circle_list = [set(c) for c in pred_circles.values()],[set(c) for c in true_circles.values()]
    
    # align the total number of circles by extending the smaller list of circles with empty circles
    for i in range(len(pred_circle_list)-len(true_circle_list)):
        true_circle_list.append(set([]))
    for j in range(len(true_circle_list)-len(pred_circle_list)):
        pred_circle_list.append(set([]))
        
    # calculate the size of the symmetric difference of each predicted circle and each true circle 
    diff_matrix = [[len(c1.symmetric_difference(c2)) for c2 in true_circle_list] for c1 in pred_circle_list]
    
    # compute the optimal assignment of circles between predicted and true
    munk = Munkres()  # the Hungarian Algorithm module
    index = munk.compute(diff_matrix)  # compute the indices for the optimal alignment
    min_diff = sum( [ diff_matrix[row][col] for row,col in index] )  # compute the total error on the optimal alignment
    return min_diff