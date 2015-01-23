"""
This script is an example of how to use the L1 function from irls.py module. 
|br|

In this example an underdetermined system Ax=y is created. 

A is a matrix with iM rows and iN columns. There are more 
columns in the matrix than rows (iN > iM). The vector x is sparse.
In this example an IRLS algorithm looks for a correct vector x solving
the problem:

    min |x|_1   subj. to |Ax-y|_2 = 0
   

*Author*:

    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 23-JAN-2015 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""
import numpy as np
import rxcs
import matplotlib.pyplot as plt


def _IRLS_ex0():
    
    # Parameters   
    iM = 10     # The number of elements in the output vector y
    iN = 20     # The number of elements in the searched vector x
    iS = 2      # The number of non-zero elements in the searched vector x
   
    iMaxIter = 100    # The maximum number of iterations
    iConv = 0.001     # Convergence parameter
    
    # Generate the system
    mA = np.random.randint(-10, 10, (iM, iN))   # Generate the matrix A    
    vX = rxcs.sig.sparseVector.generate(iN,iS)  # Generate the sparse vector x    
    vY = mA.dot(vX)                             # Compute the vector y
    
    # Find the correct vector x - run the IRLS algorithm
    ( vXr, _, iIt ) = rxcs.auxiliary.irls.L1(mA, vY, iMaxIter, iConv)   

    vYr = mA.dot(vXr)   # Compute the reconstruxted vector y

    vYerr = vYr  - vY                 # Compute y error vector 
    vXd = vXr - vX                    # Compute x error vector
    iErrY = np.linalg.norm(vYerr, 2)   # Compute error in the found y vector
    iErrX = np.linalg.norm(vXd, 2)    # Compute error in the found x vector

    print('Error in the found x vector: %.3f, error in the found y vector: %.3f, solved after %d iterations \n') \
        % (iErrX, iErrY, iIt)

    #  -------------------------------------------------------------------------    
    #  Plotting:
    hFig1 = plt.figure(1)

    hSubPlot1 = hFig1.add_subplot(211)
    hSubPlot1.plot(vY, 'g-', label="original vector Y")
    hSubPlot1.plot(vYr, 'b*', label="reconstructed vector Y")
    hSubPlot1.grid(True)
    hSubPlot1.legend(loc="best")

    hSubPlot1 = hFig1.add_subplot(212)
    hSubPlot1.plot(vX, 'r-', label="original vector X")    
    hSubPlot1.plot(vXr, 'b*', label="reconstructed vector X")
    hSubPlot1.grid(True)
    hSubPlot1.legend(loc="best")

    plt.show(block=True)


# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _IRLS_ex0()
