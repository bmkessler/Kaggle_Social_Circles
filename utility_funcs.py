# -*- coding: utf-8 -*-
"""
Created on Wed May 21 07:43:03 2014

@author: bmkessle
"""

def readfeaturelist(filename):
    """
    reads a featurelist file and returns a list of the feature names
    """
    with open(filename) as f:
        out = []        
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
        out = []        # list where index is user id, elements are dictionaries of features as keys pointing to list of values 
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
    profiles where each entry is the number of entries they have in common for that feature
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