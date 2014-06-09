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
    
    # align the total number of circles by extending the smaller list with empty circles
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