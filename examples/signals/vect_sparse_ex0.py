"""
This script is an example of how to use the random sparse vector 
generator module. |br|

In this example 5 random sparse vectors are generated. |br|


After the generation, the generated sparse vectors are plotted. |br|

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 22-MAY-2014 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""
from __future__ import division
import rxcs
import numpy as np
import matplotlib.pyplot as plt


def _vect_sparse_ex0():

    # SETTINGS:
    iN = 20        # Size of the vectors
    iS = 0.2       # Sparsity parameter (0.2 * 20 = 4 non-zero elements)
    iNVects = 5    # The number of vectors

    # -----------------------------------------------------------------
    # Generate settings for the generator

    # Start the dictionary with configuration for sparse vectors generator
    dSigConf = {}
    dSigConf['iVectSiz'] = iN       # Size of the vectors
    dSigConf['iS'] = iS             # Sparsity parameter
    dSigConf['iNVect'] = iNVects    # The number of vectors
    dSigConf['bMute'] = 0           # Be verbose

    # Run the sparse vectors generator
    mVecs = rxcs.sig.sparseVector.main(dSigConf)

    # -----------------------------------------------------------------
    # Plot the sparse vectors
    hFig1 = plt.figure(1)

    hSubPlot1 = hFig1.add_subplot(511)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Vector #1')
    hSubPlot1.stem(np.arange(iN), mVecs[:,0], linefmt='b-', markerfmt='bo', basefmt='r-')
    hSubPlot1.set_xlim(-1, iN+1)
    hSubPlot1.set_ylim(-0.1, 1.1)

    hSubPlot1 = hFig1.add_subplot(512)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Vector #2')
    hSubPlot1.stem(np.arange(iN), mVecs[:,1], linefmt='b-', markerfmt='bo', basefmt='r-')
    hSubPlot1.set_xlim(-1, iN+1)
    hSubPlot1.set_ylim(-0.1, 1.1)

    hSubPlot1 = hFig1.add_subplot(513)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Vector #3')
    hSubPlot1.stem(np.arange(iN), mVecs[:,2], linefmt='b-', markerfmt='bo', basefmt='r-')
    hSubPlot1.set_xlim(-1, iN+1)
    hSubPlot1.set_ylim(-0.1, 1.1)

    hSubPlot1 = hFig1.add_subplot(514)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Vector #4')
    hSubPlot1.stem(np.arange(iN), mVecs[:,3], linefmt='b-', markerfmt='bo', basefmt='r-')
    hSubPlot1.set_xlim(-1, iN+1)
    hSubPlot1.set_ylim(-0.1, 1.1)

    hSubPlot1 = hFig1.add_subplot(515)
    hSubPlot1.grid(True)
    hSubPlot1.set_title('Vector #5')
    hSubPlot1.stem(np.arange(iN), mVecs[:,4], linefmt='b-', markerfmt='bo', basefmt='r-')
    hSubPlot1.set_xlim(-1, iN+1)
    hSubPlot1.set_ylim(-0.1, 1.1)


    # -----------------------------------------------------------------
    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _vect_sparse_ex0()
