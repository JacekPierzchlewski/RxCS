"""
This script is an example of how to use the Kernel Recursive Least Squares algorithms. |br|

In this example the algorithm approximates a noisy sinc function. |br|

*Author*:

This example is based on Matlab example in 'Kafbox' by Steven Van Vaerenbergh.

    2012 - 2014 Steven Van Vaerenbergh (Matlab version: http://sourceforge.net/projects/kafbox/)
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 4-DEC-2014 :  * Version 1.0 released. |br|
    1.1  | 17-DEC-2104 : * Changes in signals plotting. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs.auxiliary.krls as krls
import matplotlib.pyplot as plt

def _aldkrls_ex0():

    iN_training = 1e2  # Size of the training data
    iN_test = 1e3      # Size of the test data
    iSNR = 20          # Noise in the training data [SNR in dB]

    # Generate training data
    vX = np.random.randn(iN_training)
    vY = np.sinc(vX)
    vY = vY + np.sqrt(10**(-iSNR/10)*np.var(vY,ddof=1))*np.random.randn(iN_training)

    # Generate test data
    iStep = (np.max(vX) - np.min(vX))/iN_test
    vX_test = np.arange(np.min(vX),np.max(vX),iStep)
    vY_test = np.sinc(vX_test)

    # -----------------------------------------------------------------
    # Train the algorithm
    dAldKRLS = krls.aldkrls.init('gauss')      # Construct a 'aldKRLSL' object
    for i in np.arange(iN_training):           # Training loop (loop over the all training samples)
        dAldKRLS = krls.aldkrls.train(dAldKRLS , vX[i], vY[i])

    # Evaluate the algorithm
    vY_est = krls.aldkrls.evaluate(dAldKRLS, vX_test)

    # -----------------------------------------------------------------
    # Plot
    hFig1 = plt.figure(1)
    hSubPlot1 = hFig1.add_subplot(111)
    hSubPlot1.grid(True)
    hSubPlot1.plot(vX_test, vY_est,'-b',label='Generated by the algorithms')
    hSubPlot1.plot(vX_test, vY_test,'-g',label='Correct')
    vY = vY[np.argsort(vX)]; vX = np.sort(vX); hSubPlot1.plot(vX, vY,'-*r',label='Training')
    hSubPlot1.legend()
    plt.show(block=True)

# =====================================================================
# Trigger when start as a script
# =====================================================================
if __name__ == '__main__':
    _aldkrls_ex0()
