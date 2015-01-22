"""
This a sparse vector generator module. |br|

It is able to generate *N* random sparse vectors according to settings
given by a user. |br|

An input dictionary, which is a sole argument to the *main*
function contains all the settings given to the generator.

There are two functions which should be used by user:

        - main(dSigConf) - this functions generate N sparse vectors
                           according to settings in dSigConf dictionary
                           Look at 'vect_sparse_ex0.py' in examples/sig 
                           directory for an example of usage.

        - generate(iN, iNs) - this function generate one vector of a size iN,
                              with with iNs non-zero elements.
                              Look at 'IRLSrecon_ex0.py' in examples/reconstruction 
                              directory for an example of usage.

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0  | 22-JAN-2014 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""

from __future__ import division
import numpy as np
import rxcs


def main(dSigConf):
    """
    This the main function of the generator and one of two functions which 
    should be accessed by a user. |br|

    An input dictionary, which is a sole argument to the function
    function contains all the settings given to the generator. |br|

    The function returns a matrix with generated vectors |br|

    Please go to the *examples* directory for examples on how to use the
    generator ('vect_sparse_ex0.py) |br|

    Fields in the configuration dictionary:

    - a. **bMute** (*int*):     mute the console output from the generator
                                [default = 1]

    - b. **iVectSiz** (*int*):  size of the vectors

    - c. **iS** (*int*):        sparsity parameter ( 0, 1 >

    - d. **iNVect** (*float*):  the number of vectors to be generated


    Args:
        dSigConf (dictionary): dictionary with configuration for the generator

    Returns:
        mVects (numpy 2D array): matrix with generated vectors 
                                 (one vector p column)
    """


    # Check if the configuration for the module make sense
    _checkConf(dSigConf)

    # Print the configuration to the console
    tStart = _printConf(dSigConf)

    # Generate sparse vectors
    mVects = _genVectors(dSigConf)

    # Info that the generation is done    
    if not np.isnan(tStart):   # <-tStart is nan = console output is off
        rxcs.console.module_progress_done(tStart)
    
    return mVects

# =================================================================
# Check the configuration dict. and get the configuration from it
# =================================================================
def _getData(dSigConf):
    """
    This function checks if all the needed configuration fields are in
    the configuration dictionary and gets these configuration fields.

    Args:
        dSigConf (dictionary): dictionary with configuration for the module

    Returns:
        bMute (number):      mute the conole output flag
        iVectSiz (number):   size of the vectors
        iS (number):         sparsity
        iNVect (number):     the number of vectors to be generated
                
    """

    # -----------------------------------------------------------------
    # Get the mute parameter
    if not 'bMute' in dSigConf:
        bMute = 1
    else:
        bMute = dSigConf['bMute']

    # -----------------------------------------------------------------
    # Get the size of the vectors
    if not 'iVectSiz' in dSigConf:
        strError = ('The size of the vectors iVectSiz) is missing ')
        strError = strError + ('in the input dictionary')
        raise NameError(strError)
    else:
        iVectSiz = dSigConf['iVectSiz']

    # -----------------------------------------------------------------
    # Get the sparsity parameter
    if not 'iS' in dSigConf:
        strError = ('The sparsity parameter (iS) is missing')
        strError = strError + (' in the input dictionary')
        raise NameError(strError)
    else:
        iS = dSigConf['iS']

    # -----------------------------------------------------------------
    # Get the number of vectors to be generated
    if not 'iNVect' in dSigConf:
        strError = ('The number of vectors to be generated (iNVect) is missing')
        strError = strError + (' in the input dictionary')
        raise NameError(strError)
    else:
        iNVect = dSigConf['iNVect']

    # -----------------------------------------------------------------
    return (bMute, iVectSiz, iS, iNVect)


# =================================================================
# Check if the configuration for the reconstruction make sense
# =================================================================
def _checkConf(dSigConf):
    """
    This function checks the configuration of the generator.

    Args:
        dSigConf (dictionary): dictionary with configuration for the generator

    Returns:
        nothing

    """
    
    # Get the configuration parameters
    (_, iVectSiz, iS, iNVect) = _getData(dSigConf)

    # -----------------------------------------------------------------
    # Check if the size of the vectors is a positive integer
    if not isinstance(iVectSiz, int):
        strError = ('The size of the vectors (iVectSiz) must be a positive integer')
        raise TypeError(strError)
    
    if iVectSiz <= 0:
        strError = ('The size of the vectors (iVectSiz) must be a positive integer')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the sparsity parameter is a number in range (0, 1>
    if not (iS > 0 and iS <= 1):
        strError = ('The sparsity parameter (iS) must be withing range (0, 1>')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    # Check if the number of vectors to be generated is a positive integer
    if not isinstance(iNVect, int):
        strError = ('The number of vectors to be generated (iNVect) must be a positive integer')
        raise TypeError(strError)
    
    if iNVect <= 0:
        strError = ('The number of vectors to be generated (iNVect) must be a positive integer')
        raise ValueError(strError)

    # -----------------------------------------------------------------
    return     

# =================================================================
# Print the configuration to the console
# =================================================================
def _printConf(dSigConf):
    """
    This function prints the generator configuration and the signal parameters
    to the console, if the 'bMute' flag on the configuration is cleared.

    Args:
        dSigConf (dictionary): dictionary with configuration for the generator

    Returns:
        tStart (float): time stamp of starting the generator

    """

    # Get the configuration parameters
    (bMute, iVectSiz, iS, iNVect) = _getData(dSigConf)

    #----------------------------------------------------------------------
    # Print the configuration if the 'mute' flag is not set
    if bMute == 0:

        # Print out the header of the sampler
        strStage = 'Signal generator'
        strModule = 'Sparse vectors generator'
        rxcs.console.progress(strStage, strModule)

        # - - - - - - - - - - - - - - - - - - -

        rxcs.console.bullet_param('size of the vectors', iVectSiz, ' ', '')

        rxcs.console.bullet_param('sparsity parameter', iS, ' ', '')
        rxcs.console.param('the number of non zero elements in the vectors',
                            int(np.ceil(iS*iVectSiz)), '-', '')

        rxcs.console.bullet_param('the number of vectors to be generated',
                                  iNVect, '-', '')

        # - - - - - - - - - - - - - - - - - - -
        # Information about the computations start
        strStartMessage = ('vectors generation starts!!!')
        tStart = rxcs.console.module_progress(strStartMessage)

    #----------------------------------------------------------------------
    else:   # <- the output was muted
        tStart = np.nan

    #----------------------------------------------------------------------
    return tStart

# =================================================================
# This is the engine of the vector generator
# =================================================================
def _genVectors(dSigConf):
    """
    This is the engine which generates N sparse vectors accoriding to the 
    settings in the configuration dictionary.

    Args:
        dSigConf (dictionary): dictionary with configuration for the generator

    Returns:
        mVects (numpy vectors): matrix with the generated sparse vectors,
                                (one vector p. column)
    """

    # Get the configuration parameters
    (bMute, iVectSiz, iS, iNVect) = _getData(dSigConf)

    iNs = np.ceil(iS * iVectSiz)  # The number of non-zero elements in the vector X
    
    # Loop over all vectors   
    mVects = np.zeros((iVectSiz, iNVect))  # Allocate matrix for all the vectors
    for inxVect in np.arange(iNVect):
        vVect = _generate(iVectSiz, iNs)   # Generate a sparse vector
        vVect.shape = (vVect.size, )      # Store the vector
        mVects[:, inxVect] = vVect        # ^

    return mVects

# =================================================================
# Generate one sparse vector (internal function)
# =================================================================
def _generate(iN, iNs):
    """
    This function generates one sparse vector. 

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


# =================================================================
# Generate one sparse vector
# =================================================================
def generate(iN, iNs):
    """
    This function generates one sparse vector.
    It can be accessed by user.

    Look at 'IRLSrecon_ex0.py' in examples/reconstruction directory for 
    an example of usage.

    Args:
        iN  (int):  size of the vector
        iNs (int):  the number of non-zero elements

    Returns:
        vX (numpy array):   generated sparse vector
    """

    # Check the input parameters
    # ----------------------------------------------------------------------
    if not (isinstance(iN, int)  and iN > 0 ):    
        strError = ("Size of the vector must be an interger higher than 0")        
        raise ValueError(strError)

    if not (isinstance(iNs, int)  and iNs > 0 ):    
        strError = ("The number of non-zero  must be an interger higher than 0")        
        raise ValueError(strError)

    if (iNs > iN):
        strError = ("Size of the vector must be an interger higher than 0")        
        raise ValueError(strError)

    # ----------------------------------------------------------------------
    vX = np.zeros((iN,1))               # Allocate X vector
    
    vInx = np.random.permutation(iN)    # Draw indices on non-zero elements 
    vInx = vInx[0:iNs]                  # ^

    vXel = np.random.rand(iNs,1)        # Draw the non-zero elements of the vector x
    for inxEl in np.arange(iNs):        # Put the non-zero elements into the vector x
        vX[vInx[inxEl]] = vXel[inxEl]   # ^

    return vX
