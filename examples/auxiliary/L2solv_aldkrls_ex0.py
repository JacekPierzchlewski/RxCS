"""
This script is an example of how to use the L2 solver (krls). |br|

In this example, and L2 solver searches for a vector X \in R^(iN x 1),
which solves the problem:

       min|| Y - AX  ||_2

where Y is \in R^(iM x 1) and A is \in R^(iM x iN)
  

*Author*:

    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 4-DEC-2014 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs
import matplotlib.pyplot as plt


def _L2solv_aldkrls_ex0():

    # Dimensions of the system
    iM = 20   
    iN = 11

    # Construct the data
    mA = np.random.randint(-10, 10, (iM, iN))
    vX = np.random.randint(-10,10,(iN, 1))
    vY = mA.dot(vX)

    # Solve the L2 problem
    vX_solv = rxcs.auxiliary.L2solv_aldkrls.main(mA, vY)             # Find the vector X using KRLS with linear kernel
    vX_solv.shape = (iN, )

    # Plot
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.plot(np.arange(iN), vX_solv,'-g',label='Found X vector')
    (markerline, stemlines, baseline) = hSubPlot1.stem(np.arange(iN), vX,
                                                       linefmt='b-',
                                                       markerfmt='bo',
                                                       basefmt='b-',
                                                       label='Original vector')
    hSubPlot1.legend()
    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _L2solv_aldkrls_ex0()
