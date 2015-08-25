"""
 This module generates Theta matrices from dictionary matrices and 
 observation matrices. |br|

 The input to the generator consists of two lists with dictionaries and observation 
 matrices (**lDict** and **lPhi**). The output Theta matrices are constructed 
 by multpiplication of a dictionary from the list **lDict** with corresponding 
 observation matrix from the list **lPhi**.

 Both the lists should have the same length. However, tt is allowed, that
 the lists contain only one element. In this case the singular dictionary
 matrix or the singular observation matrix will be used for constructing all 
 the Theta  matrices. 

*Examples*:
    Please go to the *examples/reconstruction* directory for examples 
    on how to use the Theta matrix generator. |br|

*Settings*:
    Parameters of the Theta generator are described below.

    Take a look on '__parametersDefine' function for more info on the 
    parameters.

    Parameters of the Theta generator are attributes of the class which 
    must/can be set before the generator is run.

    Required parameters:

    - a. **lDict** (*list with 2D Numpy arrays*): list with dictionaries

    - b. **lPhi** (*list with 2D Numpy arrays*): list with observation matrices

    Optional parameters:

    - c. **bMute** (*int*):    mute the console output from the sampler [default = 0]

*Output*:
    Description of the Theta matrix generator output is below.
    This is the list of attributes of the generator class which are available
    after calling the 'run' method:

    - a. **lTheta** (*list with 1D Numpy arrays*):  list with the generated 
                                                    Theta matrices

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1,0    | 25-AUG-2015 : * Version 1.0 released |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import rxcs
import numpy as np


# =================================================================
# L1 solver object
# =================================================================
class makeTheta(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        # Name of group of RxCS modules and module name
        self.strRxCSgroup = 'Reconstruction'  
        self.strModuleName = 'Theta matrices generator'

        self.__parametersDefine()  # Define the parameters

    # Define parameters
    def __parametersDefine(self):

        # Dictionaries:
        self.paramAddMan('lDict', 'dictionary matrix', noprint=1)
        self.paramType('lDict', list)          # Must be a list
        self.paramTypeEl('lDict', np.ndarray)  # with Numpy arrays
        self.paramSizH('lDict', 0)             # The list can not be empty

        # Observation matrices:
        self.paramAddMan('lPhi', 'observation matrix', noprint=1)
        self.paramType('lPhi', list)          # Must a list
        self.paramTypeEl('lPhi' ,np.ndarray)  # with Numpy arrays
        self.paramSizH('lPhi', 0)             # The list can not be empty

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute', [0, 1])     # It can be either 1 or 0


    # Run
    def run(self):
        self.parametersCheck()        # Check if all the needed partameters are in place and are correct
        self.parametersPrint()        # Print the values of parameters
        
        self.engineStartsInfo()  # Info that the engine starts
        self.__engine()          # Run the engine
        self.engineStopsInfo()   # Info that the engine ends
        return self.__dict__     # Return dictionary with the parameters


    # Engine
    def __engine(self):

        # Check if dictionaries and observation matrices were given as long
        # lists of short lists
        (nDict, nPhi) = self._processDictPhi(self.lDict, self.lPhi)

        # Equal the number of elements in lists
        if nPhi == 1:
            self.lPhi = self.lPhi * nDict
        if nDict == 1:
            self.lDict = self.lDict * nPhi

        # Check if all the dictionaries and observation matrices have correct dimensions
        self.checkDictPhiDim(self.lDict, self.lPhi, nDict, nPhi)

        # Loop over all the observation matrices
        self.lTheta = []
        for inxPhi in np.arange(nPhi):
            mPhi = self.lPhi[inxPhi]
            mDict = self.lDict[inxPhi]
            mTheta = np.dot(mPhi, mDict)
            self.lTheta.append(mTheta)

    # Count and check the number of dictionaries and observation matrices
    def _processDictPhi(self, lDict, lPhi):
        """
        This function counts the number of observation matrices and 
        dictionaries. Additionally, it checks if the number of given 
        dictionaries and observation matrices is correct.
        
        Args:
            lDict (list):   list with dictionaries       
            lPhi (list):    list with observation matrices     

        Returns:
            nDict (int):    the number of dictionaries        
            nPhi  (int):    the number of observation matrices
        """
        
        # Count the number of given dictionaries and observation matrices
        nDict = len(lDict)            
        nPhi = len(lPhi)

        # Check the sizes of lists
        if (nDict > 1) and (nPhi > 1):
            if not (nPhi == nDict):
                strE = 'Lists with dictionaries and observation matrices must have equal size!'
                raise ValueError(strE)

        return (nDict, nPhi)


    def checkDictPhiDim(self, lDict, lPhi, nDict, nPhi):
        """
        This function checks if the dimensions of the observation matrices and
        dictionaries is correct.

        Args:
            lDict (list):   list with dictionaries       
            lPhi (list):    list with observation matrices     
            nDict (int):    the number of dictionaries        
            nPhi  (int):    the number of observation matrices

        Returns:
            nothing
        """

        # Check if all the dictionaries and observation matrices have correct
        # number of dimensions
        for inxPhi in np.arange(len(lPhi)):
            mPhi = lPhi[inxPhi]              # Take the observation matrix
            mDict = lDict[inxPhi]            # Take the dictionary matrix
            
            # The number of dimensions
            if not (mPhi.ndim == 2):
                strE = 'Observation matrix #%d is not a 2-dimensional Numpy array!' % inxPhi
                raise ValueError(strE)
 
            if not (mDict.ndim == 2):
                strE = 'Dictionary #%d is not a 2-dimensional Numpy array!' % inxPhi
                raise ValueError(strE)
                                       
            # Column in observation == rows in dictionary
            (_, nCols) = mPhi.shape    # Get the number of columns in the observation matrix
            (nRows, _) = mDict.shape   # Get the number of rows in the dictionary matrix
            if not (nRows == nCols):
                self.PhiDictDimensionError(inxPhi, nDict, nPhi)


    def PhiDictDimensionError(self, inxA, nDict, nPhi):
        """
        This function prints out an error about incorrect dimensions of 
        the dictionaries and observation matrices.

        Args:
            inxA (int):     index of an obsevation matrix/dictionary     
            nDict (int):    the number of dictionaries        
            nPhi  (int):    the number of observation matrices

        Returns:
            nothing
        """

        if (nDict > 1) and (nPhi > 1):
            strE = 'Dictionary matrix #%d does not have the number of rows equal ' % inxA 
            strE = strE + 'to the number of columns in the corresponding observation matrix!'
        
        elif (nDict > 1) and (nPhi == 0):
            strE = 'Dictionary matrix #%d does not have the number of rows equal ' % inxA 
            strE = strE + 'to the number of columns in the given observation matrix!'

        elif (nDict == 0) and (nPhi > 1):
            strE = 'Observation matrix #%d does not have the number of columns equal ' % inxA 
            strE = strE + 'to the number of rows in the given dictionary matrix!'

        elif (nDict == 0) and (nPhi == 0):
            strE = 'The given observation matrix does not have the numbe r of columns equal ' 
            strE = strE + 'to the number of rows in the given dictionary matrix!'
        raise ValueError(strE)
