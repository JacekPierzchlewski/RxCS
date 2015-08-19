"""
This a sparse vectors generator module. |br|

It is able to generate *N* random sparse vectors according to settings
given by a user. |br|

*Examples*:
    Please go to the *examples/signals* directory for examples on how to use 
    the generator. |br|

*Settings*:
    Parameters of the generator described below.

    Take a look on '__parametersDefine' function for more info on the 
    parameters.

    Parameters of the generator are attributes of the class which must/can
    be set before the generator run.

    Required parameters:

    - a. **iVectSiz** (*int*):  size of a single vector

    - b. **iS** (*float*):      sparsity of a single vector (0 <= iS <= 1)

    - c. **iNVect** (*int):     the number of vectors to be generated


    Optional parameters:

     - d. **bMute** (*int*):  mute the console output from the generator [default = 0]


*Output*:
    Description of the generator output is below. 
    This is the list of attributes of the generator class which are available 
    after calling the 'run' method:

    - a. **mVects** (*Numpy array 2D*):   Numpy array with the generated vectors


*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 22-JAN-2014 : * Version 1.0 released. |br|
    2.0    | 15-JUL-2015 : * Version 2.0 released. |br|
    2.0r1  | 18-AUG-2015 : * Adjusted to RxCSobject v1.0 |br|

*License*:
    BSD 2-Clause

"""


from __future__ import division
import numpy as np
import rxcs

class sparseVector(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object

        self.strRxCSgroup = 'Signal generator'           # Name of group of RxCS modules
        self.strModuleName = 'Sparse vectors generator'  # Module name

        self.__parametersDefine()      # Define the parameters

    def __parametersDefine(self):
        """
        Internal method which defines the parameters    
        """

        # Size of the vectors
        self.paramAddMan('iVectSiz', 'Size of the vectors', unit='')
        self.paramType('iVectSiz', (int))
        self.paramH('iVectSiz', 0)                  # Size of the vectors must be higher than zero
        self.paramL('iVectSiz', np.inf)             # ...and lower than infinity

        # The sparsity parameter
        self.paramAddMan('iS', 'Sparsity parameter', unit='', unitprefix=' ')
        self.paramType('iS', (int, float))
        self.paramHE('iS', 0)          # The sparsity parameter must be higher or equal to zero
        self.paramLE('iS', 1)          # ...and lower or equal to one

        # The number of vectors to be generated
        self.paramAddMan('iNVect', 'The number of vectors to be generated', unit='')
        self.paramType('iNVect', (int))
        self.paramH('iNVect', 0)           # The number of vectors to be generated must be higher than zero
        self.paramL('iNVect', np.inf)      # ...and lower than infinity

        # Mute the output flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)
        self.paramType('bMute', int)          # Must be of int type
        self.paramAllowed('bMute',[0, 1])     # It can be either 1 or 0


    def run(self):
        """
        Run method, which starts the generator    
        """
        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters

        self.engineStartsInfo()    # Info that the engine starts
        self.__engine()            # Run the engine
        self.engineStopsInfo()     # Info that the engine ends
        
        return self.__dict__           # Return dictionary with the parameters


    def __engine(self):
        """
        Engine of the function.

        This is the engine which generates N sparse vectors accoriding to the 
        settings to the module.
        """
        
        # Compute the number of non-zero elements in the vector X
        iNs = np.ceil(self.iS * self.iVectSiz)

        # Loop over all vectors
        self.mVects = np.zeros((self.iVectSiz, self.iNVect))  # Allocate matrix for all the vectors
        for inxVect in np.arange(self.iNVect):
            vVect = self._generate(self.iVectSiz, iNs)   # Generate a sparse vector
            vVect.shape = (vVect.size, )                 # Store the vector
            self.mVects[:, inxVect] = vVect              # ^
        return

    def _generate(self, iN, iNs):
        """
        This function generates one sparse vector (internal function). 
    
        Args:
            iN  (int):  size of the vector
            iNs (int):  the number of non-zero elements
    
        Returns:
            vX (numpy vectors):    generated sparse vector
        """
    
        vX = np.zeros((iN,1))               # Allocate X vector
        
        vInx = np.random.permutation(iN)    # Draw indices on non-zero elements
        vInx = vInx[0:iNs]                  # ^
    
        vXel = np.random.rand(iNs,1)        # Draw the non-zero elements of the vector x
        for inxEl in np.arange(iNs):        # Put the non-zero elements into the vector x
            vX[vInx[inxEl]] = vXel[inxEl]   # ^

        return vX
