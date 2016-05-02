"""
This is a multi CPU wrapper. |br|


*Examples*:
    Please go to the *examples/auxiliary* directory for examples on how to use the wrapper. 

*Author*:
    Jacek Pierzchlewski, Aalborg University, Denmark. <jap@es.aau.dk>

*Version*:
    1.0    | 02-MAY-2016 : * Version 1.0 released. |br|

*License*:
    BSD 2-Clause
"""


from __future__ import division
import numpy as np
import rxcs


# Try to import multiprocessing module
bParralel = 1
try:
    import multiprocessing as mp
except:
    bParralel = 0

class parExp(rxcs._RxCSobject):

    def __init__(self, *args):
        rxcs._RxCSobject.__init__(self)    # Make it a RxCS object 
        
        self.strRxCSgroup = 'Auxiliary'          # Name of group of RxCS modules
        self.strModuleName = 'Multi CPU wrapper'  # Module name        

        self.__parametersDefine()      # Define the parameters

    def __parametersDefine(self):

        # The number of signals
        self.paramAddMan('iNSigs', 'The number of signals p. sweep point')
        self.paramType('iNSigs', (int, float))    
        self.paramH('iNSigs', 0)           
        self.paramL('iNSigs', np.inf)

        # Sweep values
        self.paramAddMan('vSweep', 'Sweep values')
        self.paramType('vSweep', (np.ndarray)) 
        self.paramNDimEq('vSweep', 1)
        self.paramDimH('vSweep', 0, 0)


        # The max number of signals in a signal pack
        self.paramAddOpt('iNSigsPackMax', 'The max number of signals in a signal pack', default='$$iNSigs')
        self.paramType('iNSigsPackMax', (int, float))    
        self.paramH('iNSigsPackMax', 0)           
        self.paramL('iNSigsPackMax', np.inf)

        # CPU Overload
        self.paramAddOpt('iCPUOverload', 'CPU overload', default=1.2)
        self.paramType('iCPUOverload', (int, float))    
        self.paramH('iCPUOverload', 0)           
        self.paramL('iCPUOverload', np.inf)

        # The maximum number of processes 
        self.paramAddOpt('iMaxProc', 'The maximum number of processes', default=np.inf)
        self.paramType('iMaxProc', (int, float))    
        self.paramH('iMaxProc', 0)

        # 'Mute the output' flag
        self.paramAddOpt('bMute', 'Mute the output', noprint=1, default=0)  
        self.paramType('bMute', int)           # Must be of int type
        self.paramAllowed('bMute',[0, 1])      # It can be either 1 or 0

        
    def run(self, dExperiment, funct):

        self.parametersCheck()         # Check if all the needed partameters are in place and are correct
        self.parametersPrint()         # Print the values of parameters
    
        # ------------------------------------------------------------------------------------
        # Run the experiments over all the sweep values
        (self.lSweepResults)  = _runSweepPoints(dExperiment, self, funct)
        
        # ------------------------------------------------------------------------------------
        # Process the output results
        self.dFinalResults = _processOutput(self.lSweepResults)
    
        # Add info to the final results
        self.dFinalResults['lSweepResults'] = self.lSweepResults
        self.dFinalResults['vSweep'] = self.vSweep
        self.dFinalResults['dExperiment'] = dExperiment
        print('')
        return self.dFinalResults

"""
    MAIN WRAPPER FNCTION:
"""
def _runSweepPoints(dExperiment, _parExp, funct):

    # Run the signle CPU or multiple CPU version
    if (bParralel == 0) or (_parExp.iMaxProc == 1):
        (lSweepResults) = _runSweepPoint_singleCPU(dExperiment, _parExp, funct)
    else:
        (lSweepResults) = _runSweepPoint_multiCPU(dExperiment, _parExp, funct)
    return (lSweepResults)


"""
    SINGLE CPU FUNCTION:
"""
def _runSweepPoint_singleCPU(dExperiment, _parExp, funct):

    # List with lists (lPacksResults) from all the results
    lSweepResults = []

    # Run the experiments over all the sweep values
    for iSweepInx in range(len(_parExp.vSweep)):

        # Compute the number of signal packs
        iNPacks = int(np.ceil(int(_parExp.iNSigs) / _parExp.iNSigsPackMax))          # The number of signal packs to be processed 
        lNSigs = iNPacks * [_parExp.iNSigsPackMax]                              # List with the number of signals in every pack
        lNSigs[-1] = int(_parExp.iNSigs) - (_parExp.iNSigsPackMax * (iNPacks - 1))   # Compute the number of signals in the last pack

        # Get the current swept value and print it out
        iSweepVal = _parExp.vSweep[iSweepInx]
        strMessage = 'Sweep value #%d: %.6f' % (iSweepInx, iSweepVal)
        tTime = rxcs.console.module_progress(strMessage)

        # Loop over all signal packs
        lPacksResults = []
        for _iNSigs in lNSigs:
            dResults = funct(dExperiment, iSweepVal, _iNSigs)
            dResults['__iNSigs__'] = _iNSigs
            lPacksResults.append(dResults.copy())

        # Store all the packs
        lSweepResults.append(lPacksResults)

        # Report
        rxcs.console.progress_done(tTime)

    return (lSweepResults)

 
"""
    MULTI CPU FUNCTIONS:
"""
def _runSweepPoint_multiCPU(dExperiment, _parExp, funct):

    # Get data from the execution settings
    #iCPUOverload = dExec['iCPUOverload']     # CPUs overload
    #vSweep = dExec['vSweep']                 # Swept parameter

    # Start the pool
    iNCPU = mp.cpu_count()
    iNProc = int(np.round(_parExp.iCPUOverload * iNCPU))
    if iNProc <= _parExp.iMaxProc:
        strCPUMessage = 'I have found %d CPUs, I am starting %d processes (overload: %.1f)...' \
            % (iNCPU, iNProc, _parExp.iCPUOverload)
        rxcs.console.info(strCPUMessage)
    else:
        iNProc = _parExp.iMaxProc
        strCPUMessage = 'I have found %d CPUs, I am starting %d processes...' \
            % (iNCPU, iNProc)
        rxcs.console.info(strCPUMessage)
    CPUpool = mp.Pool(iNProc)

    # Prepare list with sublists which contain indices of swept parameter for every process
    lInxGrid = range(len(_parExp.vSweep))   # Construct list with indices of sweep values
    lInxGrid4Process = []
    for iCPU in range(iNProc):
        lInxGrid4Process.append([lInxGrid[i] for i in range(iCPU, len(_parExp.vSweep), iNProc)])

    # Prepare a list with arguments for single process functions to be distributed by pool
    tArgs = (dExperiment, _parExp)
    ltArgs = []
    for iProc in range(iNProc):
        vSweep_ = _parExp.vSweep[lInxGrid4Process[iProc]]
        ltArgs.append(tArgs + (vSweep_, iProc, funct))

    # Run the computations on all the processes
    lProcOut = CPUpool.map(_runSweepPoint_multiCPU_poolFunc, ltArgs)

    # List with lists (lPacksResults) from all the results
    lSweepResults = [np.nan] * len(_parExp.vSweep)

    # Collect the results from all the processes
    for tProcOut in lProcOut:
        (lSweepResultsOut, iProc) = tProcOut

        # Loop over all indices of sweep values from the current process
        for iInx in range(len(lInxGrid4Process[iProc])):
            iSweepInx = lInxGrid4Process[iProc][iInx]
            lSweepResults[iSweepInx] = lSweepResultsOut[iInx]
         
    return (lSweepResults)


def _runSweepPoint_multiCPU_poolFunc(tArgs):

    (dExperiment, _parExp, vSweep, iProc, funct) = tArgs  # Unpack the arguments tuple

    # List with lists (lPacksResults) from all the results
    lSweepResults = []

    # Start a process bar 
    if iProc == 0:
        strMessage = 'There are around %d swept values p. process'  % (len(vSweep))
        dBar = rxcs.console.progress_bar_start(strMessage, 1, 5, 40, bPrintSteps=1)

    # Loop over all swept values
    for iSweepInx in np.arange(vSweep.size):

        # Compute the number of signal packs
        iNPacks = int(np.ceil(int(_parExp.iNSigs) / _parExp.iNSigsPackMax))          # The number of packs
        lNSigs = iNPacks * [_parExp.iNSigsPackMax]                      # List with the number of signals in every pack
        lNSigs[-1] = int(_parExp.iNSigs) - (_parExp.iNSigsPackMax * (iNPacks - 1))   # Compute the number of signals in the last pack

        iSweepVal = vSweep[iSweepInx]      # Get the current swept value
        
        # Loop over all signal packs
        lPacksResults = []
        for _iNSigs in lNSigs:
            dResults = funct(dExperiment, iSweepVal, int(_iNSigs))
            dResults['__iNSigs__'] = _iNSigs
            lPacksResults.append(dResults.copy())

        # Progress bar
        if iProc == 0:
            dBar = rxcs.console.progress_bar(dBar, iSweepInx+1)

        # 
        lSweepResults.append(lPacksResults)

    return (lSweepResults, iProc)


"""
    PROCESS OUTPUT:
"""
def _processOutput(lSweepResults):
    
    # Take the first output dictionary from the first sweep value and first signal packa
    dDict0 = lSweepResults[0][0]

    # Create the main results dictionary
    dFinalResults = {}
    strKeys = []
    for strKey in dDict0:
        strKeys.append(strKey)
        dFinalResults[strKey] = []

    # Loop over all result values
    for strKey in strKeys:        
        # Loop over all sweep values
        for lPacksResults in lSweepResults:
                     
            # Loop over all signal packs
            lVal = []            
            iNSigs = 0
            for dResults in lPacksResults:
                lVal.append(dResults[strKey]*dResults['__iNSigs__'])
                iNSigs = iNSigs + dResults['__iNSigs__']
            iVal = sum(lVal) / iNSigs
            dFinalResults[strKey].append(iVal)
    return dFinalResults


    

    
    
