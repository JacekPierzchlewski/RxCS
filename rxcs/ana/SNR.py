"""
This module contains SNR evaluation function of the reconstructed signals. |br|


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    0.1  | 20-MAY-2014 : * Initial version. |br|
    0.2  | 21-MAY-2014 : * Success Ratio computation is added. |br|
    0.3  | 21-MAY-2014 : * Docstrings added. |br|
    0.4  | 21-MAY-2014 : * Configuration with a dictionary |br|
    0.5  | 21-MAY-2014 : * Progress and results printing |br|
    1.0  | 21-MAY-2014 : * Version 1.0 released. |br|
    2,0  | 21-AUG-2015 : * Version 2,0 (objectified version) is released. |br|

*License*:
    BSD 2-Clause
"""
from __future__ import division
import numpy as np
import rxcs


class SNR(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Analysis'  # Name of group of RxCS modules
        self.strModuleName = 'SNR'      # Module name

        self.__inputSignals()      # Define the input signals
        self.__parametersDefine()  # Define the parameters

    # Define parameters
    def __inputSignals(self):

        # Signal under test
        self.paramAddMan('mSig', 'Signal under test', noprint=1)
        self.paramType('mSig', np.ndarray)         # Must be a Numpy array
        self.paramTypeEl('mSig', (int, float))     # Elements must be of float or int type
        self.paramNDimLE('mSig', 2)                # Must be a 1, or 2 dimensional matrix

        # Reference signal
        self.paramAddMan('mSigRef', 'Reference signal', noprint=1)
        self.paramType('mSigRef', np.ndarray)         # Must be a Numpy array
        self.paramTypeEl('mSigRef', (int, float))     # Elements must be of float or int type
        self.paramNDimLE('mSigRef', 2)                # Must be a 1, or 2 dimensional matrix
        self.paramDimEq('mSigRef', 'mSig', 'rows', 'rows')         # Must have shape equal to mSig
        self.paramDimEq('mSigRef', 'mSig', 'columns', 'columns')   # ^


    # Define parameters
    def __parametersDefine(self):

        # Success threshold
        self.paramAddOpt('iSNRSuccess', 'Success threshold')
        self.paramType('iSNRSuccess', (int, float))   # Must be a Numpy array
        self.paramH('iSNRSuccess', -np.inf)
        self.paramL('iSNRSuccess', np.inf)

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0

    # Run
    def run(self):
        self.parametersCheck()    # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters

        self.engineStartsInfo()  # Info that the engine starts
        self.__engine()          # Run the engine
        self.engineStopsInfo()   # Info that the engine ends
        return self.__dict__     # Return dictionary with the parameters

    # Engine - compute the noise and the success rate
    def __engine(self):

        # Make the 2D matrces with signals under test and observed signals
        self.mSig = self.makeArray2Dim(self.mSig)
        self.mSigRef = self.makeArray2Dim(self.mSigRef)

        # Get the number of signals and the size of signals
        (nSigs, iSizSig) = self.mSig.shape  # Size of the noise

        # Compute the noise
        mNoise = np.abs(self.mSig - self.mSigRef)
        (_, iSizNoise) = mNoise.shape  # Size of the noise

        # Compute the power of noise
        vNoiseP = (np.sum(mNoise**2, axis=1) / iSizSig)

        # Compute the power of reference signals
        vSigP = (np.sum(self.mSigRef**2, axis=1) / iSizSig)

        # Compute the SNR for every reconstructed signal and the average SNR
        self.vSNR = 10 * np.log10(vSigP / vNoiseP)
        self.iSNR = self.vSNR.mean()

        # Compute the success for every reconstructed signal and the success ratio
        if self.wasParamGiven('iSNRSuccess'):
            self.vSuccessBits = (self.vSNR >= self.iSNRSuccess)
            self.iSR = self.vSuccessBits.mean()

        # -------------------------------------------------------------------
        # Print results
        if self.bMute == 0:
            self._printResults(self.iSNR, self.iSR, self.iSNRSuccess)

        return

    # Print the results of analysis
    def _printResults(self, iSNR, iSR, iSNRSuccess):
        rxcs.console.bullet_param('The average SNR of the reconstruction',
                                  iSNR, '-', 'dB')
        rxcs.console.bullet_param('The Success Ratio', iSR, ' ', '')
        rxcs.console.param('(success threshold)', iSNRSuccess, '-', 'dB')
        return
