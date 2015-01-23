"""
This module contains function which implement Iterative Reweighted 
Least Squares Algorithm.
 
Go to examples/auxiliary for examples of using the module. 
 
*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>
    
    Function 'L1' is a Pythonized and modified Matlab example by:
    C. Sidney Burrus, Rice University, US-TX, csb@rice.edu   
   
    You can find this Matlab example under the follwoing link:
    http://cnx.org/contents/92b90377-2b34-49e4-b26f-7fe572db78a1@12/Iterative_Reweighted_Least_Squ
    
*Version*:
    1.0    | 23-JAN-2015 : * Initial version. |br|

*License*:
    Creative Commons Attribution 4.0 License
    WARNING: Ths module has a different license (CC Attribution 4.0) than
              most of the RxCS code (BSD 2-clause)!
"""


from __future__ import division
import numpy as np
import rxcs


def L1(mA, vY, iMaxIter, iConvStop):
    """
     This function looks for an optimum solution Ax = y, minimizing the 
     L_1 norm ||x||_1, using Iterative Reweighted Least Squares algortihm.     
     
     It used an L2 minimizer implemented using Kernel Recursive Least Squares
     algorithm with linear kernel. 
    
     An example irls_ex0.py in examples/auxiliary shows how to use this function.
    
    Args:
        mA  (numpy array):    matrix A   (look desc. above)
        vY  (numpy array):    vector y   (look desc. above)        
        iMaxIter (number):    the max number of iterations
        iConvStop (number):   convergence parameter

    Returns:
        vX  (numpy array):    found vector x (look desc. above)
        mX   (numpy array)    matrix with vectors x found in every iteration
        iIter (number):       the number of iterations 
        
    """    
    
    (nRows, nCols) = mA.shape             # Take the number of rows and columns in Theta    
    mX = np.zeros((nCols, iMaxIter+1))    # Allocate a matrix for storing the found vectors from every iteration    
        
    # Compute the initial solution and store it in mX
    vX = rxcs.auxiliary.L2solv_aldkrls.main(mA, vY)   # Find the initial vector X
    mX[:, 0] = vX
      
    # Loop over all iterations      
    for iIter in np.arange(iMaxIter):

        mAWeightedX = np.ones(mA.shape)      # Allocate new matrix with weights
        for inxRow in np.arange(nRows):      # Compute the matrix with weights      
            mAWeightedX[inxRow, :] = np.abs(vX) * mA[inxRow, :]

        vX_prev = vX.copy() # Store the previous solution
    
        # Compute the current x vector
        vX_temp = rxcs.auxiliary.L2solv_aldkrls.main(np.dot(mAWeightedX, mA.T), vY)
        vX = np.dot(mAWeightedX.T, vX_temp.T).T
        
        # Stopre the found x vector in the 'mX' matrix
        vX_1dim = vX.copy(); vX_1dim.shape = (nCols,)
        mX[:, iIter+1] = vX_1dim

        # Check convergence condition
        vXd = vX - vX_prev              # Compute the difference vector 
        iXd_n2 = np.linalg.norm(vXd)    # Second norm of the difference vector
        iX_n2 = np.linalg.norm(vX)      # Second norm of the current x vector
        if (iXd_n2 / iX_n2 ) < iConvStop:  # Should we stop?
            break
 
    return (vX.T, mX, iIter)
