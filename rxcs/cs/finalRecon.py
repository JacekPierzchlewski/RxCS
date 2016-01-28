"""
*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 20-JAN-2016 : * Version 1.0 released |br|
    1.0r1  | 28-JAN-2016 : * Only real part of reconstructed signals is preserved

*License*:
    BSD 2-Clause
"""

from __future__ import division
import rxcs
import numpy as np


# =================================================================
# L1 solver object
# =================================================================
class finalRecon(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        # Name of group of RxCS modules and module name
        self.strRxCSgroup = 'Reconstruction'  
        self.strModuleName = 'Final reconstruction'

        self.__inputSignals()      # Define the input signals
        self.__parametersDefine()  # Define the parameters
        
        # Start L2 solver object
        self.L2solv = rxcs.auxiliary.aldkrlsL2()


    # Define parameters
    def __inputSignals(self):

        # Reconstructed signals coefficients
        self.paramAddMan('lCoeff', 'Reconstructed signals coefficients', noprint=1)
        self.paramType('lCoeff', list)             # Must be a list
        self.paramTypeEl('lCoeff', (np.ndarray))   # Elements must be np.ndarray

        # Signals dictionary
        self.paramAddMan('mDict', 'Dictionary matrix [time domain in 2nd dimension (columns) ]')  
        self.paramType('mDict', np.ndarray)             # Must be a Numpy array
        self.paramNDimEq('mDict', 2)                    # Must bo 2-dimensional

    def __parametersDefine(self):

        self.paramAddOpt('vInx', 'Indices of rows of the dictionary to be used in the reconstruction', noprint=1)
        self.paramType('vInx', np.ndarray)             # Must be a Numpy array
        self.paramTypeEl('vInx', (int))                # Elements must be integers
        self.paramNDimEq('vInx', 1)                    # Must bo 2-dimensional
        self.paramUnique('vInx')                       # Elements must be unique
        self.paramHE('vInx', 0)                        # Elements must be higher than 0 

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute', [0, 1])     # It can be either 1 or 0

    # Run
    def run(self):
        self.parametersCheck()    # Check if all the needed partameters are in place and are correct
        self.parametersPrint()    # Print the values of parameters
        
        self.checktInputSig()     # Check if the observed signals and Theta 
                                  # matrices are correct

        self.engineStartsInfo()  # Info that the engine starts
        self.__engine()          # Run the engine
        self.engineStopsInfo()   # Info that the engine ends
        return self.__dict__     # Return dictionary with the parameters

    # Check if the observed signals and Theta matrices are correct
    def checktInputSig(self):

        # All the elements in the vector with indices of rows of the dictionary to be used in the reconstruction
        # ('vInx') must be lower than the number of rows in the dictionary matrix
        (nRowsDict, _) = self.mDict.shape

        if self.wasParamGiven('vInx'):
            for inxRow in self.vInx:
                if inxRow >= nRowsDict:
                    strError = 'Indices of dictionary rows must be lower than the number of rows in the dictionary!'
                    raise ValueError(strError)      
        return


    # Engine - reconstruct the signal coefficients
    def __engine(self):
    
        # Get the number of the signal coefficients
        nSigCoeff = len(self.lCoeff)

        # Get the number of columns (time samples) in the dictionary
        (_, nT) = self.mDict.shape

        # Reconstruct the signals
        self.lSig = []                          # List with the reconstructed signals
        self.mSig = np.zeros((nSigCoeff, nT))   # Matrix with the reconstructed signals

        # Loop over all the signal coefficients
        if self.wasParamGiven('vInx'):
            # Take only a part of the dictionary which should be used to reconstruct the signal
            self.mDict_ = self.mDict[self.vInx, :]
            for inxSig in np.arange(nSigCoeff):
                vCoeff = self.lCoeff[inxSig][self.vInx]  # 
                vSig = vCoeff.dot(self.mDict_)           # Generate a signal
                self.lSig.append(vSig)                   # Add the signal to the lst
                self.mSig[inxSig, :] = vSig.real         # Add the signal to the matrix with signals

        else:
            for inxSig in np.arange(nSigCoeff):        
                vSig = self.lCoeff[inxSig].dot(self.mDict)   # Generate a signal
                self.lSig.append(vSig)
                self.mSig[inxSig, :] = vSig.real             # Add the signal to the matrix with signals

        return





