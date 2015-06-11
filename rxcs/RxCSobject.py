"""
            This module contains _RxCSobject class, which is the main base class for 
            all modules of RxCS.     
            
            License: 
                    BSD 2-clause

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015
                    
                    
            List of functions in the module:


            Add parameters:            
            paramAddMan    - Add a mandatory parameter to the object
            paramAddOpt    - Add an optional parameter to the object


            Assign allowed type:
            paramType      - assign allowed types for a parameter
            paramTypeEl    - assign allowed types for elements of a parameter


            Assign allowed values:
            paramAllowed   - assing a list with allowed values of a parameter
            NaNAllowedEl   - Allow for NaN elements in the parameter (make sense only for tuples, lists and np.ndarrays)


            Assign parameter value restrictions:
            paramH       -  higher than
            paramL       -  lower than
            paramHE      -  higher or equal than
            paramLE      -  lower or equal than
            
            
            Assign parameter size restrictions:
            paramSizEq      - size equal to
            paramSizH       - size higher than
            paramSizL       - size lower than
            paramSizHE      - size higher or equal to
            paramSizLE      - size lower or equal to
            
            
            Assign parameter restriction of the number of dimensions:            
            paramNDimEq      - the number of dimensions equal to
            paramNDimH       - the number of dimensions higher than
            paramNDimL       - the number of dimensions lower than
            paramNDimHE      - the number of dimensions higher or equal to
            paramNDimLE      - the number of dimensions lower or equal to


            Get and check the parameters given to the module:            
            parametersProcess   - process parameters given to a module as arguments for 'run' function
            parametersCheck     - check if all parameters of a module are correct 
            
            Paramters printing:
            parametersPrint     - print parameters of a module
            changeUnitPRefix    - change prefered unit prefix of a parameter
            
            Engine start/stop information:
            engineStartsInfo    - function prints info about start of a module engine
            engineStopsInfo     - function prints info about stop of a module engine



            INTERNAL FUNCTIONS:
                      
            __isParameterNameOK          -  check if a name of a parameter is correct
            __paramAddRelRestriction     -  assign relational restriction to a parameter
            __paramAddSizRestriction     -  assign size restriction to a parameter
            __paramAddNDimRestriction    -  assign restriction on the number of dimensions of a parameter
            
            __parameterWasDefined         - check if a parameter with a given name was already defined
                        
            __parametersGetDict            - get parameters given to a function as dictionary
            __parametersGetArgs            - get parameters given directly to a function as a list of arguments

            __parametersCheckMandatory       - check if all the mandatory parameters are given
            __parametersCheckType            - check types of all the parameters and their elements
            __parametersCheckRestrictions    - check restrictions given to all the parameters
            __parameterCheckRestrictions     - check restrictions of a single parameter


            Control of 'allowed values' restrictions:
            __checkAllowedVal
            __checkAllowedVal_numstr  
            __checkAllowedVal_atl     


            Control of relational value restrictions:
            __checkRelVal    
            __checkRelVal_num
            __checkRelVal_atl     
            __checkRelVal_engine  


            Control of size restrictions:
            __checkSiz              
            __checkSiz_sizParam      
            __checkSiz_sizRef              
            __checkSiz_engine       
            __checkSiz_error        


            Control of restrictions on the number of dimensions:
            __checkNDim                
            __checkNDim_NDimInParam    
            __checkNDim_NDimInRef      
            __checkNDim_engine         
            __checkNDim_error          

            
            Control of restrictions on the size of dimensions:
            __checkDimSiz                 
            __checkDimSiz_dimensions
            __checkDimSiz_dimSizInParam
            __checkDimSiz_dimSizInRef
            __checkDimSiz_engine  
            __checkDimSiz_error    
            
            
            Auxiliary functions:
            __linearCoef2Strings - change linear coefficients to strings
            __n2s                - change number to a string, 
                                 automatically regulate the number of digits after the comma
            __NthInTuple         - takes Nth element of a tuple


"""
from __future__ import division
import numpy as np
import rxcs

class _RxCSobject:

    def __init__(self):
        self.strRxCSgroup = ''   # Initilize empty name of group of RxCS modules
        self.strModuleName = ''  # Initialize empty module name        
        
        self.lParameters = []    # List with parameters
        self.iManParam = 0       # The number of mandatory parameters
        self.iOptParam = 0       # The number of optional parameters


    def paramAddMan(self, strName, strDesc, unit='', noprint=0, unitprefix='-'):
        """
            Add a mandatory parameter to the object.
    
            Arguments:
                    strName:   [string]     name of a parameter, will become public class member
                    strDesc:   [string]     short description of a parameter
                    unit:      [string]     unit of a parameter
                    noprint:   [number]     switch off priting a parameter to the console by 'parametersPrint' function
                                            (optional, default is 0 = print the parameter)

                    unitprefix [string] prefered unit prefix of a parameter to be printed
                                        (optional, default is '-', which means that CPU chooses the unit prefix,
                                        allowed values = f:femto, p:pico, n:nano, u:micro, m:mili,
                                        ' ':one, k:kilo, M:mega, G:giga, T:tera,-:CPU decides)
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    29 may 2015                
        """
        # Error checks -------------------------------------------------------
        if (self.iOptParam > 0):
            raise RuntimeError('Mandatory parameter cannot be defined after optional!')

        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')
        self.__isParameterNameOK(strName)

        if not isinstance(strDesc, str):        
            raise ValueError('Description of a parameter must be a string!')

        if not isinstance(unit, str):        
            raise ValueError('Unit of a parameter must be a string!')

        if not isinstance(noprint, int):        
            raise ValueError('\'noprint\' parameter must be a number')

        if not isinstance(unitprefix, str):        
            raise ValueError('Unit prefix must be a string!')
        
        (bDefined, _) = self.__parameterWasDefined(strName)
        if bDefined:
            strError = ('Parameter %s was already defined!') % strName
            raise RuntimeError(strError)
        #---------------------------------------------------------------------

        # Add parameter  to the list of names
        self.__dict__[strName] = np.nan

        dParameter = {}
        dParameter['strName'] = strName             # Name of a parameter
        dParameter['strDesc'] = strDesc             # Description
        dParameter['bOptional'] = 0                 # Mandatory/Optional flag
        dParameter['defaultValue'] = np.nan         # Default Value
        dParameter['strUnit'] = unit                # Unit
        dParameter['strUnitPrefix'] = unitprefix    # Unit prefix
        dParameter['bNoPrint'] = noprint            # NoPrint flag
        dParameter['bNaNAllowedEl'] = 0             # By default NaN elements are not allowed
        dParameter['lRes'] = []                     # List of restriction
        dParameter['lResErrNote'] = []              # List of error notes for restrictions
        dParameter['lResReference'] = []            # List of references for restrictions
        dParameter['lResData'] = []                 # List of additional data for restrictions

        self.lParameters.append(dParameter)
        
        self.iManParam = self.iManParam + 1  # The number of mandatory parameters


    def paramAddOpt(self, strName, strDesc, unit='', noprint=0, unitprefix='-', default=np.nan):
        """
            Add an optional parameter to the object.
    
            Arguments:
                    strName: [string]   name of a parameter, will become public class member
                    strDesc: [string]   short description of a parameter
                    unit:    [string]   unit of a parameter
                    noprint: [int]      switch off priting a parameter to the console by 'parametersPrint' function
                                        (optional, default is 0 = print the parameter)
                                    
                    unitprefix [string] prefered unit prefix of a parameter to be printed
                                        (optional, default is '-', which means that CPU chooses the unit prefix,
                                        allowed values = f:femto, p:pico, n:nano, u:micro, m:mili,
                                        ' ':one, k:kilo, M:mega, G:giga, T:tera,-:CPU decides)

                    default             default value
                                        (optional, by default it is np.nan)

            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    29 may 2015                
        """    

        # Error checks -------------------------------------------------------      
        if not isinstance(strName, str):        
            raise ValueError('Name of a parameter must be a string!')
        self.__isParameterNameOK(strName)

        if not isinstance(strDesc, str):        
            raise ValueError('Description of a parameter must be a string!')

        if not isinstance(unit, str):        
            raise ValueError('Unit of a parameter must be a string!')

        if not isinstance(noprint, int):        
            raise ValueError('\'noprint\' parameter must be a number')

        if not isinstance(unitprefix, str):        
            raise ValueError('Unit prefix must be a string!')

        (bDefined, _) = self.__parameterWasDefined(strName)
        if bDefined:
            strError = ('Parameter %s was already defined!') % strName
            raise RuntimeError(strError)
        #---------------------------------------------------------------------
        
        # Add parameter  to the list of names
        self.__dict__[strName] = default
        
        dParameter = {}
        dParameter['strName'] = strName             # Name of a parameter
        dParameter['strDesc'] = strDesc             # Description
        dParameter['bOptional'] = 1                 # Mandatory/Optional flag
        dParameter['defaultValue'] = default        # Default value
        dParameter['strUnit'] = unit                # Unit
        dParameter['strUnitPrefix'] = unitprefix    # Unit prefix
        dParameter['bNoPrint'] = noprint            # NoPrint flag
        dParameter['lRes'] = []                     # List of restriction
        dParameter['bNaNAllowedEl'] = 0             # By default NaN elements are not allowed
        dParameter['lResErrNote'] = []              # List of error notes for restrictions
        dParameter['lResReference'] = []            # List of references for restrictions
        dParameter['lResData'] = []                 # List of additional data for restrictions
 
        self.lParameters.append(dParameter)        

        self.iOptParam = self.iOptParam + 1  # The number of optional parameters


    def paramType(self, strName, types):
        """
            Assign allowed types to a parameter. If types are assigned, it will be 
            checked if the parameter is of correct type.
                                
            Arguments:
                    strName: [string]         name of the parameter
                    types: [type/tuple/list]  allowed types
                    
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    2 june 2015                
        
        """

        # Error checks -------------------------------------------------------

        # Check the given parameter
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter %s was not yet defined!') % strName
            raise RuntimeError(strError)

        # Check the given types        
        if isinstance(types, type):
            types = [types]
        elif(isinstance(types, list)):
            strWasGiven = 'list'
        elif(isinstance(types, tuple)):
            strWasGiven = 'tuple'
            types = list(types)
        else:
            raise ValueError('Allowed types of a parameter must be a type, a tuple of types, or a list of types!')
        
        # Check the list with allowed types
        for inxType in range(len(types)):
            if (not isinstance(types[inxType], type)):
                strErr = 'Allowed types of a parameter must be a type, a tuple of types, or a list of types!'
                strErr = strErr + '\n            Element #%d of the given %s of types is: %s' % \
                    (inxType, strWasGiven, type(types[inxType]))
                raise ValueError(strErr)

        #---------------------------------------------------------------------
        self.lParameters[inxParam]['lTypes'] = types
        return


    def paramTypeEl(self, strName, types):
        """
            Assign allowed types of parameter to a parameter. 
            If types are assigned, it will be checked if elements of a parameter 
            are of correct types.
            It will be checked only if a parameter is of type:
            
                - list
                - tuple
                - numpy array
                                
            Arguments:
                    strName: [string]         name of a parameter
                    types: [type/tuple/list]  allowed types
                    
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    2 june 2015                
        
        """

        # Error checks -------------------------------------------------------

        # Check the given parameter
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter %s was not yet defined!') % strName
            raise RuntimeError(strError)

        # Check the given types        
        if isinstance(types, type):
            types = [types]
        elif(isinstance(types, list)):
            strWasGiven = 'list'
        elif(isinstance(types, tuple)):
            strWasGiven = 'tuple'
            types = list(types)
        else:
            raise ValueError('Allowed types of elements of a parameter must be a type, a tuple of types, or a list of types!')
        
        # Check the list with allowed types
        for inxType in range(len(types)):
            if (not isinstance(types[inxType], type)):
                strErr = 'Allowed types of a elements of parameter must be a type, a tuple of types, or a list of types!'
                strErr = strErr + '\n            Element #%d of the given %s of types is: %s' % \
                    (inxType, strWasGiven, type(types[inxType]))
                raise ValueError(strErr)
        #---------------------------------------------------------------------
        self.lParameters[inxParam]['lTypesEl'] = types
        return


    def NaNAllowedEl(self, strName):
        """
            Allow for NaN values of elements of a parameter.
            Using this function make sense only for tuples, lists and np.ndarrays,
            in combination with relational restriction functions, which are 
            paramH, paramL, paramHE, paramLE.
            
            If a parameter contains NaN elements, but no relational restriction 
            is imposed, the parameter will be treated as correct even though
            the NaN parameters were not allowed.


            Arguments:
                    strName: [string]   name of a parameter

            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015
        """    

        # Error checks -------------------------------------------------------

        # Check the given parameter
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter %s was not yet defined!') % strName
            raise RuntimeError(strError)

        #---------------------------------------------------------------------
        self.lParameters[inxParam]['bNaNAllowedEl'] = 1
        return


    def paramAllowed(self, strName, lAllowed, errnote=''):
        """
            Assign allowed values for a parameter.

            Arguments:
                    strName:  [string]         name of a parameter
                    lAllowed: [list/tuple]     a list or a tuple with allowed values
                    errnote:  [string]         error note to be printed if a parameter will not contain one of allowed values
                                               (optional, by default it is '' (empty string), which means that an error
                                               note will be constructed automatically)

            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015
        """    

        # Error checks -------------------------------------------------------
        
        # Parameter to be checked        
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter > %s < was not yet defined!') % strName
            raise RuntimeError(strError)

        # List of allowed values
        if not isinstance(lAllowed, (list, tuple)):                       
             raise ValueError('Allowed values must be grouped in a list or in a tuple!')
             
        if isinstance(lAllowed, tuple):
            lAllowed = list(lAllowed)

        # Error note
        if not isinstance(errnote, str):
            raise ValueError('Error note must be a string!')

        #---------------------------------------------------------------------
        self.lParameters[inxParam]['lRes'].append('allowed values')
        self.lParameters[inxParam]['lResErrNote'].append(errnote)
        self.lParameters[inxParam]['lResReference'].append('')
        self.lParameters[inxParam]['lResData'].append(lAllowed)
        

    def paramH(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - higher than a reference 
                                            
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    29 may 2015                
        
        """
        self.__paramAddRelRestriction('higher than', strName, reference, mul, add, errnote)


    def paramL(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - lower than a reference 

            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)

            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    29 may 2015                
        
        """
        self.__paramAddRelRestriction('lower than', strName, reference, mul, add, errnote)


    def paramHE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - higher or equal to a reference 
                                            
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)

            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    29 may 2015                
        
        """
        self.__paramAddRelRestriction('higher or equal to', strName, reference, mul, add, errnote)


    def paramLE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - lower or equal to a reference 
                                            
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)

            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    29 may 2015                
        
        """
        self.__paramAddRelRestriction('lower or equal to', strName, reference, mul, add, errnote)



    def paramSizEq(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign size restriction to a parameter - size equal to a reference 

            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)

            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015                
        
        """

        self.__paramAddSizRestriction('size equal to', strName, reference, mul, add, errnote)


    def paramSizH(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign size restriction to a parameter - size higher than a reference 

            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)

            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015                
        
        """
        self.__paramAddSizRestriction('size higher than', strName, reference, mul, add, errnote)


    def paramSizL(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign size restriction to a parameter - size lower than a reference 
    
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)
    
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015                
        
        """
        self.__paramAddSizRestriction('size lower than', strName, reference, mul, add, errnote)


    def paramSizHE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign size restriction to a parameter - size higher than a reference 
    
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)
    
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015                
        
        """
        self.__paramAddSizRestriction('size higher or equal to', strName, reference, mul, add, errnote)


    def paramSizLE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign size restriction to a parameter - size lower or equal to a reference 
    
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)
    
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015                
        
        """
        self.__paramAddSizRestriction('size lower or equal to', strName, reference, mul, add, errnote)


    def paramNDimEq(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign restriction on the number of dimensions to a parameter - 
            the number of dimensions equal to a reference 
    
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)
    
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015                
        
        """
        self.__paramAddNDimRestriction('number of dimensions equal to', strName, reference, mul, add, errnote)

        
    def paramNDimH(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign restriction on the number of dimensions to a parameter - 
            the number of dimensions higher than a reference 
    
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)
    
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015                
        
        """
        self.__paramAddNDimRestriction('number of dimensions higher than', strName, reference, mul, add, errnote)

        
    def paramNDimHE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign restriction on the number of dimensions to a parameter - 
            the number of dimensions higher or equal to a reference 
    
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)
    
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015                
        
        """
        self.__paramAddNDimRestriction('number of dimensions higher or equal to', strName, reference, mul, add, errnote)

        
    def paramNDimL(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign restriction on the number of dimensions to a parameter - 
            the number of dimensions lower than a reference 
    
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)
    
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015                
        
        """
        self.__paramAddNDimRestriction('number of dimensions lower than', strName, reference, mul, add, errnote)


    def paramNDimLE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign restriction on the number of dimensions to a parameter - 
            the number of dimensions lower or equal to a reference 
    
            Arguments:
                    strName:   [string]          name of the parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this 
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)
    
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    5 june 2015                
        
        """
        self.__paramAddNDimRestriction('number of dimensions lower or equal to', strName, reference, mul, add, errnote)


    def paramDimEq(self, strName, reference, iDim, refdim=np.nan, pedantic=0, mul=1, add=0, errnote=''):
        self.__paramAddDimSizRestriction('dimension size equal to', strName, reference, pedantic, iDim, refdim, mul, add, errnote)


    def paramDimH(self, strName, reference, iDim, refdim=np.nan, pedantic=0, mul=1, add=0, errnote=''):
        self.__paramAddDimSizRestriction('dimension size higher than', strName, reference, pedantic, iDim, refdim, mul, add, errnote)


    def paramDimL(self, strName, reference, iDim, refdim=np.nan, pedantic=0, mul=1, add=0, errnote=''):
        self.__paramAddDimSizRestriction('dimension size lower than', strName, reference, pedantic, iDim, refdim, mul, add, errnote)


    def paramDimHE(self, strName, reference, iDim, refdim=np.nan, pedantic=0, mul=1, add=0, errnote=''):
        self.__paramAddDimSizRestriction('dimension size higher or equal to', strName, reference, pedantic, iDim, refdim, mul, add, errnote='')


    def paramDimLE(self, strName, reference, iDim, refdim=np.nan, pedantic=0, mul=1, add=0, errnote=''):
        self.__paramAddDimSizRestriction('dimension size lower or equal to', strName, reference, pedantic, iDim, refdim, mul, add, errnote='')


    def parametersProcess(self, *args):
        """
            Process parameters given to a module as arguments for 'run' function.
                                            
            Arguments:                    
                    args:   [list]    list of argments
            
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """
        
        if len(args) == 0:
            return
 
        firstArg = self.__NthInTuple(0, args)  # Get the first argument
        if isinstance(firstArg, dict):
            self.__parametersGetDict(firstArg)
        else:
            self.__parametersGetArgs(*args)
        return


    def parametersCheck(self):
        """
            Function checks if all parameters of a module are correct.            
     
            Arguments:                    
                    none
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """
        self.__parametersCheckMandatory()     # Check if all the mandatory parameters are given 
        self.__parametersCheckType()          # Check types of all the parameters
        self.__parametersCheckRestrictions()  # Check restrictions on the parameters


    def parametersPrint(self):
        """
            Function prints parameters of a module.

            Arguments:
                    none

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """
        if self.bMute == 0:
    
            # Print out the header of the module
            rxcs.console.progress(self.strRxCSgroup, self.strModuleName)

            # Loop over all parameters
            for inxPar in range(self.iManParam + self.iOptParam):
                dParam = self.lParameters[inxPar]   # Dictionary of the parameter
                if (dParam['bNoPrint'] == 1):
                    continue
                
                strDesc = dParam['strDesc']                  # Description of the parameter
                strUnit = dParam['strUnit']                  # Unit of the parameter
                strUnitPrefix = dParam['strUnitPrefix']      # Unit prefix
                strParName = dParam['strName']              # Name of the parameter
                par = self.__dict__[strParName]             # The parameter itself
                
                # Run the correct function dependently on the type of the parameter           
                if isinstance(par, (int, float)):
                    if np.isnan(par):
                        rxcs.console.bullet_info(strDesc, 'NaN')
                    else:
                        rxcs.console.bullet_param(strDesc, par, strUnitPrefix, strUnit)
                elif isinstance(par, str):
                    rxcs.console.bullet_info(strDesc, par)
        return


    def changeUnitPRefix(self, strName, strUnitPrefix):
        """
            Function changes prefered unit prefix of a parameter
            
             Arguments:
                    strName:     [string]   name of the parameter
                    unitprefix   [string]   prefered unit prefix of a parameter to be printed
                                            allowed values = f:femto, p:pico, n:nano, u:micro, m:mili,
                                            ' ':one, k:kilo, M:mega, G:giga, T:tera)
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    29 may 2015
        """

        if not isinstance(strName, str):        
            raise ValueError('Name of a parameter must be a string!')
        self.__isParameterNameOK(strName)

        if not isinstance(strUnitPrefix, str):        
            raise ValueError('Unit prefix must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter %s was not yet defined!') % strName
            raise RuntimeError(strError)

        self.lParameters[inxParam]['strUnitPrefix'] = strUnitPrefix

        return


    def engineStartsInfo(self):
        """
            Function prints info about start of a module engine.
            
            Arguments:
                    none

            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    29 may 2015
        """

        if self.bMute == 0:
            strName = ('%s: \'%s\' is starting') % (self.strRxCSgroup, self.strModuleName) 
            self.tStart = rxcs.console.module_progress(strName)


    def engineStopsInfo(self):
        """
            Function prints info about stop of a module engine.
            
            Arguments:
                    none

            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    29 may 2015
        """

        if self.bMute == 0:
            strName = ('%s: \'%s\'.............') % (self.strRxCSgroup, self.strModuleName) 
            rxcs.console.module_progress(strName)
            rxcs.console.module_progress_done(self.tStart)


    ###------------------------------------------------------------------------
    ### INTERNAL FUNCTIONS:
    ###------------------------------------------------------------------------


    def __isParameterNameOK(self, strName):
        """
            Check if a name of a parameter is correct.
            It is allowed to contain only letters, numbers or '_' (underscore).
            The first letter can not be a number.
    
            Arguments:
                    strName: [string]   name to be checked
            Output:
                    none, the function raises an error if the name is incorrect
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
            
            Last modification:
                    29 may 2015                
        
        """
        if len(strName) == 0:
            raise ValueError('Name of a parameter can not be empty!')
        
        # Check the first letter
        chr1 = strName[0]         # Take the first letter
        if not chr1.isalpha():    # 
            if not (chr1 == '_'):       
                strError = '>%s< is an incorrect name for a parameter' % (strName)
                raise ValueError(strError)
        
        # Check the rest of the letters
        for inxChr in range(1,len(strName)):
            chrLetter = strName[inxChr]         # Take a current letter
            if not (chrLetter.isalpha() or chrLetter.isdigit() or (chrLetter == '_')):
                strError = '>%s< is an incorrect name for a parameter' % (strName)
                raise ValueError(strError)
        return


    def __paramAddRelRestriction(self, strResCode, strName, reference, iMul, iAdd, strErrNote):
        """
            Assign relational restriction to a parameter
                                            
            Arguments:
                    
                    strResCode:   [string]          code of the restriction
                    strName:      [string]          name of the parameter
                    reference:    [string/number]   reference, it can be a number or a name of another parameter
                    iMul:         [number]          multiply coefficient, reference will be multipled by this 
                    iAdd:         [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    strErrNote    [string]          optional error note, will be displayed if the restriction is broken
            
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """

        # Error checks -------------------------------------------------------
        
        # Parameter to be checked        
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter > %s < was not yet defined!') % strName
            raise RuntimeError(strError)
            
        # Restriction code
        if not isinstance(strResCode, str):
            raise ValueError('Restriction code must be a string!')

        # Multiply coefficient
        if not isinstance(iMul, (int, float)):
            raise ValueError('> mul < parameter must be a number ')

        # Add coefficient
        if not isinstance(iAdd, (int, float)):
            raise ValueError('> add <  parameter must be a number ')
        
        # Error note
        if not isinstance(strErrNote, str):
            raise ValueError('Error note must be a string ')

        # Reference          
        if not isinstance(reference, (str, int, float, tuple, np.ndarray, list)):
            strError = 'Reference for relational restriction must be a string, a real number, a tuple, a list or a numpy array!'
            raise ValueError(strError)
        if isinstance(reference, float) :
            if np.isnan(reference): 
                raise ValueError('Reference must not be nan!')

        #---------------------------------------------------------------------
        self.lParameters[inxParam]['lRes'].append(strResCode)
        self.lParameters[inxParam]['lResErrNote'].append(strErrNote)
        self.lParameters[inxParam]['lResReference'].append(reference)
        self.lParameters[inxParam]['lResData'].append([iMul, iAdd])

        return


    def __paramAddSizRestriction(self, strResCode, strName, reference, iMul, iAdd, strErrNote):
        """
            Assign size restriction to a parameter
                                            
            Arguments:
                    
                    strResCode:   [string]          code of the restriction
                    strName:      [string]          name of the parameter
                    reference:    [string/number]   reference, it can be a number or a name of another parameter
                    iMul:         [number]          multiply coefficient, reference will be multipled by this 
                    iAdd:         [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    strErrNote    [string]          optional error note, will be displayed if the restriction is broken
            
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """

        # Error checks -------------------------------------------------------
        
        # Parameter to be checked        
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter > %s < was not yet defined!') % strName
            raise RuntimeError(strError)
            
        # Restriction code
        if not isinstance(strResCode, str):
            raise ValueError('Restriction code must be a string!')

        # Multiply coefficient
        if not isinstance(iMul, (int, float)):
            raise ValueError('> mul < parameter must be a number ')

        # Add coefficient
        if not isinstance(iAdd, (int, float)):
            raise ValueError('> add <  parameter must be a number ')
        
        # Error note
        if not isinstance(strErrNote, str):
            raise ValueError('Error note must be a string ')

        # Reference          
        if not isinstance(reference, (str, int, float, tuple, np.ndarray, list)):
            strError = 'Reference must be a string, a real number, a tuple, a list or a numpy array!\n'
            strError = strError + '            Reference for restriction \'%s\' for parameter > %s < is of type: %s!' \
                % (strResCode, strName, type(reference))
            raise ValueError(strError)
        if isinstance(reference, float) :
            if np.isnan(reference): 
                strError = 'Reference must not be NaN!\n'
                strError = strError + '            Reference for restriction \'%s\' for parameter > %s < is NaN!' \
                    % (strResCode, strName)
                raise ValueError(strError)

        #---------------------------------------------------------------------
        self.lParameters[inxParam]['lRes'].append(strResCode)
        self.lParameters[inxParam]['lResErrNote'].append(strErrNote)
        self.lParameters[inxParam]['lResReference'].append(reference)
        self.lParameters[inxParam]['lResData'].append([iMul, iAdd])

        return


    def __paramAddNDimRestriction(self, strResCode, strName, reference, iMul, iAdd, strErrNote):
        """
            Assign restriction on the number of dimensions of a parameter
                                            
            Arguments:
                    
                    strResCode:   [string]          code of the restriction
                    strName:      [string]          name of the parameter
                    reference:    [string/number]   reference, it can be a number or a name of another parameter
                    iMul:         [number]          multiply coefficient, reference will be multipled by this 
                    iAdd:         [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    strErrNote    [string]          optional error note, will be displayed if the restriction is broken
            
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """
        
        # Error checks -------------------------------------------------------
        
        # Parameter to be checked        
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter > %s < was not yet defined!') % strName
            raise RuntimeError(strError)
            
        # Restriction code
        if not isinstance(strResCode, str):
            raise ValueError('Restriction code must be a string!')

        # Multiply coefficient
        if not isinstance(iMul, (int, float)):
            raise ValueError('> mul < parameter must be a number ')

        # Add coefficient
        if not isinstance(iAdd, (int, float)):
            raise ValueError('> add <  parameter must be a number ')
        
        # Error note
        if not isinstance(strErrNote, str):
            raise ValueError('Error note must be a string ')

        # Reference          
        if not isinstance(reference, (str, int, float, tuple, np.ndarray, list)):
            strError = 'Reference for restriction of the no. of dimensions must be\n'
            strError = strError + '            a string, a real number, a tuple, a list or a numpy array!'
            raise ValueError(strError)
        if isinstance(reference, float) :
            if np.isnan(reference): 
                raise ValueError('Reference must not be nan!')

        #---------------------------------------------------------------------
        self.lParameters[inxParam]['lRes'].append(strResCode)
        self.lParameters[inxParam]['lResErrNote'].append(strErrNote)
        self.lParameters[inxParam]['lResReference'].append(reference)
        self.lParameters[inxParam]['lResData'].append([iMul, iAdd])

        return


    def __paramAddDimSizRestriction(self, strResCode, strName, reference, bPedantic, iDim, iRefDim, iMul, iAdd, strErrNote):

        # Error checks -------------------------------------------------------
        
        # Parameter to be checked        
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter > %s < was not yet defined!') % strName
            raise RuntimeError(strError)
            
        # Restriction code
        if not isinstance(strResCode, str):
            raise ValueError('Restriction code must be a string!')

        # Dimension index
        if not isinstance(iDim, int):
            raise ValueError('Dimension index must be an integer number ')

        # Reference dimension index
        if not isinstance(iRefDim, int):
            if isinstance(iRefDim, float):
                if not np.isnan(iRefDim):
                    raise ValueError('Dimension index of a reference must be an integer number or NaN!')
            else:
                    raise ValueError('Dimension index of a reference must be an integer number or NaN!')

        # Multiply coefficient
        if not isinstance(iMul, (int, float)):
            raise ValueError('> mul < parameter must be a number ')

        # Add coefficient
        if not isinstance(iAdd, (int, float)):
            raise ValueError('> add <  parameter must be a number ')
        
        # Error note
        if not isinstance(strErrNote, str):
            raise ValueError('Error note must be a string ')

        # Reference          
        if not isinstance(reference, (str, int, float, tuple, np.ndarray, list)):
            strError = 'Reference for restriction of the dimension size must be\n'
            strError = strError + '            a string, a real number, a tuple, a list or a numpy array!'
            raise ValueError(strError)
        if isinstance(reference, float) :
            if np.isnan(reference): 
                raise ValueError('Reference must not be nan!')

        #---------------------------------------------------------------------
        self.lParameters[inxParam]['lRes'].append(strResCode)
        self.lParameters[inxParam]['lResErrNote'].append(strErrNote)
        self.lParameters[inxParam]['lResReference'].append(reference)
        self.lParameters[inxParam]['lResData'].append([iMul, iAdd, iDim, iRefDim, bPedantic])

        return


    def __parameterWasDefined(self, strName):
        """
            Check if a parameter with a given name was already defined 
                                            
            Arguments:                    
                    strName:   [string]          name of the parameter
            
            Output:
                    bDefined:  [number]     0 - was not defined, 1 - yes, it was 
                    iPos:      [number]     position of a defined parameter in the parameters list
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """        
        inxParam = 0
        for dParam in self.lParameters:
            if strName == dParam['strName']:
                return (1, inxParam)
            inxParam = inxParam + 1
        return (0, -1)



    def __parametersGetDict(self, dArgInput):
        """
            Get the parameters given to a function as dictionary            
      
            Arguments:                    
                    dArgInput:   [dictionary]    dictionary with argments
            
            Output:
                    none
                    
            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """
        # Loop over all defined parameters         
        for dParam in self.lParameters:
            strParName = dParam['strName']
            if strParName in dArgInput:
                self.__dict__[strParName] = dArgInput[strParName]
        return


    def __parametersGetArgs(self, *args):
        """
            Get the parameters given directly to a function as a list of arguments.            
     
            Arguments:                    
                    args:   [list]    dictionary with argments

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """

        if len(args) > (self.iManParam + self.iOptParam):
            raise ValueError('To many arguments!')
        
        # Loop over all defined parameters
        inxArg = 0 
        for arg in args:
            strParName = self.lParameters[inxArg]['strName']
            self.__dict__[strParName] = arg
            inxArg = inxArg + 1
        return


    def __parametersCheckMandatory(self):
        """
            Function checks if all the mandatory parameters are given.
     
            Arguments:                    
                    none
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """
        # Loop over all parameters 
        for inxMan in range(self.iManParam):
            strParName = self.lParameters[inxMan]['strName']
            if isinstance(self.__dict__[strParName], float):
                if np.isnan(self.__dict__[strParName]):
                    strError = ('Mandatory parameter > %s < is not given!') % strParName
                    raise ParameterMissingError(strError)


    def __parametersCheckType(self):
        """
            Function checks types of all the parameters and their elements.
     
            Arguments:                    
                    none
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    1 june 2015
        """
        # Loop over all parameters 
        for inxPar in range(self.iManParam + self.iOptParam):

            # If type is not give, continue to the next parameter            
            if not 'lTypes' in self.lParameters[inxPar]:
                continue

            # Get the name of the parameter, allowed types and the parameter itself
            strParName = self.lParameters[inxPar]['strName']   # Name of the current parameter
            strDesc = self.lParameters[inxPar]['strDesc']      # Description of the currect parameter
            lTypes = self.lParameters[inxPar]['lTypes']        # Allowed types of the current parameter
            parameter = self.__dict__[strParName]              # Get the parameter

            # Check the type
            if not (isinstance(parameter,tuple(lTypes))):
                strError = ('Type %s is incorrect for parameter > %s < !') % (type(parameter), strParName)
                raise ParameterTypeError(strError)
            
            # Check types of elements, if needed
            if isinstance(parameter, (np.ndarray, list, tuple)):
                if not 'lTypesEl' in self.lParameters[inxPar]:
                    continue
                lTypesEl = self.lParameters[inxPar]['lTypesEl']   # Allowed types of elements of the current parameter

                # Service for numpy array
                if isinstance(parameter, np.ndarray):
                    if (parameter.size > 0):
                        if not (isinstance(parameter[0], tuple(lTypesEl))):
                            strError = ('Parameter > %s < contains elements of an illegal type (%s)!') \
                                % (strParName, type(parameter[0]))
                            raise ElementTypeError(strError)
                    continue

                # Service for a tuple or a list
                for inxEl in range(len(parameter)):       # Loop over all elements of the current parameter
                    if not (isinstance(parameter[inxEl], tuple(lTypesEl))):
                        strError = ('Parameter > %s < on position %d contains an element of an illegal type (%s)!') \
                            % (strParName, inxEl, type(parameter[inxEl]))
                        raise ElementTypeError(strError)
            
            # Check if an elements type check was assigned to soemthing elese than a 
            # tuple, a list or a Numpy array. If yes, it is an error.
            else:
                if 'lTypesEl' in self.lParameters[inxPar]:
                    strError = ('Elements type check can be assigned only to tuples, lists and Numpy arrays!\n')
                    strError = strError + ('            Parameter > %s < (%s) is of type %s') \
                        % (strParName, strDesc, type(parameter))
                    raise ValueError(strError)
                
        return


    def __parametersCheckRestrictions(self):
        """
            Function checks restrictions given to all the parameters.
     
            Arguments:                    
                    none
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """
        
        # Loop over all parameters 
        for inxPar in range(self.iManParam + self.iOptParam):
            dParam = self.lParameters[inxPar]
            self.__parameterCheckRestrictions(dParam)


    def __parameterCheckRestrictions(self, dParam):
        """
            Function checks restrictions of a single parameter.

            Arguments:                    
                    dParam [dictionary]   dictionary with parameter data
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """
        strParName = dParam['strName']            # Name of the parameter
        strDesc = dParam['strDesc']               # Description of the parameter 
        bNaNAllowedEl = dParam['bNaNAllowedEl']   # NaN elements allowed flag
        parVal = self.__dict__[strParName]        # The parameter itself

        # If the parameter is NaN than there is nothing to be checked
        if isinstance(parVal, float):
            if np.isnan(parVal):
                return

        # Loop over all restrictions
        for inxRes in range(len(dParam['lRes'])):

            # Get the restriction code, error note, reference and coefficients
            strRes = dParam['lRes'][inxRes]                # Restriction                 
            lResData = dParam['lResData'][inxRes]          # Data associated with the restriction
            reference = dParam['lResReference'][inxRes]    # Reference
            strErrNote = dParam['lResErrNote'][inxRes]     # Error note
            
            # Change the reference into its value and a string with a name of the referenece
            if isinstance(reference, str):
                
                if not (reference == ''):
                    (bDefinedRef, inxRef) = self.__parameterWasDefined(reference)
                    if not bDefinedRef:
                        strError = ('Reference > %s < was not yet defined!') % reference
                        raise RuntimeError(strError)
                    refVal = self.__dict__[reference]       # value
                    strRefName = '> %s <' % (reference)     # string with name
                else:
                    # If reference is an empty string, it means we do not need it
                    # But a restriction check function may have a different opinion....
                    refVal = np.nan
                    strRefName = '> (empty) <'
            else:
                refVal=reference                        # value

                # string with name of the reference
                if isinstance(reference, float):
                    strRefName = ('the given number')       # float
                elif isinstance (reference, int):
                    strRefName = ('the given number')       # int
                elif isinstance (reference, tuple):
                    strRefName = 'the given tuple'          # tuple
                elif isinstance (reference, list):
                    strRefName = 'the given list'           # list
                elif isinstance (reference, np.ndarray):
                    strRefName = 'the given numpy array'    # numpy array
                else:
                    strRefName = 'the given variable'      # everythin else

            # Run the correct parameter restriction check function:
            # allowed values
            if (strRes == 'allowed values'):
                self.__checkAllowedVal(strParName, strDesc, parVal, lResData, strErrNote, bNaNAllowedEl)                
            
            # value relational restrictions
            elif (strRes == 'higher than' or \
                  strRes == 'higher or equal to' or \
                  strRes == 'lower than' or \
                  strRes == 'lower or equal to'):    
                  self.__checkRelVal(strParName, strDesc, parVal, strRefName, refVal, lResData, strErrNote, strRes, bNaNAllowedEl)

            # size restrictions
            elif (strRes == 'size equal to' or \
                  strRes == 'size higher than' or \
                  strRes == 'size higher or equal to' or \
                  strRes == 'lower than' or \
                  strRes == 'lower or equal to'):
                  self.__checkSiz(strParName, strDesc, parVal, strRefName, refVal, lResData, strErrNote, strRes)            
            
            # the number of dimensions 
            elif (strRes == 'number of dimensions equal to' or \
                  strRes == 'number of dimensions higher than' or \
                  strRes == 'number of dimensions higher or equal to' or \
                  strRes == 'number of dimensions lower than' or \
                  strRes == 'number of dimensions lower or equal to'):
                  self.__checkNDim(strParName, strDesc, parVal, strRefName, refVal, lResData, strErrNote, strRes)

            # size of restrictions
            elif (strRes == 'dimension size equal to' or \
                  strRes == 'dimension size higher than' or \
                  strRes == 'dimension size lower than' or \
                  strRes == 'dimension size higher or equal to' or \
                  strRes == 'dimension size lower or equal to'):
                  self.__checkDimSiz(strParName, strDesc, parVal, strRefName, refVal, lResData, strErrNote, strRes)

            # unknown restrictions            
            else:
                raise RuntimeError('Unknown parameter restriction. Something went seriously wrong...[internal RxCSobject error]')


    def __checkAllowedVal(self, strParName, strDesc, parVal, lAllVal, strErrNote, bNaNAllowedEl):
        """
            Function checks the 'allowed values' restriction of a parameter.

            Arguments:
                    strParName: [string]        name of a parameter
                    strDesc:    [string]        description of a parameter
                    parVal:                     value of the parameter to be checked
                    lAllVal     [list]          list with allowed values 
                    strErrNote  [string]        error note to be displayed if the restriction is broken
                                                (might be empty, then a default note is generated)
                    bNaNAllowed [number]        'NaN' elements allowed flag
                    
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """

        # -------------------------------------------------------------------
        # Error check
        if not isinstance(parVal, (float, int, str, tuple, list, np.ndarray)):
            strError = 'Only numbers, strings, tuples, lists, and numpy arrays can be restricted with allowed values!'
            strError = strError+'(>%s< is of type: %s)' % (strParName, type(parVal))
            raise ValueError(strError)
        # -------------------------------------------------------------------

        # Run the correct function dependently on the parameter type
        if isinstance(parVal, (str, float, int)):
            self.__checkAllowedVal_numstr(strParName, strDesc, parVal, lAllVal, strErrNote)
        else:
            self.__checkAllowedVal_atl(strParName, strDesc, parVal, lAllVal, strErrNote, bNaNAllowedEl)
        return


    def __checkAllowedVal_numstr(self, strParName, strDesc, parVal, lAllVal, strErrNote):
        """
            Function checks the 'allowed values' restriction of number and string parameters.

            Arguments:
                    strParName: [string]        name of a parameter
                    strDesc:    [string]        description of a parameter
                    parVal:                     value of the parameter to be checked
                    lAllVal     [list]          list with allowed values 
                    strErrNote  [string]        error note to be displayed if the restriction is broken
                                                (might be empty, then a default note is generated)
                    
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    11 june 2015
        """
        inxAl = 0  # Reset the index of elements in a list with allowed values

        # Loop over all elements of a list with allowed values
        for allVal in lAllVal:

            # An allowed value must be either a string or a number            
            if not isinstance(allVal, (str, float, int)):
                strError = 'List of allowed values must contain only strings or numbers!\n'
                strError = strError+'            An allowed value #%d for the parameter > %s < (\'%s\') is of type %s' \
                    % (inxAl, strParName, strDesc, type(allVal))
                raise ValueError(strError)

            # If an allowed value is NaN, throw out an error! 
            if isinstance(allVal, float):
                if np.isnan(allVal):
                    strError = 'NaN can not be an allowed value for the parameter > %s < (\'%s\')' % (strParName, strDesc)
                    raise ValueError(strError)
            
            # If an allowed value was found, return from the function             
            if (parVal == allVal):
                return

        # Allowed value was not found, throw out an error
        if (strErrNote == ''):            
            if isinstance(parVal, (int, float)):
                strErrNote = ('\'%s\' is an incorrect value for parameter > %s < (\'%s\')') % (self.__n2s(parVal), strParName, strDesc)
            elif isinstance(parVal, (str)):
                strErrNote = ('\'%s\' is an incorrect value for parameter > %s < (\'%s\')') % (parVal, strParName, strDesc)
        raise AllowedValuesError(strErrNote)


    def __checkAllowedVal_atl(self, strParName, strDesc, parVal, lAllVal, strErrNote, bNaNAllowedEl):
        """
            Function checks the 'allowed values' restriction for Numpy arrays, tuples and lists.

            Arguments:
                    strParName: [string]        name of a parameter
                    strDesc:    [string]        description of a parameter
                    parVal:                     value of the parameter to be checked
                    lAllVal     [list]          list with allowed values 
                    strErrNote  [string]        error note to be displayed if the restriction is broken
                                                (might be empty, then a default note is generated)
                    bNaNAllowed [number]        'NaN' elements allowed flag
                    
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """
        
        inxEl = 0  # Reset the index of elements in tuple, list or a numpy array

        # Vectorize the parameter, if it is a numpy array
        if isinstance(parVal, np.ndarray):
            parVal.shape = (parVal.size, )

        # Check if a list of allowed values contains correct elements (string and non-NaN numbers) 
        inxAl = 0  # Reset the index of elements in a list with allowed values
        bErr = 1   # Set error flag 
        for allVal in lAllVal:       # Loop over all elements of a list with allowed values

            # An allowed value must be either a string or a number            
            if not isinstance(allVal, (str, float, int)):
                strError = 'List of allowed values must contain only strings or numbers!\n'
                strError = strError+'            An allowed value #%d for the parameter > %s < (\'%s\') is of type %s' \
                    % (inxAl, strParName, strDesc, type(allVal))
                raise ValueError(strError)
                                
            # If an allowed value is NaN, throw out an error!     
            if isinstance(allVal, float):
                if np.isnan(allVal):
                    strError = 'NaN can not be an allowed value for the parameter > %s < (\'%s\')' % (strParName, strDesc)
                    raise ValueError(strError)
        
        # Loop over all elements of the parameter
        for par in parVal:
            
            # An element of the tested parameter must be either a string or a number            
            if not isinstance(par, (str, float, int)):
                strError = 'Only number or string elements can be restricted with allowed values!\n'
                strError = strError+'            Element #%d of > %s < (%s) is of type %s' \
                    % (inxEl, strParName, strDesc, type(par))
                raise ValueError(strError)

            # If an element if NaN, then decide what to do
            if isinstance(par, float):
                if np.isnan(par):
                    if bNaNAllowedEl:
                        continue
                    else:
                        strError = 'Element %d of > %s < (%s) is NaN, which is not allowed!' \
                            % (inxEl, strParName, strDesc)
                        raise ValueError(strError)

            # Loop over all elements of a list with allowed values
            inxAl = 0  # Reset the index of elements in a list with allowed values
            bErr = 1   # Set error flag 
            for allVal in lAllVal:       
                
                # If an allowed value was found, clear the error flag, break the loop and go to the next element             
                if (par == allVal):
                    bErr = 0
                    break

                inxAl = inxAl + 1     # Index of an element in the list with allowed values     
            
            # If error flag is cleared, go to the next element of the tested parameter
            if (bErr == 0):
                inxEl = inxEl + 1     # Index of an element in the tested parameter 
                continue
            
            # Allowed value was not found, throw out an error
            if (strErrNote == ''):            
                if isinstance(par, (int, float)):
                    strErrNote = ('%s is an incorrect value for element #%d of parameter > %s < (\'%s\')') \
                        % (self.__n2s(par), inxEl, strParName, strDesc)
                elif isinstance(par, (str)):
                    strErrNote = ('%s is an incorrect value for element #%d of parameter > %s < (\'%s\')') \
                        % (par, inxEl, strParName, strDesc)
            raise AllowedValuesError(strErrNote)
        return


    def __checkRelVal(self, strParName, strDesc, parVal, strReference, refVal, lCoef, strErrNote, strRelation, bNaNAllowedEl):
        """
            Function checks relative value restriction of a parameter.

            Arguments:                    
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    parVal:                       parameter to be checked
                    strRefence    [string]        name of a reference
                    refVal                        reference
                    lCoef         [list]          list with 'mul' and 'add' coefficients 
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then a default note is generated)
                    strRelation   [string]        relation, allowed values: 
                                                  'higher than', 'higher or equal to', 'lower than', 'lower or equal to'
                    bNaNAllowed [number]          'NaN' elements allowed flag
                                        
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    2 june 2015
        """

        # -------------------------------------------------------------------
        # Error check
        if not isinstance(parVal, (float, int, tuple, list, np.ndarray)):
            strError = 'Only numbers, lists, tuples and numpy arrays can be restricted \'%s...\'! '  % (strRelation)
            strError = strError+'            (>%s< is of type: %s)' % (strParName, type(parVal))
            raise ValueError(strError)

        # -------------------------------------------------------------------

        # Switch to correct function dependently on type of the parameter:
        if isinstance(parVal, (float, int)):
            self.__checkRelVal_num(strParName, strDesc, parVal, strReference, refVal, lCoef, strErrNote, strRelation)
        else:
            self.__checkRelVal_atl(strParName, strDesc, parVal, strReference, refVal, lCoef, strErrNote, strRelation, bNaNAllowedEl)

        return

        # -------------------------------------------------------------------


    def __checkRelVal_num(self, strParName, strDesc, parVal, strReference, refVal, lCoef, strErrNote, strRelation):
        """
            Function checks relative value restriction of a number parameter.

            Arguments:                    
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    parVal:                       parameter to be checked
                    strRefence    [string]        name of a reference
                    refVal                        reference
                    lCoef         [list]          list with 'mul' and 'add' coefficients 
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then a default note is generated)
                    strRelation   [string]        relation, allowed values: 
                                                  'higher than', 'higher or equal to', 'lower than', 'lower or equal to'
                                        
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    2 june 2015
        """

        # Only numbers can be a reference
        if not isinstance(refVal, (float, int)):
            strError = 'Only numbers can be a reference for restriction \'%s...\' for numbers!\n' % (strRelation)
            strError = strError+'                 (> %s < is of type: %s)' % (strReference, type(refVal))
            raise ValueError(strError)
        
        # If reference is NaN, restriction can not be checked, it is assumed that the value is correct
        if isinstance(refVal, float):
            if np.isnan(refVal):
                return

        # Check the restriction, if it is ok, return
        if (self.__checkRelVal_engine(parVal, refVal, lCoef, strRelation)):
            return
 
        # Throw out an error
        if strErrNote == '':
            (strMul, strAdd) = self.__linearCoef2Strings(lCoef)       
            strErrNote = '%s > %s < must be %s %s %s %s!' \
                % (strDesc, strParName, strRelation, strMul, strReference, strAdd)
        raise RelationalError(strErrNote)


    def __checkRelVal_atl(self, strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRelation, bNaNAllowedEl):
        """
            Function checks the relative value restriction for Numpy arrays, tuples or lists.
            
            Arguments:                    
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    parVal:                       parameter to be checked
                    strRefence    [string]        name of a reference
                    refVal                        reference
                    lCoef         [list]          list with 'mul' and 'add' coefficients 
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then a default note is generated)
                    strRelation   [string]        relation, allowed values: 
                                                  'higher than', 'higher or equal to', 'lower than', 'lower or equal to'
                    bNaNAllowed   [number]        'NaN' elements allowed flag

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    2 june 2015
        """

        # If reference is a NaN, number it can not be used as a reference, return from function
        if isinstance(refVal, float):
            if np.isnan(refVal):
                return

        # Take the length of the parameter
        iLen = self.__checkRelVal_atl_parLen(self, parVal)

        # Take the length of the reference
        iLenRef = self.__checkRelVal_atl_refTypeLen(refVal, strRefName, strRelation)

        # Check the lengths of the parameter and the reference.
        # These lenghts must be the identical.
        self.__checkRelVal_atl_lenParRef(strParName, refVal, strRefName, iLen, iLenRef)

        # Vectorize the parameter and the reference
        (parVal, refVal) = self.__checRelVal_atl_vectorize(parVal, refVal)      
           
        # Check the restriction:
        if isinstance(refVal, (int, float)):        
            # Check for number reference
            self.__checkRelVal_atl_refNum(strParName, strDesc, parVal, strRefName, refVal, lCoef, 
                                          strErrNote, strRelation, bNaNAllowedEl)

        else:              
            # Check for tuple, list, numpy array reference
            self.__checkRelVal_atl_refAtl(strParName, strDesc, parVal, strRefName, refVal, lCoef, 
                                          strErrNote, strRelation, bNaNAllowedEl)
        
        return


    def __checkRelVal_atl_parLen(self, parVal):

        # Take the lenght of the checked parameter        
        if isinstance(parVal, np.ndarray):
            iLen = parVal.size
        else:
            iLen = len(parVal)

        return iLen


    def __checkRelVal_atl_refLen(self, refVal, strRefName, strRelation):

        # Take the lenght of the  reference

        # Reference is a tuple or a list
        if isinstance(refVal, tuple, list):
            iLenRef = len(refVal)
              
        # Reference is a Numpy array    
        elif isinstance(refVal, np.ndarray):
            iLenRef = refVal.size
            
        # Reference is a number
        elif isinstance(refVal, (float, int)):
            iLenRef = 1
        
        # Reference has illegal type
        else:
            strError = 'Only numbers, lists, tuples and numpy arrays can be a reference for restriction \'%s...\'!\n' \
                % (strRelation)
            strError = strError+'       (>%s< is of type: %s)' % (strRefName, type(refVal))
            raise ValueError(strError)
        
        return iLenRef


    def __checRelVal_atl_vectorize(self, parVal, refVal):
        
        # Vectorize the parameter, if it is a numpy array
        if isinstance(parVal, np.ndarray):
            parVal.shape = (parVal.size, )

        # Vectorize the reference, if it is a numpy array
        if isinstance(refVal, np.ndarray):
            refVal.shape = (refVal.size, )
        
        return (parVal, refVal)

        
    def __checkRelVal_atl_refNum(self, strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRelation, bNaNAllowedEl):
        
            # Loop over all elements in the checked parameter             
            for inxEl in range(len(parVal)):
                
                # Get the current element of the checked parameter and                                 
                parEl = parVal[inxEl]

                # Check if an element is a number
                if not isinstance(parEl, (float, int)):
                    self.__checkRelVal_atl_PET_error(strParName, strRelation, inxEl, parEl)

                # Check if the current elements of the checked parameter is NaN
                if isinstance(parEl, float):
                    if np.isnan(parEl):
                        if (bNaNAllowedEl == 1):
                            continue
                        else:
                            strError = 'Element %d of > %s < (%s) is NaN, which is not allowed!' \
                                % (inxEl, strParName, strDesc)
                            raise ValueError(strError)
                            
                # Check the reference
                if not (self.__checkRelVal_engine(parEl, refVal, lCoef, strRelation)):
                    self.__checkRelVal_atl_error(strParName, strDesc, parVal, strRefName, refVal, lCoef, 
                                                 strErrNote, strRelation, inxEl)


    def __checkRelVal_atl_refAtl(self, strParName, strDesc, parVal, strRefName, refVal, 
                                 lCoef, strErrNote, strRelation, bNaNAllowedEl):

            # Loop over all elements in the checked parameter             
            for inxEl in range(len(parVal)):

                # ---------------------------------------------------------------------------------                
                # Get the current element of the checked parameter and check if it is a number                
                parEl = parVal[inxEl]
                
                # Check if the current element is a number
                if not isinstance(parEl, (float, int)):                        
                    self.__checkRelVal_atl_PET_error(strParName, strRelation, inxEl, parEl)

                # Check if the current elements of the checked parameter is NaN
                if isinstance(parEl, float):
                    if np.isnan(parEl):
                        if (bNaNAllowedEl == 1):
                            continue
                        else:
                            strError = 'Element %d of > %s < (%s) is NaN, which is not allowed!' \
                                % (inxEl, strParName, strDesc)
                            raise ValueError(strError)
                            
                # ---------------------------------------------------------------------------------

                # Get the current element of the reference                                                
                refEl = refVal[inxEl]
                
                # Check if the reference is a number
                if not isinstance(refEl, (float, int)):                        
                    self.__checkRelVal_atl_RET_error(strParName, strRefName, strRelation, inxEl, refEl)                
                
                # Check if the reference element is NaN. If it is, continue
                if isinstance(refEl, float):
                    if np.isnan(refEl):
                        continue

                # ---------------------------------------------------------------------------------

                # Check the relation between the element and the reference
                if not (self.__checkRelVal_engine(parEl,refEl, lCoef, strRelation)):
                    self.__checkRelVal_atl_error(strParName, strDesc, parVal, strRefName, refVal, lCoef, 
                                                 strErrNote, strRelation, inxEl)

    
    def __checkRelVal_atl_PET_error(self, strParName, strRelation, inxEl, parEl):

        # Throw the error of parameter element type , if it was found above
        strError = 'Only numbers can be checked for restriction  \'%s...\'!\n'  % (strRelation)
        strError = strError+'            Element #%d of > %s < is of type %s!' % (inxEl, strParName, type(parEl))
        raise ValueError(strError)

    
    def __checkRelVal_atl_RET_error(self, strParName, strRefName, strRelation, inxEl, refEl):

        # Throw the error of reference parameter element type , if it was found above
        strError = 'Only numbers can be a reference for restriction  \'%s...\'!\n'  % (strRelation)
        strError = strError+'            Element #%d of %s (reference for > %s< ) is of type %s!' \
            % (inxEl, strRefName, strParName, type(refEl))
        raise ValueError(strError)


    def __checkRelVal_atl_lenParRef(self, strParName, refVal, strRefName, iLen, iLenRef):

        # Compare the lenghts with the lenght of the reference, if the reference is a list, a tuple or a numpy array
        if isinstance(refVal, (list, tuple, np.ndarray)):
            if not (iLen == iLenRef):
                strError = 'Reference must be of equal size to the restricted parameter!\n'
                strError = strError+'            Parameter > %s < is of size %d, its reference (%s) is of size %d!' \
                    % (strParName, iLen, strRefName, len(refVal))
                raise ValueError(strError)


    def __checkRelVal_atl_error(self, strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRelation, inxElErr, strDelimStart, strDelimLast, inxEl):

        # Throw out an error, if the error note was already given            
        if not (strErrNote == ''):
            raise RelationalError(strErrNote)

        # Construct the error note:

        # Firstly, change linear coefficients into strings
        (strMul, strAdd) = self.__linearCoef2Strings(lCoef)

        # If the reference is a number it is easy to construct the error info... 
        if isinstance(refVal, (int, float)):
            strErrNote = 'All elements of %s > %s < must be %s %s %s %s! (error on element # %d)!' \
                % (strDesc, strParName, strRelation, strMul, strRefName, strAdd, inxElErr)
            raise RelationalError(strErrNote)

        # If the reference is an array, a tuple or a list, it is getting complicated... 
        if (strMul == '') and (strAdd == ''):
            strErrNote = 'Elements of > %s < (%s) must be %s the corresponding elements of %s' \
                % (strParName, strDesc, strRelation, strRefName)
        else:
            strErrNote = 'Elements of > %s < (%s) must be %s %s x %s, where x are the corresponding elements of %s' \
                % (strParName, strDesc, strRelation, strMul, strAdd, strRefName)
        
        # Print the reference if its size is lower than 10
        if (len(refVal) <= 10):
            self.__checkRelVal_atl_refDelim(refVal)
            strErrNote = strErrNote + ' %s' % strDelimStart
            for el in refVal:
                strErrNote = strErrNote + ' %s' % self.__n2s(el)
            strErrNote =  strErrNote + ' %s' % strDelimLast
            strErrNote = strErrNote + '!\n'

        # Add info about the element which brakes the restriction
        strErrNote=strErrNote+'            Element #%d of > %s < is %s, element #%d of %s is %s!' \
            % (inxEl, strParName, self.__n2s(parVal[inxEl]), inxEl, strRefName, self.__n2s(refVal[inxEl]))
        
        # Ok, error is ready, throw out an error            
        raise RelationalError(strErrNote)


    def __checkRelVal_atl_refDelim(self, refVal):
 
        # Reference is a tuple
        if isinstance(refVal, (tuple)):
            strDelimStart = '('
            strDelimLast = ')'

        # Reference is a list or a Numpy array
        elif isinstance(refVal, (list, np.ndarray)):
            strDelimStart = '['
            strDelimLast = ']'

        # Reference is a number
        elif isinstance(refVal, (float, int)):
            strDelimStart = ''
            strDelimLast = ''
        
        return (strDelimStart, strDelimLast)


    def __checkRelVal_engine(self, iPar, iRef, lCoef, strRelation):
        """
            Engine of value relational restriction check.

            Arguments:                    
                    iPar:        [number]       tested parameter
                    iRef:        [number]       reference
                    lCoef        [list]         list with linear coefficients
                    strRelation  [string]       relation, allowed values: 
                                                'higher than', 'higher or equal to', 
                                                'lower than', 'lower or equal to', 
            Output:
                    1 - restriction correct
                    0 - restriction incorrect

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    2 june 2015
        """
        iMul = lCoef[0]
        iAdd = lCoef[1]
        iRef = iMul * iRef + iAdd
        
        if (strRelation == 'higher than'):
            return (iPar > iRef)
        elif (strRelation == 'higher or equal to'):        
            return (iPar >= iRef)
        elif (strRelation == 'lower than'):
            return (iPar < iRef)
        elif (strRelation == 'lower or equal to'):
            return (iPar <= iRef)
        else:
            strError = '%s is an unknown type of a relation!' % strRelation
            raise RuntimeError(strError)


    def __checkSiz(self, strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRes):
        """
            Function checks the size restrictions of a parameter.

            Arguments:
                    strParName:   [string]        name of the parameter
                    strDesc:      [string]        description of the parameter
                    parVal:                       parameter to be checked
                    strRefName    [string]        name of a reference
                    refVal                        reference
                    lCoef         [list]          list with 'mul' and 'add' coefficients 
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then a default note is generated)
                    strRes        [string]        restriction, allowed values: 
                                                  'size equal to', 'size higher than', 'size higher or equal to', 
                                                  'size lower than', 'size lower or equal to'
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    10 june 2015
        """

        # Take the size of the tested parameter
        iSize = self.__checkSiz_sizParam(parVal, strParName)
        
        # Take the reference size
        iRefSize = self.__checkSiz_sizRef(strParName, refVal, strRefName, strRes)
        
        # Check the restriction, if it is ok, return
        if not self.__checkSiz_engine(iSize, iRefSize, lCoef, strRes):
            self.__checkSiz_error(strParName, strDesc, strRefName, refVal, lCoef, strErrNote, strRes, iSize)

        return


    def __checkSiz_sizParam(self, parVal, strParName):
        """
            Function gets the size of a restricted parameter.

            Arguments:
                    parVal:                       the parameter to be checked                    
                    strParName:   [string]        name of the parameter

            Output:
                    iSize:        [number]        size of the parameter to be checked

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015        
        """
        # Size of numbers is always one
        if isinstance(parVal, (int, float)):
            iSize = 1
            
        # Size of tuples, lists and strings             
        elif isinstance(parVal, (tuple, list, str)):
            iSize = len(parVal)
        
        # Size of Numpy arrays
        elif isinstance(parVal, np.ndarray):
            iSize = parVal.size
        
        # Error
        else:
            strError = 'Only numbers, strings, tuples, lists, and numpy arrays can be size restricted!\n'
            strError = strError+'            ( > %s < is of type: %s )' % (strParName, type(parVal))
            raise ValueError(strError)
        return iSize


    def __checkSiz_sizRef(self, strParName, refVal, strRefName, strRes):
        """
            Function gets a reference for a size restriction.

            Arguments:                    
                    strParName:   [string]        name of a checked parameter
                    refVal                        reference
                    strRefName    [string]        name of the reference
                    strRes        [string]        restriction, allowed values: 
                                                  'size equal to', 'size higher than', 'size higher or equal to', 
                                                  'size lower than', 'size lower or equal to'
            Output:
                    iRefSize:     [number]        the reference of size restrictions

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015        
        """

        # Reference can not be empty
        if (strRefName == '> (empty) <'):
            strError = ('Reference for size restriction of > %s < is empty!') % (strParName)
            raise ValueError(strError)

        # Reference is a number
        if isinstance(refVal, (int, float)):
            iRefSize = refVal
            
            # Size can not be equal to a float number            
            if isinstance(refVal, float) and (strRes == 'size equal to'):
                strError = ('Float number can not be a reference for restriction \'size equal to\'!\n')
                strError = strError + '            %s (reference for > %s < ) is of type %s' \
                    % (strRefName, strParName, type(refVal))
                raise ValueError(strError) 
        
        # Reference is a tuple, a list or a string
        elif isinstance(refVal, (tuple, list, str)):
            iRefSize = len(refVal)
        
        # Reference is a Numpy array
        elif isinstance(refVal, np.ndarray):
            iRefSize = refVal.size
        
        # Error        
        else:
            strError = 'Only numbers, strings, tuples, lists, and numpy arrays can be a reference for size restriction!'
            strError = strError + '                        %s (restriction for > %s < ) is of type: %s)' \
                % (strRefName, strParName, type(refVal))
            raise ValueError(strError)
        
        return iRefSize


    def __checkSiz_engine(self, iSize, iRefSize, lCoef, strRelation):
        """
            Engine of size restriction check.

            Arguments:                    
                    iSize:        [number]        size of a parameter
                    iRefSize:     [number]        reference for size restriction
                    lCoef         [list]          list with 'mul' and 'add' coefficients
                    strRelation   [string]        restriction, allowed values: 
                                                  'size higher than', 'size higher or equal to', 
                                                  'size lower than', 'size lower or equal to', 
                                                  'size equal to'
            Output:
                    1 - restriction correct
                    0 - restriction incorrect

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    2 june 2015
        """

        iMul = lCoef[0]     # Take the linear coefficients
        iAdd = lCoef[1]     # Take the linear coefficients

        iRefSize = iMul*iRefSize+iAdd  # Apply the linear coefficients
        
        if (strRelation == 'size higher than'):
            return (iSize > iRefSize)
        elif (strRelation == 'size higher or equal to'):        
            return (iSize >= iRefSize)
        elif (strRelation == 'size lower than'):
            return (iSize < iRefSize)
        elif (strRelation == 'size lower or equal to'):
            return (iSize <= iRefSize)
        elif (strRelation == 'size equal to'):
           return (iSize == iRefSize)
        else:
            strError = '%s is an unknown type of a relation!' % strRelation
            raise RuntimeError(strError)


    def __checkSiz_error(self, strParName, strDesc, strRefName, refVal, lCoef, strErrNote, strRes, iSize):
        """
            Function raises a size restriction error.

            Arguments:                    
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of the parameter
                    strRefName    [string]        name of the reference
                    refVal                        reference
                    lCoef         [list]          list with 'mul' and 'add' coefficients 
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then the default note is generated)
                    strRes        [string]        restriction, allowed values: 
                                                  'size equal to', 'size higher than', 'size higher or equal to', 
                                                  'size lower than', 'size lower or equal to'
                    iSize         [number]        size of the parameter which was checked

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015        
        """
        
        # If error note was given, use it
        if not strErrNote == '':
            raise ValueError(strErrNote)
        
        # Change linear coefficients into strings
        (strMul, strAdd) = self.__linearCoef2Strings(lCoef)

        # Construct the error message:        
        if isinstance(refVal, (int, float)):
            strError = ('Parameter > %s < (%s) must have %s value of %s %s %s (%s%s%s)!\n') \
                % (strParName, strDesc, strRes, strMul, strRefName, strAdd, strMul, self.__n2s(refVal), strAdd)
        else:
            strError = ('Parameter > %s < (%s) must have %s %ssize of %s %s!\n') \
                % (strParName, strDesc, strRes, strMul, strRefName, strAdd) 
        strError = strError + '            Current size of parameter > %s < is %d!' % (strParName, iSize)        
        raise ValueError(strError)


    def __checkNDim(self, strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRes):
        """
            Function checks restrictions imposed on the number of dimensions of a parameter.

            Arguments:                    
                    strParName:   [string]        name of the parameter
                    strDesc:      [string]        description of the parameter
                    parVal:                       parameter to be checked
                    strRefName    [string]        name of a reference
                    refVal                        reference
                    lCoef         [list]          list with 'mul' and 'add' coefficients 
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then a default note is generated)
                    strRes        [string]        restriction, allowed values:
                                                  'number of dimensions equal to', 'number of dimensions higher than', 
                                                  'number of dimensions higher or equal to', 'number of dimensions lower than', 
                                                   'number of dimensions lower or equal to'
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015
        """

        # Take the number of dimensions of the tested parameter
        iNDim = self.__checkNDim_NDimInParam(strParName, parVal)

        # Take the number of dimensions in the reference
        iRefNDim = self.__checkNDim_NDimInRef(strParName, refVal, strRefName, strRes)
        
        # Check the restriction, if it is ok, return
        if not self.__checkNDim_engine(iNDim, iRefNDim, lCoef, strRes):
            self.__checkNDim_error(strParName, strDesc, strRefName, refVal, lCoef, strErrNote, strRes, iNDim, iRefNDim)
        return


    def __checkNDim_NDimInParam(self, strParName, parVal):
        """
            Function gets the number of dimensions in a tested parameter.

            Arguments:                    
                    strParName:   [string]        name of athe parameter
                    parVal:                       the parameter to be checked

            Output:
                    iNDim:        [number]        the number of dimensions 
                                                  in a tested parameter

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015
        """

        # Parameter is a number, tuple, list or string        
        if isinstance(parVal, (int, float, tuple, list, str)):
            iNDim = 1            
        
        # Parameter is a Numpy array       
        elif isinstance(parVal, np.ndarray):
            iNDim = parVal.ndim
        
        # illegal type of a tested parameter  
        else:
            strError = 'Only numbers, strings, tuples, lists, and numpy arrays can be restricted for the number of dimensions!\n'
            strError = strError+'            ( > %s < is of type: %s )' % (strParName, type(parVal))
            raise ValueError(strError)
        return iNDim


    def __checkNDim_NDimInRef(self, strParName, refVal, strRefName, strRes):
        """
            Function gets the number of dimensions in a reference for the restriction imposed on the number of dimensions.

            Arguments:                    
                    strParName:   [string]        name of a parameter
                    refVal:                       reference to a parameter
                    strRefName    [string]        name of a reference
                    strRes        [string]        restriction, allowed values: 
                                                  'number of dimensions equal to', 'number of dimensions higher than', 
                                                  'number of dimensions higher or equal to', 'number of dimensions lower than', 
                                                  'number of dimensions lower or equal to'

            Output:
                    iRefNDim:     [number]        reference for restriction 

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015
        """
        
        # Reference can not be empty
        if (strRefName == '> (empty) <'):
            strError = ('Reference for restriction of the number of dimensions of > %s < is empty!') % (strParName)
            raise ValueError(strError)

        # Restriction is a number
        if isinstance(refVal, (int, float)):
            iRefNDim = refVal
            if isinstance(refVal, float) and (strRes == 'no. of dimensions equal to'):
                strError = ('Float number can not be a reference for restriction \'%s\'!\n') \
                    % (strRes)
                strError = strError + '            %s (reference for > %s < ) is of type %s' \
                    % (strRefName, strParName, type(refVal))
                raise ValueError(strError)
                
        # Restriction is a tuple, a list or a string
        elif isinstance(refVal, (tuple, list, str)):
            iRefNDim = 1
            
        # Restriction is a Numpy array
        elif isinstance(refVal, np.ndarray):
            iRefNDim = refVal.ndim
            
        # Illegal type of restriction
        else:
            strError = 'Only numbers, strings, tuples, lists, and numpy arrays can be a reference for restriction of the number of dimensions!'
            strError = strError + '                        %s (restriction for > %s < ) is of type: %s)' \
                % (strRefName, strParName, type(refVal))
            raise ValueError(strError)
        return iRefNDim


    def __checkNDim_engine(self, iNDim, iRefNDim, lCoef, strRes):
        """
            Engine of 'the number of dimensions' restriction check.

            Arguments:                    
                    iNDim:        [number]        the number of dimensions in a parameter
                    iRefNDim:     [number]        reference
                    lCoef         [list]          list with 'mul' and 'add' coefficients
                    strRes        [string]        restriction, allowed values: 
                                                  'number of dimensions equal to', 'number of dimensions higher than', 
                                                  'number of dimensions higher or equal to', 'number of dimensions lower than', 
                                                  'number of dimensions lower or equal to'
            Output:
                    1 - restriction correct
                    0 - restriction incorrect

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015
        """
        iMul = lCoef[0]     # Take the linear coefficients
        iAdd = lCoef[1]     # 
        iRefNDim = iMul * iRefNDim + iAdd  # Apply the linear coefficients        
        
        if (strRes == 'number of dimensions equal to'):
            return (iNDim == iRefNDim)
        elif (strRes == 'number of dimensions higher than'):        
            return (iNDim > iRefNDim)
        elif (strRes == 'number of dimensions higher or equal to'):
            return (iNDim >= iRefNDim)
        elif (strRes == 'number of dimensions lower than'):
            return (iNDim < iRefNDim)
        elif (strRes == 'number of dimensions lower or equal to'):
            return (iNDim <= iRefNDim)
        else:
            strError = '%s is an unknown type of a relation!' % strRes
            raise RuntimeError(strError)


    def __checkNDim_error(self, strParName, strDesc, strRefName, refVal, lCoef, strErrNote, strRes, iNDim, iRefNDim):
        """
            Function raises an error if the restriction on the number of dimensions was broken.

            Arguments:                    
                    strParName:   [string]        name of the parameter which was checked
                    strDesc:      [string]        description of the parameter
                    strRefName    [string]        name of a reference
                    refVal                        value of the reference
                    lCoef         [list]          list with 'mul' and 'add' coefficients 
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then a default note is generated)
                    strRes        [string]        restriction, allowed values: 
                                                  'number of dimensions equal to', 'number of dimensions higher than', 
                                                  'number of dimensions higher or equal to', 'number of dimensions lower than', 
                                                  'number of dimensions lower or equal to'
                    iNDim         [number]        the number of dimensions in the parameter which was checked
                    iRefNDim      [number]        reference

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015        
        """

        # If error note was given, use it
        if not (strErrNote == ''):
            raise ValueError(strErrNote)

        # Construct the error message:        

        # Change linear coefficients into strings
        (strMul, strAdd) = self.__linearCoef2Strings(lCoef)

        # Reference was a number
        if isinstance(refVal, (int, float)):
            strError = ('Parameter > %s < (%s) must have the %s \n') \
                % (strParName, strDesc, strRes)
            strError = strError + ('            a value of %s %s %s (%s%s%s)!\n') \
                % (strMul, strRefName, strAdd, strMul, self.__n2s(refVal), strAdd)                
            strError = strError + '            The number of dimensions of parameter > %s < is %d!' % (strParName, iNDim)

        # reference was not a number
        else:
            strError = ('Parameter > %s < (%s) must have the %s\n') \
                % (strParName, strDesc, strRes,) 
            strError = strError + ('            %s the number of dimensions of %s %s!\n') \
                % (strMul, strRefName, strAdd) 
            strError = strError + '            The number of dimensions of parameter > %s < is %d!\n' % (strParName, iNDim)
            strError = strError + '            The number of dimensions of parameter %s is %d!' % (strRefName, iRefNDim)
        
        raise ValueError(strError)


    def __checkDimSiz(self, strParName, strDesc, parVal, strRefName, refVal, lResData, strErrNote, strRes):
        """
            Function checks restriction imposed on the size of a dimension of a parameter.

            Arguments:         
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of the parameter
                    parVal:                       the parameter to be checked
                    strRefName    [string]        name of a reference
                    refVal                        reference
                    lResData      [list]          list with auxiliary data for the restriction 
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then a default note is generated)
                    strRes        [string]        restriction, allowed values:
                                                  'dimension size equal to', 'dimension size higher than',
                                                  'dimension size lower than', 'dimension size higher or equal to',
                                                  'dimension size lower or equal to'
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015
        """

        # Take the dimensions indices and 'pedantic' flag
        (iDim, iRefDim, bPedantic) = self.__checkDimSiz_dimensions(lResData)
        
        # Take the size of restricted dimension of the tested parameter
        iDimSize = self.__checkDimSiz_dimSizInParam(parVal, iDim, bPedantic, strParName, strDesc)
        
        # Take the size of dimension in reference
        iRefDimSize = self.__checkDimSiz_dimSizInRef(strParName, strDesc,iDim, refVal, strRefName, iRefDim, bPedantic,  strRes)

        # Check the restriction 
        if not self.__checkDimSiz_engine(iDimSize, iRefDimSize, lResData, strRes):
            self.__checkDimSiz_error(strParName, strDesc, strRefName, refVal, lResData, strErrNote, strRes, iDimSize, iRefDimSize)
        return


    def __checkDimSiz_dimensions(self, lResData):
        """
            Function return indices of dimensions to be checked and 'pedantic' flag.
             
            Arguments:
                    lResData      [list]          list with auxiliary data for the restriction

            Output:
                    iDim          [number]        index of dimension to be checked 
                    iRefDim       [number]        index of reference dimension
                    bPedantic     [number]        'pedantic' flag

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015
        """
                
        # Take the dimensions indices and 'pedantic' flag
        iDim = lResData[2]        # Dimension index of a tested parameter
        iRefDim = lResData[3]     # Dimension index of a reference
        if np.isnan(iRefDim):     # If th dimension index of a reference is NaN, 
            iRefDim = iDim        # it must be equal to the dimension index of a tested parameter

        bPedantic = lResData[4]   # 'pedantic' flag
        return (iDim, iRefDim, bPedantic)


    def __checkDimSiz_dimSizInParam(self, parVal, iDim, bPedantic, strParName, strDesc):
        """
            Function gets the size of checked dimension of a tested parameter.
             
            Arguments:
                    parVal:                       the parameter to be checked
                    iDim          [number]        index of a dimension to be checked 
                    bPedantic     [number]        'pedantic' flag
                    strParName:   [string]        name of the parameter to be checked
                    strDesc:      [string]        description of the parameter
                    
            Output:
                    iDimSize      [number]        size of dimension

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015
        """
        
        # Parameter is a number        
        if isinstance(parVal, (int, float)):
            if (iDim == 0):
                iDimSize = 1
            elif (bPedantic==0):
                iDimSize = 1
            else:
                strError = 'Error in size restriction of dimension #%d for parameter > %s < (%s)!\n' % (iDim, strParName, strDesc)                    
                strError = strError+'            Numbers do not have dimension #%d, and I was asked to be pedantic!\n' \
                    % (iDim)
                strError = strError+'            ( > %s < (%s) is of type %s!)' % (strParName, strDesc, type(parVal))
                raise ValueError(strError)
    
        # Parameter is a tuple or a list
        elif isinstance(parVal, (tuple, list)):
            if (iDim == 0):
                iDimSize = len(parVal)
            elif (bPedantic==0):
                iDimSize = 1
            else:
                if isinstance(parVal, tuple):
                    strType = 'Tuples'
                else:
                    strType = 'Lists'
                strError = 'Error in size restriction of dimension #%d for parameter > %s < (%s)!\n' % (iDim, strParName, strDesc)                    
                strError = strError+'            %s do not have dimension #%d, and I was asked to be pedantic!\n' \
                    % (strType, iDim)
                strError = strError+'            ( > %s < (%s) is of type %s!)' % (strParName, strDesc, type(parVal))
                raise ValueError(strError)
            
        # Parameter is a Numpy array
        elif isinstance(parVal, np.ndarray):
            iNDimPar = parVal.ndim  
            if (iDim < iNDimPar):
                iDimSize = parVal.shape[iDim]
            elif (bPedantic==0):
                iDimSize = 1
            else:
                strError = 'Error in size restriction of dimension #%d for parameter > %s < (%s)!\n' % (iDim, strParName, strDesc)                    
                strError = strError+'            Numpy array > %s < (%s) do not have dimension #%d, and I was asked to be pedantic! \n' \
                    % (strParName, strDesc, iDim)
                raise ValueError(strError)
        
        # Illegal type of a parameter        
        else:
            strError = 'Only numbers, tuples, lists, and numpy arrays can have size restricted dimensions!\n'
            strError = strError+'            ( > %s < (%s) is of type: %s )' % (strParName, strDesc, type(parVal))
            raise ValueError(strError)

        return iDimSize


    def __checkDimSiz_dimSizInRef(self, strParName, strDesc, iDim, refVal, strRefName, iRefDim, bPedantic,  strRes):
        """
            Function gets a reference for a restriction imposed on the size of dimension.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    iDim          [number]        index of dimension to be checked 
                    refVal                        reference 
                    strRefName    [string]        name of a reference
                    iRefDim       [number]        index of reference dimension                    
                    bPedantic     [number]        'pedantic' flag
                    strRes        [string]        restriction, allowed values:
                                                  'dimension size equal to', 'dimension size higher than',
                                                  'dimension size lower than', 'dimension size higher or equal to',
                                                  'dimension size lower or equal to'

            Output:
                    iRefDimSize   [number]        reference for a restriction of the size of dimension

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015
        """
        
        # Reference can not be empty
        if (strRefName == '> (empty) <'):
            strError = ('Reference for restriction of #%d dimension size of > %s < (%s) is empty!') % (iDim, strParName, strDesc)
            raise ValueError(strError)

        # Reference is a number
        if isinstance(refVal, (int, float)):
            iRefDimSize = refVal
            if isinstance(refVal, float) and (strRes == 'dimension size equal to'):
                strError = ('Float number can not be a reference for restriction of \'dimension size equal to...\'!\n')
                strError = strError + '            %s (reference for > %s < ) is of type %s' \
                    % (strRefName, strParName, type(refVal))
                raise ValueError(strError) 
                
        # Reference is a tuple or a list
        elif isinstance(refVal, (tuple, list)):
            if (iRefDim == 0):
                iRefDimSize = len(refVal)
            elif (bPedantic==0):
                iRefDimSize = 1
            else:
                strError = 'Error in size restriction of dimension #%d for parameter > %s < (%s)!\n' % (iDim, strParName, strDesc)                    
                strError = strError + '            Reference %s do not have dimension #%d, and I was asked to be pedantic!\n' \
                    % (strRefName, iRefDim)
                strError = strError + '            ( Reference %s for > %s < (%s) is of type %s. )' \
                    % (strRefName, strParName, strDesc, type(refVal))
                raise ValueError(strError)

        # Reference is a Numpy array
        elif isinstance(refVal, np.ndarray):
            iNDimRef = refVal.ndim  
            if (iRefDim < iNDimRef):
                iRefDimSize = refVal.shape[iRefDim]
            elif (bPedantic==0):
                iRefDimSize = 1
            else:
                strError = 'Error in size restriction of dimension #%d for parameter > %s < (%s)!\n' % (iDim, strParName, strDesc)                    
                strError = strError + '            Reference %s do not have dimension #%d, and I was asked to be pedantic!\n' \
                    % (strRefName, iRefDim)
                strError = strError + '            ( Reference %s for > %s < (%s) is of type %s. )' \
                    % (strRefName, strParName, strDesc, type(refVal))
                raise ValueError(strError)
                
        # Illegal type of the reference
        else:
            strError = 'Only numbers, lists, and numpy arrays can be a reference for restriction of size of dimension!\n'
            strError = strError + '            %s (restriction for > %s < ) is of type: %s)' \
                % (strRefName, strParName, type(refVal))
            raise ValueError(strError)
            
        return iRefDimSize


    def __checkDimSiz_engine(self, iDimSize, iRefDimSize, lResData, strRes):
        """
            Engine of check of restriction imposed on size of a dimension.

            Arguments:                    
                    iDimSize:         [number]         size of a dimensions in a checked parameter
                    iRefDimSize:      [number]         reference
                    lResData          [list]           list with 'mul' and 'add' coefficients
                    strRes            [string]         restriction, allowed values: 
                                                       'dimension size equal to', 'dimension size higher than', 
                                                       'dimension size lower than', 'dimension size higher or equal to', 
                                                       'dimension size lower or equal to'
            Output:
                    1 - restriction correct
                    0 - restriction incorrect

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    10 june 2015
        """

        iMul = lResData[0]     # Take the linear coefficients
        iAdd = lResData[1]     # Take the linear coefficients
        
        iRefDimSize = iMul*iRefDimSize+iAdd   # Apply the linear coefficients

        if (strRes == 'dimension size equal to'):
            return (iDimSize == iRefDimSize)
        elif (strRes == 'dimension size higher than'):        
            return (iDimSize > iRefDimSize)
        elif (strRes == 'dimension size lower than'):
            return (iDimSize >= iRefDimSize)
        elif (strRes == 'dimension size higher or equal to'):
            return (iDimSize < iRefDimSize)
        elif (strRes == 'dimension size lower or equal to'):
            return (iDimSize <= iRefDimSize)
        else:
            strError = '%s is an unknown type of a relation!' % strRes
            raise RuntimeError(strError)


    def __checkDimSiz_error(self, strParName, strDesc, strRefName, refVal, lResData, strErrNote, strRes, iDimSize, iRefDimSize):
        """
            Function raises an error if a restriction imposed on the size of dimensions was broken.
            
            Arguments:                    
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    strRefName    [string]        name of a reference
                    refVal                        value of a reference
                    lResData      [list]          list with auxiliary data for the restriction 
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then a default note is generated)
                    strRes        [string]        restriction, allowed values:
                                                  'dimension size equal to', 'dimension size higher than',
                                                  'dimension size lower than', 'dimension size higher or equal to',
                                                  'dimension size lower or equal to'
                    iDimSize      [number]        size of dimension to be checked
                    iRefDimSize   [number]        reference for the restriction

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015        

        """
        # If error note was given, use it 
        if not (strErrNote == ''):
            raise ValueError(strErrNote)

        # If error note was not given, construct the error message:
        iDim = lResData[2]        # Dimension index of a tested parameter
        iRefDim = lResData[3]     # Dimension index of a reference
        if np.isnan(iRefDim):     # If th dimension index of a reference is NaN, 
            iRefDim = iDim        # it must be equal to the dimension index of a tested parameter

        strErrNote = 'Parameter > %s < (%s) must have size of dimension #%d ' \
            % (strParName, strDesc, iDim)
        (strMul, strAdd) = self.__linearCoef2Strings(lResData)
        if (strRes == 'dimension size equal to'):
            strErrNote = strErrNote + 'equal to '
        elif (strRes == 'dimension size higher than'):
            strErrNote = strErrNote + 'higher than '
        elif (strRes == 'dimension size lower than'):
             strErrNote = strErrNote + 'lower than '          
        elif (strRes == 'dimension size higher or equal to'):
             strErrNote = strErrNote + 'higher or equal to '                      
        elif (strRes == 'dimension size lower or equal to'):
             strErrNote = strErrNote + 'lower or equal to '
        strErrNote = strErrNote + '%s\'x\'%s\n' \
            % (strMul, strAdd)
        strErrNote = strErrNote + '            where \'x\' is '
        if isinstance(refVal, (int, float)):
            if strRefName == 'the given number':
                strErrNote = strErrNote + 'equal to the given number (%d)\n' \
                    % (iRefDimSize)
            else:
                strErrNote = strErrNote + 'equal to a value of %s.\n' \
                    % (strRefName)
        else:
            strErrNote = strErrNote + 'is a size of dimension #%d of parameter %s.\n' \
                % (iRefDim, strRefName)
        strErrNote = strErrNote + '            Current size of dimension #%d of > %s < is %d, ' \
            % (iDim, strParName, iDimSize)
        if isinstance(refVal, (int, float)):
            strErrNote = strErrNote + 'current value of %s is %d.\n' \
                % (strRefName, iRefDimSize)
        else:
            strErrNote = strErrNote + 'current size of dimension #%d of %s is %d.\n' \
                % (iRefDim, strRefName, iRefDimSize)
        raise ValueError(strErrNote)


    def __linearCoef2Strings(self, lResData):
        """
            Function changes linear coefficients into strings.

            Arguments:                    
                    lResData      [list]          list with auxiliary data for the restriction 

            Output:
                    strMul        [string]        string with  'mul' parameter 
                    strAdd        [string]        string with  'add' parameter

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    9 june 2015        
            
        """

        iMul = lResData[0]     # Take the linear coefficients
        iAdd = lResData[1]     # Take the linear coefficients

        # Change linear coefficients into strings
        if (iMul == 1):
            strMul = ''
        else:
            strMul = '%s*' % self.__n2s(iMul)
        if (iAdd == 0):
            strAdd = ''
        else:
            strAdd = '+%s' % self.__n2s(iAdd)
    
        return (strMul, strAdd)
    

    def __n2s(self, iX):
        """
            Function changes number to a string.
            It automatically regulates the number of digits after the comma.  
  
            Arguments:
                    iX [number]        number to be changed
                    
            Output:
                    strX [string]      string with a number

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """

        if isinstance(iX, int):
            strX = ('%d') % iX
            return strX
        
        iMaxDigits = 24  # Maximum precision 
        for iPrec in range(1,iMaxDigits+1):
            strFormat = ('%%.%df') % iPrec         # Change the numer to 
            strEval= ('\'%s\' %% iX') % strFormat  # a string
            strX = eval(strEval)                   # ^
            
            iX_ = float(strX)    # Change the string back to the number     
            if (iX_ == iX):      # and check if it is correct      
                return strX      #
        
        # No correct solution was found until the max digits, let the CPU decide         
        strX = ('%f') % iX  
        return strX           
        

    def __NthInTuple(self, iN, tup):
        """
            Function takes Nth element of a tuple.
            It is assumed that the elemnts are indexed starting from 0
  
            Arguments:
                    iN [number]        position in a tuple
                    
            Output:
                    element            Nth element of a tuple

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    29 may 2015
        """

        if (iN < 0):
            strError = ('Index of the wanted element must not be lower than 0!')
            raise ValueError(strError)                        
        if not (len(tup) > iN):
            strError = ('There are only %d elements in the tuple!') % len(tup)
            raise ValueError(strError)            
        inxN = 0         
        for element in tup:
            if inxN == iN:
                break
            inxN = inxN + 1
        return element




class ErrorTemplate(Exception):
    def __call__(self, *args):
        return self.__class__(*(self.args + args))


class ParameterMissingError(ErrorTemplate):
    pass
    
class ParameterTypeError(ErrorTemplate):
    pass
    
class ElementTypeError(ErrorTemplate):
    pass

class AllowedValuesError(ErrorTemplate):
    pass

class RelationalError(ErrorTemplate):
    pass



