"""
            This module contains _RxCSobject class, which is the main base class for
            all modules of RxCS.

            License:
                    BSD 2-clause

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    24 August 2015

            Versions:
                0.1     | 20-JUL-2015 : * Initial version. |br|
                1.0     | 18-AUG-2015 : * Version (1.0) is ready |br|
                1.01    | 19-AUG-2015 : * Function 'wasParamGivenVal' is added |br|
                1.02    | 19-AUG-2015 : * Function 'makeArray2Dim' is added |br|
                1.02r1  | 19-AUG-2015 : * Bug in checking the values of the Numpy arrays is fixed, |br|
                                          (devectorization of the arrays)
                1.03    | 20-AUG-2015 : * Function 'isequal' is added |br|
                1.04    | 24-AUG-2015 : * Function 'array2D2list1D' is added |br|


            List of functions in the module:

            Add parameters:
            paramAddMan    - Add a mandatory parameter to the object
            paramAddOpt    - Add an optional parameter to the object


            Assign allowed type:
            paramType      - assign allowed types of a parameter
            paramTypeEl    - assign allowed types of elements of a parameter


            Assign allowed values:
            paramAllowed   - assing a list with allowed values of a parameter
            NaNAllowedEl   - Allow for NaN elements in the parameter (make sense only for tuples, lists and np.ndarrays)


            Assign relational restrictions on a parameter:
            paramH       -  higher than a reference
            paramL       -  lower than a reference
            paramHE      -  higher or equal than a reference
            paramLE      -  lower or equal than a reference


            Assign restrictions on the size of a parameter:
            paramSizEq      - size equal to a reference
            paramSizH       - size higher than a reference
            paramSizL       - size lower than a reference
            paramSizHE      - size higher or equal to a reference
            paramSizLE      - size lower or equal to a reference


            Assign restriction of the number of dimensions of a parameter:
            paramNDimEq      - the number of dimensions equal to a reference
            paramNDimH       - the number of dimensions higher than a reference
            paramNDimL       - the number of dimensions lower than a reference
            paramNDimHE      - the number of dimensions higher or equal to a reference
            paramNDimLE      - the number of dimensions lower or equal to a reference


            Assign restriction of the size of a dimension of a parameter:
            paramDimEq       - the size of a dimension equal to a reference
            paramDimH        - the size of a dimension higher than a reference
            paramDimL        - the size of a dimension lower than a reference
            paramDimHE       - the size of a dimension higher or equal to a reference
            paramDimLE       - the size of a dimension lower or equal to a reference

            Assign restriction on uniqness of elements of a parameter:
            paramUnique       - elements of a parameter must be unique

            Get and check the parameters given to the module:
            parametersCheck     - check if all parameters of a module are correct

            wasParamGiven       - check if a parameter was given (recommended only for optional parameters)
                                  In fact, this function checks if the parameter exists, and if it has the value 
                                  different than NaN. If so, it returns 1, otherwise 0

            wasParamGivenVal    - check if a parameter was given (recommended only for optional parameters)
                                  In fact, this function checks if the parameter has the value different than NaN. 
                                  If so, it returns 1, otherwise 0
                                  
            makeArray2Dim       - make a 1Dimensional array a 2 dimensional
            array2D2list1D      - put rows of a 2D Numpy array into a list with 1D Numpy arrays
 
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
            __paramAddDimSizRestriction  -  assign restriction on the size of a dimension of a parameter
            __paramAddUniqueRestriction  -  assign restriction on uniqness of elements of a parameter

            __parameterWasDefined         - check if a parameter with a given name was already defined

            __parametersGetDict            - get parameters given to a function as dictionary
            __parametersGetArgs            - get parameters given directly to a function as a list of arguments

            __parametersCheckMandatory       - check if all the mandatory parameters are given
            __parametersOptAssignVal         - propagates a value onto optional parameters, if requested
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
            __checkRelVal_atl_parLen
            __checkRelVal_atl_refLen
            __checkRelVal_atl_vectorize
            __checkRelVal_atl_refNum
            __checkRelVal_atl_refAtl
            __checkRelVal_atl_PET_error
            __checkRelVal_atl_RET_error
            __checkRelVal_atl_lenParRef
            __checkRelVal_atl_error
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
            __checkDimSiz_error_restriction

            Control of restrictions on the dimensions:
            __checkUnique
            __checkUnique_elTypeCheck
            __checkUnique_error

            Auxiliary functions:
            __getReference        - get reference value and name
            __linearCoef2Strings  - change linear coefficients to strings
            __n2s                 - change number to a string,
                                    automatically regulate the number of digits after the comma
            __NthInTuple          - takes Nth element of a tuple
            __strOnlyNumb         - check if a given string contains only a number
            isequal               - check if two values are equal, with a given allowed margin

"""
from __future__ import division
import numpy as np
import console


class _RxCSobject:

    def __init__(self):
        self.strRxCSgroup = ''   # Initilize empty name of group of RxCS modules
        self.strModuleName = ''  # Initialize empty module name

        self.lParameters = []    # List with parameters
        self.iParam = 0          # The number of parameters

    def paramAddMan(self, strName, strDesc, unit='', noprint=0, unitprefix='-'):
        """
            Add a mandatory parameter to the object.

            Arguments:
                    strName:   [string]     name of a parameter, will become a public class member
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
        # ---------------------------------------------------------------------

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

        self.lParameters.append(dParameter)

        self.iParam = self.iParam + 1  # Increase the number of parameters

    def paramAddOpt(self, strName, strDesc, unit='', noprint=0, unitprefix='-', default=np.nan):
        """
            Add an optional parameter to the object.

            Arguments:
                    strName: [string]   name of a parameter, will become public class member
                    strDesc: [string]   short description of a parameter
                    unit:    [string]   unit of a parameter
                    noprint: [number]   switch off priting a parameter to the console by 'parametersPrint' function
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
        # ---------------------------------------------------------------------

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
        dParameter['bNaNAllowedEl'] = 1             # By default NaN elements ARE allowed (different than the mandatory arguments)
        dParameter['lRes'] = []                     # List of restriction

        self.lParameters.append(dParameter)

        self.iParam = self.iParam + 1  # Increase the number of parameters

    def paramType(self, strName, types):
        """
            Assign allowed types to a parameter. If types are assigned, it will be
            checked if a parameter is of correct type.

            Arguments:
                    strName: [string]           name of a parameter
                    types:   [type/tuple/list]  allowed types

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

        """

        # Error checks -------------------------------------------------------

        # Check a parameter
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter %s was not yet defined!') % strName
            raise RuntimeError(strError)

        # Check given types
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

        # ---------------------------------------------------------------------
        self.lParameters[inxParam]['lTypes'] = types
        return

    def paramTypeEl(self, strName, types):
        """
            Assign allowed types of elements of a parameter.
            If types are assigned, it will be checked if elements of a parameter
            are of correct types.
            It will be checked only if a parameter is of type:

                - list
                - tuple
                - numpy array

            Arguments:
                    strName: [string]           name of a parameter
                    types:   [type/tuple/list]  allowed types

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # Error checks -------------------------------------------------------

        # Check the given parameter
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter %s was not yet defined!') % strName
            raise RuntimeError(strError)

        # Check given types
        if isinstance(types, type):
            types = [types]
        elif(isinstance(types, list)):
            strWasGiven = 'list'
        elif(isinstance(types, tuple)):
            strWasGiven = 'tuple'
            types = list(types)
        else:
            raise ValueError('Allowed types of elements of a parameter must be a type, a tuple of types, or a list of types!')

        # Check a list with allowed types
        for inxType in range(len(types)):
            if (not isinstance(types[inxType], type)):
                strErr = 'Allowed types of elements of a parameter must be a type, a tuple of types, or a list of types!'
                strErr = strErr + '\n            Element #%d of the given %s of types is: %s' % \
                    (inxType, strWasGiven, type(types[inxType]))
                raise ValueError(strErr)
        # ---------------------------------------------------------------------
        self.lParameters[inxParam]['lTypesEl'] = types
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

        # ---------------------------------------------------------------------
        dRes = {}  
        dRes['strName'] = 'allowed values'
        dRes['strErrNote'] = errnote
        dRes['lAllowed'] = lAllowed

        self.lParameters[inxParam]['lRes'].append(dRes)

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
        """

        # Error checks -------------------------------------------------------

        # Check the given parameter
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter %s was not yet defined!') % strName
            raise RuntimeError(strError)

        # ---------------------------------------------------------------------
        self.lParameters[inxParam]['bNaNAllowedEl'] = 1
        return

    def paramH(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - higher than a reference

            Arguments:
                    strName:   [string]          name of a parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    mul:       [number]          multiply coefficient, reference will be multipled by this
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

        """
        self.__paramAddRelRestriction('higher than', strName, reference, mul, add, errnote)

    def paramL(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - lower than a reference

            Arguments:
                    strName:   [string]          name of a parameter
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
        """
        self.__paramAddRelRestriction('lower than', strName, reference, mul, add, errnote)

    def paramHE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - higher or equal to a reference

            Arguments:
                    strName:   [string]          name of a parameter
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
        """
        self.__paramAddRelRestriction('higher or equal to', strName, reference, mul, add, errnote)

    def paramLE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - lower or equal to a reference

            Arguments:
                    strName:   [string]          name of a parameter
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
        """
        self.__paramAddRelRestriction('lower or equal to', strName, reference, mul, add, errnote)

    def paramSizEq(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign size restriction to a parameter - size equal to a reference

            Arguments:
                    strName:   [string]          name of a parameter
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
        """

        self.__paramAddSizRestriction('size equal to', strName, reference, mul, add, errnote)

    def paramSizH(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign size restriction to a parameter - size higher than a reference

            Arguments:
                    strName:   [string]          name of a parameter
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
        """
        self.__paramAddSizRestriction('size higher than', strName, reference, mul, add, errnote)

    def paramSizL(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign size restriction to a parameter - size lower than a reference

            Arguments:
                    strName:   [string]          name of a parameter
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

        """
        self.__paramAddSizRestriction('size lower than', strName, reference, mul, add, errnote)

    def paramSizHE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign size restriction to a parameter - size higher than a reference

            Arguments:
                    strName:   [string]          name of a parameter
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

        """
        self.__paramAddSizRestriction('size higher or equal to', strName, reference, mul, add, errnote)

    def paramSizLE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign size restriction to a parameter - size lower or equal to a reference

            Arguments:
                    strName:   [string]          name of a parameter
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

        """
        self.__paramAddSizRestriction('size lower or equal to', strName, reference, mul, add, errnote)

    def paramNDimEq(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign restriction on the number of dimensions to a parameter -
            the number of dimensions equal to a reference

            Arguments:
                    strName:   [string]          name of a parameter
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

        """
        self.__paramAddNDimRestriction('number of dimensions equal to', strName, reference, mul, add, errnote)

    def paramNDimH(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign restriction on the number of dimensions to a parameter -
            the number of dimensions higher than a reference

            Arguments:
                    strName:   [string]          name of a parameter
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
        """
        self.__paramAddNDimRestriction('number of dimensions higher than', strName, reference, mul, add, errnote)

    def paramNDimL(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign restriction on the number of dimensions to a parameter -
            the number of dimensions lower than a reference

            Arguments:
                    strName:   [string]          name of a parameter
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
        """
        self.__paramAddNDimRestriction('number of dimensions lower than', strName, reference, mul, add, errnote)

    def paramNDimHE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign restriction on the number of dimensions to a parameter -
            the number of dimensions higher or equal to a reference

            Arguments:
                    strName:   [string]          name of a parameter
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
        """
        self.__paramAddNDimRestriction('number of dimensions higher or equal to', strName, reference, mul, add, errnote)

    def paramNDimLE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign restriction on the number of dimensions to a parameter -
            the number of dimensions lower or equal to a reference

            Arguments:
                    strName:   [string]          name of a parameter
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
        """
        self.__paramAddNDimRestriction('number of dimensions lower or equal to', strName, reference, mul, add, errnote)

    def paramDimEq(self, strName, reference, dimension, refdim=np.nan, pedantic=0, mul=1, add=0, errnote=''):
        """
            Assign restriction on the size of a dimension of a parameter -
            the size of a dimension equals to a reference

            Arguments:
                    strName:   [string]          name of a parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    dimension  [string/number]   code of a dimension or an index of a dimension
                    refdim     [string/number]   code of a reference dimension, or an index of a reference dimension, [optional, default = np.nan]
                                                 if refdim == np.nan than refdim = reference
                    pedantic   [number]          If pedantic flag is cleared, size of unexisted dimensions is treated as 1
                                                 otherwise, if unexisted dimension is being called it is an error!
                    mul:       [number]          multiply coefficient, reference will be multipled by this [optional, default = 1]
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul [optional, default = 0]
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        self.__paramAddDimSizRestriction('dimension size equal to', strName, reference, pedantic, dimension, refdim, mul, add, errnote)

    def paramDimH(self, strName, reference, dimension, refdim=np.nan, pedantic=0, mul=1, add=0, errnote=''):
        """
            Assign restriction on the size of a dimension of a parameter -
            the size of a dimension higher than a reference

            Arguments:
                    strName:   [string]          name of a parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    dimension  [string/number]   code of a dimension or an index of a dimension
                    refdim     [string/number]   code of a reference dimension, or an index of a reference dimension, [optional, default = np.nan]
                                                 if refdim == np.nan than refdim = reference
                    pedantic   [number]          If pedantic flag is cleared, size of unexisted dimensions is treated as 1
                                                 otherwise, if unexisted dimension is being called it is an error!
                    mul:       [number]          multiply coefficient, reference will be multipled by this [optional, default = 1]
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul [optional, default = 0]
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        self.__paramAddDimSizRestriction('dimension size higher than', strName, reference, pedantic, dimension, refdim, mul, add, errnote)

    def paramDimL(self, strName, reference, dimension, refdim=np.nan, pedantic=0, mul=1, add=0, errnote=''):
        """
            Assign restriction on the size of a dimension of a parameter -
            the size of a dimension lower than a reference

            Arguments:
                    strName:   [string]          name of a parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    dimension  [string/number]   code of a dimension or an index of a dimension
                    refdim     [string/number]   code of a reference dimension, or an index of a reference dimension, [optional, default = np.nan]
                                                 if refdim == np.nan than refdim = reference
                    pedantic   [number]          If pedantic flag is cleared, size of unexisted dimensions is treated as 1
                                                 otherwise, if unexisted dimension is being called it is an error!
                    mul:       [number]          multiply coefficient, reference will be multipled by this [optional, default = 1]
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul [optional, default = 0]
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        self.__paramAddDimSizRestriction('dimension size lower than', strName, reference, pedantic, dimension, refdim, mul, add, errnote)

    def paramDimHE(self, strName, reference, dimension, refdim=np.nan, pedantic=0, mul=1, add=0, errnote=''):
        """
            Assign restriction on the size of a dimension of a parameter -
            the size of a dimension higher or equal to a reference

            Arguments:
                    strName:   [string]          name of a parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    dimension  [string/number]   code of a dimension or an index of a dimension
                    refdim     [string/number]   code of a reference dimension, or an index of a reference dimension, [optional, default = np.nan]
                                                 if refdim == np.nan than refdim = reference
                    pedantic   [number]          If pedantic flag is cleared, size of unexisted dimensions is treated as 1
                                                 otherwise, if unexisted dimension is being called it is an error!
                    mul:       [number]          multiply coefficient, reference will be multipled by this [optional, default = 1]
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul [optional, default = 0]
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        self.__paramAddDimSizRestriction('dimension size higher or equal to', strName, reference, pedantic, dimension, refdim, mul, add, errnote)

    def paramDimLE(self, strName, reference, dimension, refdim=np.nan, pedantic=0, mul=1, add=0, errnote=''):
        """
            Assign restriction on the size of a dimension of a parameter -
            the size of a dimension lower or equal to a reference

            Arguments:
                    strName:   [string]          name of a parameter
                    reference: [string/number]   reference, it can be a number or a name of another parameter
                    dimension  [string/number]   code of a dimension or an index of a dimension
                    refdim     [string/number]   code of a reference dimension, or an index of a reference dimension, [optional, default = np.nan]
                                                 if refdim == np.nan than refdim = reference
                    pedantic   [number]          If pedantic flag is cleared, size of unexisted dimensions is treated as 1
                                                 otherwise, if unexisted dimension is being called it is an error!
                    mul:       [number]          multiply coefficient, reference will be multipled by this [optional, default = 1]
                    add:       [number]          add coefficient, will be added to a reference AFTER multiplication by mul [optional, default = 0]
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        self.__paramAddDimSizRestriction('dimension size lower or equal to', strName, reference, pedantic, dimension, refdim, mul, add, errnote)

    def paramUnique(self, strName, errnote=''):
        """
            Assign restriction on uniqness of a parameter.

            Arguments:
                    strName:   [string]          name of a parameter
                    errnote    [string]          optional error note, will be displayed if the restriction is broken
                                                 (optional, by default it is '' (empty string), which means that an error
                                                  note will be constructed automatically)
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        self.__paramAddUniqueRestriction(strName, errnote)
        
    def parametersCheck(self):
        """
            Function checks if all parameters of a module are correct.

            Arguments:
                    none
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

        """
        self.__parametersCheckMandatory()     # Check if all the mandatory parameters are given
        self.__parametersOptAssignVal()       # Assign values to optional parameters which are taken from other parameters        
        self.__parametersCheckType()          # Check types of all the parameters
        self.__parametersCheckRestrictions()  # Check restrictions on the parameters

    def wasParamGiven(self, strParName):
        """
            Function checks if a parameter was given.

            Arguments:
                    strParName:  [string]   name of the parameter
            Output:
                    0 - parameter was not given
                    1 - parameter was given

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        if not strParName in (self.__dict__):
            return 0
        if isinstance(self.__dict__[strParName], float):
            if np.isnan(self.__dict__[strParName]):
                return 0
        return 1
        
    def wasParamGivenVal(self, iVal):
        """
            Function checks if a parameter was given, or
            if it still has the default value.

            Arguments:
                    iVal:   value of the parameter
            Output:
                    0 - parameter was not given
                    1 - parameter was given

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        if isinstance(iVal, float):
            if np.isnan(iVal):
                return 0
        return 1

    def makeArray2Dim(self, mArr):
        """
            Function changes a 1 dimensional Numpy array into a 2 dimensional.

            Arguments:
                    mArr:  [Numpy array]  1- or 2-dimensional Numpy array
            
            Output: 
                    mArr:  [Numpy array 2D]  2 dimensional Numpy array

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # Make a 1D Numpy array with signals 2 dim, if it is 1 dim
        if mArr.ndim == 1:
            mArr = mArr.copy()   
            mArr.shape = (1, mArr.size)
        return mArr


    def array2D2list1D(self, mArr, remnan=1):
        """
            This function changes a 2D Numpy array into a list with 1D arrays.
            If remnan == 1 than NaN elements are removed.

            Arguments:
                    mArr:  [Numpy array]  1- or 2-dimensional Numpy array
                    remnan: [number]      1-remove NaN, 0-do not remove NaN            
            
            Output: 
                    lRows:  [list]  the list with rows of the input matrices

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        if not isinstance(mArr, np.ndarray):
            raise ValueError('Input matrix must be 2D or 1D Numpy array!')            
        if mArr.ndim > 2:
            raise ValueError('Input matrix must be 2D or 1D Numpy array!')
        elif mArr.ndim == 1:
            mArr = self.makeArray2Dim(mArr)
        elif mArr.ndim < 1:
            raise ValueError('Input matrix must be 2D or 1D Numpy array!')
            
        (nRows, _) = mArr.shape
        lRows = []
        
        if remnan == 0:
            for inxRow in range(nRows):
                lRows.append(mArr[inxRow, :])
        else:
            for inxRow in range(nRows):
                vRow = mArr[inxRow, :]
                vRow = vRow[np.invert(np.isnan(vRow))]
                lRows.append(vRow)
        return lRows


    def parametersPrint(self):
        """
            Function prints parameters of a module.

            Arguments:
                    none

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        if self.bMute == 0:

            # Print out the header of the module
            console.progress(self.strRxCSgroup, self.strModuleName)

            # Loop over all parameters
            for inxPar in range(self.iParam):
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
                        console.bullet_info(strDesc, 'NaN')
                    else:
                        console.bullet_param(strDesc, par, strUnitPrefix, strUnit)

                elif isinstance(par, str):
                    console.bullet_info(strDesc, par)
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
        """

        if self.bMute == 0:
            strName = ('%s: \'%s\' is starting') % (self.strRxCSgroup, self.strModuleName)
            self.__tStartOfModuleRxCSobject = console.module_progress(strName)

    def engineStopsInfo(self):
        """
            Function prints info about stop of a module engine.

            Arguments:
                    none

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        if self.bMute == 0:
            strName = ('%s: \'%s\'.............') % (self.strRxCSgroup, self.strModuleName)
            console.module_progress(strName)
            console.module_progress_done(self.__tStartOfModuleRxCSobject)

    # ##-----------------------------------------------------------------------
    # ## INTERNAL FUNCTIONS:
    # ##-----------------------------------------------------------------------

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
        for inxChr in range(1, len(strName)):
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
        if isinstance(reference, float):
            if np.isnan(reference):
                raise ValueError('Reference must not be nan!')

        # ---------------------------------------------------------------------
        dRes = {}  
        dRes['strName'] = strResCode
        dRes['strErrNote'] = strErrNote
        dRes['reference'] = reference
        dRes['coeff'] = [iMul, iAdd]

        self.lParameters[inxParam]['lRes'].append(dRes)

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
        if isinstance(reference, float):
            if np.isnan(reference):
                strError = 'Reference must not be NaN!\n'
                strError = strError + '            Reference for restriction \'%s\' for parameter > %s < is NaN!' \
                    % (strResCode, strName)
                raise ValueError(strError)

        # ---------------------------------------------------------------------
        dRes = {}  
        dRes['strName'] = strResCode
        dRes['strErrNote'] = strErrNote
        dRes['reference'] = reference
        dRes['coeff'] = [iMul, iAdd]

        self.lParameters[inxParam]['lRes'].append(dRes)

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
        if isinstance(reference, float):
            if np.isnan(reference):
                raise ValueError('Reference must not be nan!')

        # ---------------------------------------------------------------------
        dRes = {}  
        dRes['strName'] = strResCode
        dRes['strErrNote'] = strErrNote
        dRes['reference'] = reference
        dRes['coeff'] = [iMul, iAdd]

        self.lParameters[inxParam]['lRes'].append(dRes)

        return

    def __paramAddDimSizRestriction(self, strResCode, strName, reference, bPedantic, dimension, refdim, iMul, iAdd, strErrNote):
        """
            Assign restriction on the size of a dimension of a parameter

            Arguments:

                    strResCode:   [string]          code of a restriction
                    strName:      [string]          name of a parameter
                    reference:    [string/number]   reference, it can be a number or a name of another parameter
                    bPedantic     [number]          if pedantic flag is cleared, size of unexisted dimensions is treated as 1
                                                    otherwise, if unexisted dimension is being called it is an error!
                    dimension     [string/number]   code of a dimension or an index of a dimension
                    refdim        [string/number]   code of a reference dimension, or an index of a reference dimension, [optional, default = np.nan]
                                                    if refdim == np.nan than refdim = reference
                    iMul:         [number]          multiply coefficient, reference will be multipled by this
                    iAdd:         [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    strErrNote    [string]          optional error note, will be displayed if the restriction is broken

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
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

        # Dimension index
        if not isinstance(dimension, (int, str)):
            raise ValueError('Dimension index must be an integer number or a string')

        # Reference dimension index
        if not isinstance(refdim, (int, str)):
            if isinstance(refdim, float):
                if not np.isnan(refdim):
                    raise ValueError('Dimension index of a reference must be a string, an integer number or NaN!')
            else:
                    raise ValueError('Dimension index of a reference must be a string, an integer number or NaN!')

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
        if isinstance(reference, float):
            if np.isnan(reference):
                raise ValueError('Reference must not be nan!')

        # ---------------------------------------------------------------------
        dRes = {}
        dRes['strName'] = strResCode
        dRes['strErrNote'] = strErrNote
        dRes['reference'] = reference
        dRes['coeff'] = [iMul, iAdd]
        dRes['dimension'] = dimension
        dRes['refdim'] = refdim
        dRes['bPedantic'] = bPedantic

        self.lParameters[inxParam]['lRes'].append(dRes)

        return


    def __paramAddUniqueRestriction(self, strName, strErrNote):
        """
            Assign restriction of uniqness of elements of a parameter

            Arguments:
                    strName:      [string]    name of a parameter
                    strErrNote:   [string]    optional error note, will be displayed if the restriction is broken

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # Error checks -------------------------------------------------------

        # Parameter to be checked
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter > %s < was not yet defined!') % strName
            raise RuntimeError(strError)

        # Error note
        if not isinstance(strErrNote, str):
            raise ValueError('Error note must be a string ')

        # ---------------------------------------------------------------------
        dRes = {}
        dRes['strName'] = 'unique elements'
        dRes['strErrNote'] = strErrNote

        self.lParameters[inxParam]['lRes'].append(dRes)

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
        """
        # Loop over all defined parameters
        for dParam in self.lParameters:
            strParName = dParam['strName']
            if strParName in dArgInput:
                self.__dict__[strParName] = dArgInput[strParName]
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
        """
        # Loop over all parameters
        for inxParam in range(self.iParam):

            dParam = self.lParameters[inxParam]  # Get the dictionary with parameter data
            
            # If it is an optional parameter, skip it            
            if dParam['bOptional'] == 1:
                continue

            strParName = dParam['strName']
            if isinstance(self.__dict__[strParName], float):
                if np.isnan(self.__dict__[strParName]):
                    strError = ('Mandatory parameter > %s < is not given!') % strParName
                    raise ParameterMissingError(strError)

    def __parametersOptAssignVal(self):
        """
            Function propagates onto optional parameters a value from the other parameters,
            if such a propagation was requested.

            Arguments:
                    none
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # Loop over all optional parameters
        for inxParam in range(self.iParam):

            dParam = self.lParameters[inxParam]  # Get the dictionary with parameter data

            # If it is a mandatory parameter, skip it            
            if dParam['bOptional'] == 0:
                continue

            strParName = dParam['strName']       # Name of the current parameter
            parVal = self.__dict__[strParName]   # Get the parameter

            # If it is not a string, continue to the next parameter
            if not isinstance(parVal, str):
                continue

            # If it is shorter than 3, continue to the next parameter
            if len(parVal) < 3:
                continue
            
            # If the first two values of the parameter are not '$$', continue to the next parameter
            if not (parVal[0] == '$' and parVal[1] == '$'):
                continue
            
            # Take the name of the parameter from which the value should be propagated
            strRefName = parVal[2:len(parVal)]
            if not self.__parameterWasDefined(strRefName):
                strError = 'Reference parameter %s does not exist! (Reference for parameter > %s <)' \
                    % (strRefName, strParName)
                raise NameError(strError)
            
            # Propagate the value
            self.__dict__[strParName] = self.__dict__[strRefName]                        
        return

    def __parametersCheckType(self):
        """
            Function checks types of all the parameters and their elements.

            Arguments:
                    none
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        # Loop over all parameters
        for inxPar in range(self.iParam):

            # Get the dictionary with parameter data
            dParam = self.lParameters[inxPar]

            # If type is not given, continue to the next parameter
            if not ('lTypes' in dParam):
                continue

            # Get the name of the parameter, allowed types and the parameter itself
            strParName = dParam['strName']         # Name of the current parameter
            strDesc = dParam['strDesc']            # Description of the currect parameter
            lTypes = dParam['lTypes']              # Allowed types of the current parameter
            bOptional = dParam['bOptional']        # The optional flag
            parameter = self.__dict__[strParName]   # Get the parameter

            # If this is an optional parameter, and it has a NaN value, do nothng with it
            if bOptional:
                if not self.wasParamGiven(strParName):
                    return

            # Check the type
            if not (isinstance(parameter, tuple(lTypes))):
                strError = ('Type %s is incorrect for parameter > %s < !') % (type(parameter), strParName)
                raise ParameterTypeError(strError)

            # Check types of elements, if needed
            if isinstance(parameter, (np.ndarray, list, tuple)):
                if not ('lTypesEl' in self.lParameters[inxPar]):
                    continue
                lTypesEl = self.lParameters[inxPar]['lTypesEl']   # Allowed types of elements of the current parameter

                # Service for numpy array
                if isinstance(parameter, np.ndarray):
                    if (parameter.size > 0):
                        original_shape = parameter.shape
                        parameter.shape = (parameter.size, )
                        if not (isinstance(parameter[0], tuple(lTypesEl))):
                            strError = ('Parameter > %s < contains elements of an illegal type (%s)!') \
                                % (strParName, type(parameter[0]))
                            raise ElementTypeError(strError)
                        parameter.shape = original_shape
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
        """

        # Loop over all parameters
        for inxPar in range(self.iParam):
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
        """
        strParName = dParam['strName']            # Name of the parameter
        strDesc = dParam['strDesc']               # Description of the parameter
        parVal = self.__dict__[strParName]        # The parameter itself
        bNaNAllowedEl = dParam['bNaNAllowedEl']   # NaN elements allowed flag
        bOptional = dParam['bOptional']           # The optional flag

        # If this is an optional parameter, and it has a NaN value, do nothng with it
        if bOptional:
            if not self.wasParamGiven(strParName):
                return

        # Loop over all restrictions
        for inxRes in range(len(dParam['lRes'])):
            
            # Get the restriction dictionary
            dRes = dParam['lRes'][inxRes]     # Restriction dictionary
            strResCode = dRes['strName']      # Restriction code

            (refVal, strRefName) = self.__getReference(dRes)

            # Run the correct parameter restriction check function:
            # allowed values
            if (strResCode == 'allowed values'):
                self.__checkAllowedVal(strParName, strDesc, parVal, bNaNAllowedEl, dRes)

            # value relational restrictions
            elif (strResCode == 'higher than' or
                    strResCode == 'higher or equal to' or
                    strResCode == 'lower than' or
                    strResCode == 'lower or equal to'):
                self.__checkRelVal(strParName, strDesc, parVal, strRefName, refVal, strResCode, bNaNAllowedEl, dRes)

            # size restrictions
            elif (strResCode == 'size equal to' or
                    strResCode == 'size higher than' or
                    strResCode == 'size higher or equal to' or
                    strResCode == 'size lower than' or
                    strResCode == 'size lower or equal to'):
                self.__checkSiz(strParName, strDesc, parVal, strRefName, refVal, strResCode, dRes)

            # the number of dimensions
            elif (strResCode == 'number of dimensions equal to' or
                    strResCode == 'number of dimensions higher than' or
                    strResCode == 'number of dimensions higher or equal to' or
                    strResCode == 'number of dimensions lower than' or
                    strResCode == 'number of dimensions lower or equal to'):
                self.__checkNDim(strParName, strDesc, parVal, strRefName, refVal, strResCode, dRes)

            # size of restrictions
            elif (strResCode == 'dimension size equal to' or
                    strResCode == 'dimension size higher than' or
                    strResCode == 'dimension size lower than' or
                    strResCode == 'dimension size higher or equal to' or
                    strResCode == 'dimension size lower or equal to'):
                self.__checkDimSiz(strParName, strDesc, parVal, strRefName, refVal, strResCode, dRes)

            # uniqness
            elif (strResCode == 'unique elements'):
                self.__checkUnique(strParName, strDesc, parVal, dRes)

            # unknown restrictions
            else:
                raise RuntimeError('Unknown parameter restriction. Something went seriously wrong...[internal RxCSobject error]')

    def __checkAllowedVal(self, strParName, strDesc, parVal, bNaNAllowedEl, dRes):
        """
            Function checks the 'allowed values' restriction of a parameter.

            Arguments:
                    strParName:  [string]        name of a parameter
                    strDesc:     [string]        description of a parameter
                    parVal:                      value of the parameter to be checked
                    bNaNAllowed: [number]        'NaN' elements allowed flag
                    dRes:        [dictionary]    dictionary with all the restriction data

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # -------------------------------------------------------------------
        # Error check
        if not isinstance(parVal, (float, int, str, tuple, list, np.ndarray)):
            strError = 'Only numbers, strings, tuples, lists, and numpy arrays can be restricted with allowed values!'
            strError = strError + '(>%s< is of type: %s)' % (strParName, type(parVal))
            raise ValueError(strError)
        # -------------------------------------------------------------------

        lAllowed = dRes['lAllowed']        # Get the allowed values
        strErrNote = dRes['strErrNote']    # Get the error note

        # Run the correct function dependently on the parameter type
        if isinstance(parVal, (str, float, int)):
            self.__checkAllowedVal_numstr(strParName, strDesc, parVal, lAllowed, strErrNote)
        else:
            self.__checkAllowedVal_atl(strParName, strDesc, parVal, lAllowed, strErrNote, bNaNAllowedEl)
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
        """
        inxAl = 0  # Reset the index of elements in a list with allowed values

        # Loop over all elements of a list with allowed values
        for allVal in lAllVal:

            # An allowed value must be either a string or a number
            if not isinstance(allVal, (str, float, int)):
                strError = 'List of allowed values must contain only strings or numbers!\n'
                strError = strError + '            An allowed value #%d for the parameter > %s < (\'%s\') is of type %s' \
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
                strError = strError + '            An allowed value #%d for the parameter > %s < (\'%s\') is of type %s' \
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
                strError = strError + '            Element #%d of > %s < (%s) is of type %s' \
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

    def __checkRelVal(self, strParName, strDesc, parVal, strRefName, refVal, strRelation, bNaNAllowedEl, dRes):
        """
            Function checks relative value restriction of a parameter.

            Arguments:
                    strParName:   [string]         name of a parameter
                    strDesc:      [string]         description of a parameter
                    parVal:                        parameter to be checked
                    strRefName    [string]         name of a reference
                    refVal                         reference
                    strRelation   [string]         relation, allowed values:
                                                   'higher than', 'higher or equal to', 'lower than', 'lower or equal to'
                    bNaNAllowed   [number]         'NaN' elements allowed flag
                    dRes :        [dictionary]     dictionary with all the restriction data

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # -------------------------------------------------------------------
        # Error check
        if not isinstance(parVal, (float, int, tuple, list, np.ndarray)):
            strError = 'Only numbers, lists, tuples and numpy arrays can be restricted \'%s...\'! ' % (strRelation)
            strError = strError + '            (>%s< is of type: %s)' % (strParName, type(parVal))
            raise ValueError(strError)

        # -------------------------------------------------------------------

        lCoef = dRes['coeff']              # Get the list with coefficients
        strErrNote = dRes['strErrNote']    # Get the error note

        # Switch to correct function dependently on type of the parameter:
        if isinstance(parVal, (float, int)):
            self.__checkRelVal_num(strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRelation)
        else:
            self.__checkRelVal_atl(strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRelation, bNaNAllowedEl)

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
        """

        # Only numbers can be a reference
        if not isinstance(refVal, (float, int)):
            strError = 'Only numbers can be a reference for restriction \'%s...\' for numbers!\n' % (strRelation)
            strError = strError + '                 (> %s < is of type: %s)' % (strReference, type(refVal))
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
            strErrNote = '%s > %s < must be %s %s %s %s! (= %s) \n' \
                % (strDesc, strParName, strRelation, strMul, strReference, strAdd, self.__n2s(lCoef[0] * refVal + lCoef[1]))
            strErrNote = strErrNote + 17 * ' ' + 'Current value of > %s < is %s!' % (strParName, self.__n2s(parVal))
        raise RelationalError(strErrNote)

    def __checkRelVal_atl(self, strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRelation, bNaNAllowedEl):
        """
            Function checks the relative value restriction for Numpy arrays, tuples or lists.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    parVal:                       parameter to be checked
                    strRefName    [string]        name of a reference
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
        """

        # If reference is a NaN, number it can not be used as a reference, return from function
        if isinstance(refVal, float):
            if np.isnan(refVal):
                return

        # Take the length of the parameter
        iLen = self.__checkRelVal_atl_parLen(parVal)

        # Take the length of the reference
        iLenRef = self.__checkRelVal_atl_refLen(refVal, strRefName, strRelation)

        # Check the lengths of the parameter and the reference.
        # These lenghts must be the identical.
        self.__checkRelVal_atl_lenParRef(strParName, refVal, strRefName, iLen, iLenRef)

        # Vectorize the parameter and the reference
        (parVal, refVal, tparValShape, trefValShape) = self.__checkRelVal_atl_vectorize(parVal, refVal)

        # Check the restriction:
        if isinstance(refVal, (int, float)):
            # Check for number reference
            self.__checkRelVal_atl_refNum(strParName, strDesc, parVal, strRefName, refVal, lCoef,
                                          strErrNote, strRelation, bNaNAllowedEl)

        else:
            # Check for tuple, list, numpy array reference
            self.__checkRelVal_atl_refAtl(strParName, strDesc, parVal, strRefName, refVal, lCoef,
                                          strErrNote, strRelation, bNaNAllowedEl)

        # Devectorize the parameter and the reference
        (parVal, refVal) = self.__checkRelVal_atl_devectorize(parVal, refVal, tparValShape, trefValShape)

        return

    def __checkRelVal_atl_parLen(self, parVal):
        """
            Function computes length of a checked parameter.

            Arguments:
                    parVal:                   parameter to be checked

            Output:
                    iLen     [number]         length of a parameter

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        # Take the lenght of the checked parameter
        if isinstance(parVal, np.ndarray):
            iLen = parVal.size
        else:
            iLen = len(parVal)

        return iLen

    def __checkRelVal_atl_refLen(self, refVal, strRefName, strRelation):
        """
            Function computes length of a reference.

            Arguments:
                    refVal                        reference
                    strRefName    [string]        name of a reference
                    strRelation   [string]        relation, allowed values:
                                                  'higher than', 'higher or equal to', 'lower than', 'lower or equal to'
            Output:
                    iLenRef       [number]        length of a reference parameter

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

        """

        # Take the lenght of the  reference

        # Reference is a tuple or a list
        if isinstance(refVal, (tuple, list)):
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
            strError = strError + '       (>%s< is of type: %s)' % (strRefName, type(refVal))
            raise ValueError(strError)

        return iLenRef

    def __checkRelVal_atl_vectorize(self, parVal, refVal):
        """
            Function vectorizes checked parameter and a reference, if
            these variables are Numpy arrays.

            Arguments:
                    parVal:              parameter to be checked
                    refVal               reference

            Output:
                    parVal:               parameter to be checked (vectorized, if it was neccessary)
                    refVal:               reference (vectorized, if it was neccessary)
                    tParValShape:         tuple with the orignal shape of the parameter to tbe checked
                    tRefValShape:         tuple with the orignal shape of the reference

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # Vectorize the parameter, if it is a numpy array
        tParValShape = np.nan        
        if isinstance(parVal, np.ndarray):
            tParValShape = parVal.shape
            parVal.shape = (parVal.size, )

        # Vectorize the reference, if it is a numpy array
        tRefValShape = np.nan
        if isinstance(refVal, np.ndarray):
            tRefValShape = refVal.shape
            refVal.shape = (refVal.size, )

        return (parVal, refVal, tParValShape, tRefValShape)

    def __checkRelVal_atl_devectorize(self, parVal, refVal, tParValShape, tRefValShape):
        """
            Function devectorizes checked parameter and a reference, if
            these variables are Numpy arrays.

            Arguments:
                    parVal:               parameter to be checked
                    refVal                reference
                    tParValShape:         tuple with the orignal shape of the parameter to tbe checked
                    tRefValShape:         tuple with the orignal shape of the reference

            Output:
                    parVal:               parameter to be checked (vectorized, if it was neccessary)
                    refVal:               reference (vectorized, if it was neccessary)

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # Devectorize the parameter, if it is a numpy array
        if isinstance(parVal, np.ndarray):
            parVal.shape = tParValShape

        # Devectorize the reference, if it is a numpy array
        if isinstance(refVal, np.ndarray):
            refVal.shape = tRefValShape
        return (parVal, refVal)

    def __checkRelVal_atl_refNum(self, strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRelation, bNaNAllowedEl):
        """
            Function checks relative value restriction for Numpy arrays, tuples or lists,
            if a reference is a single number.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    parVal:                       parameter to be checked
                    strRefName    [string]        name of a reference
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
        """

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
        """
            Function checks relative value restriction for Numpy arrays, tuples or lists,
            if a reference is a Numpy Array, a tuple or a list.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    parVal:                       parameter to be checked
                    strRefName    [string]        name of a reference
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
        """

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
            if not (self.__checkRelVal_engine(parEl, refEl, lCoef, strRelation)):
                self.__checkRelVal_atl_error(strParName, strDesc, parVal, strRefName, refVal, lCoef,
                                             strErrNote, strRelation, inxEl)

    def __checkRelVal_atl_PET_error(self, strParName, strRelation, inxEl, parEl):
        """
            Function raises an error if elements of a checked parameter are not numbers.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strRelation   [string]        relation, allowed values:
                                                  'higher than', 'higher or equal to', 'lower than', 'lower or equal to'
                    inxEl         [number]        index of an element which is not a number
                    parEl                         element which is not a number

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # Throw the error of parameter element type , if it was found above
        strError = 'Only numbers can be checked for restriction  \'%s...\'!\n' % (strRelation)
        strError = strError + '            Element #%d of > %s < is of type %s!' % (inxEl, strParName, type(parEl))
        raise ValueError(strError)

    def __checkRelVal_atl_RET_error(self, strParName, strRefName, strRelation, inxEl, refEl):
        """
            Function raises an error if elements of a reference are not numbers.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strRefName    [string]        name of a reference
                    strRelation   [string]        relation, allowed values:
                                                  'higher than', 'higher or equal to', 'lower than', 'lower or equal to'
                    inxEl         [number]        index of an element of a reference which is not a number
                    refEl                         element of a reference which is not a number

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # Throw the error of reference parameter element type , if it was found above
        strError = 'Only numbers can be a reference for restriction  \'%s...\'!\n' % (strRelation)
        strError = strError + '            Element #%d of %s (reference for > %s< ) is of type %s!' \
            % (inxEl, strRefName, strParName, type(refEl))
        raise ValueError(strError)

    def __checkRelVal_atl_lenParRef(self, strParName, refVal, strRefName, iLen, iLenRef):
        """
            Function compares the lenght of a checked parameter with the lenght of a reference,
            if the reference is a list, a tuple or a numpy array.
            If the lengths are not equal, it raises en error.

            Arguments:
                    strParName:   [string]        name of a parameter
                    refVal                        reference
                    strRefName    [string]        name of a reference
                    iLen          [number]        length of a parameter
                    iLenRef       [number]        length of a reference parameter

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        if isinstance(refVal, (list, tuple, np.ndarray)):
            if not (iLen == iLenRef):
                strError = 'Reference must be of equal size to the restricted parameter!\n'
                strError = strError + '            Parameter > %s < is of size %d, its reference (%s) is of size %d!' \
                    % (strParName, iLen, strRefName, len(refVal))
                raise ValueError(strError)

    def __checkRelVal_atl_error(self, strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRelation, inxEl):
        """
            Function raises an error is a parameter (a tuple, a list or a Numpy array) brakes the relative value restriction.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    parVal:                       parameter to be checked
                    strRefName    [string]        name of a reference
                    refVal                        reference
                    lCoef         [list]          list with 'mul' and 'add' coefficients
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then a default note is generated)
                    strRelation   [string]        relation, allowed values:
                                                  'higher than', 'higher or equal to', 'lower than', 'lower or equal to'
                    inxEl         [number]        index of an element which brakes the restriction

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # Throw out an error, if the error note was already given
        if not (strErrNote == ''):
            raise RelationalError(strErrNote)

        # Construct the error note:

        iMul = lCoef[0]  # Get the linear coefficients
        iAdd = lCoef[1]  # ^
        # Firstly, change linear coefficients into strings
        (strMul, strAdd) = self.__linearCoef2Strings(lCoef)

        # If the reference is a number it is easy to construct the error info...
        if isinstance(refVal, (int, float)):
            strErrNote = 'All elements of > %s < (%s) must be %s %s%s%s' \
                % (strParName, strDesc, strRelation, strMul, strRefName, strAdd)
            if (strMul != '' or strAdd != '' or (not self.__strOnlyNumb(strRefName))):
                strErrNote = strErrNote + ' (%s%s%s = %s)' \
                    % (strMul, self.__n2s(refVal), strAdd, self.__n2s(iMul * refVal + iAdd))
            strErrNote = strErrNote + '!\n'
            strErrNote = strErrNote + 17 * ' ' + 'Element #%d of > %s < is %s!' \
                % (inxEl, strParName, self.__n2s(parVal[inxEl]))
            raise RelationalError(strErrNote)

        # If the reference is an array, a tuple or a list, it is getting complicated...
        if (strMul == '') and (strAdd == ''):
            strErrNote = 'Elements of > %s < (%s) must be %s\n' \
                % (strParName, strDesc, strRelation)
            strErrNote = strErrNote + 17 * ' ' + 'the corresponding elements of %s !\n' \
                % (strRefName)
        else:
            strErrNote = 'Elements of > %s < (%s) must be %s %sx%s,\n' \
                % (strParName, strDesc, strRelation, strMul, strAdd)
            strErrNote = strErrNote + 17 * ' ' + 'where x are the corresponding elements of %s !\n' \
                % (strRefName)

        # Add info about the element which brakes the restriction
        strErrNote = strErrNote + 17 * ' ' + 'Element #%d of > %s < is %s, element #%d of %s is %s' \
            % (inxEl, strParName, self.__n2s(parVal[inxEl]), inxEl, strRefName, self.__n2s(refVal[inxEl]))
        if (strMul != '') or (strAdd != ''):
            strErrNote = strErrNote + ' (%s%s%s = %s)' \
                % (strMul, self.__n2s(refVal[inxEl]), strAdd, self.__n2s(iMul * refVal[inxEl] + iAdd))
        strErrNote = strErrNote + '!'

        # Ok, error is ready, throw out an error
        raise RelationalError(strErrNote)

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

    def __checkSiz(self, strParName, strDesc, parVal, strRefName, refVal, strRes, dRes):
        """
            Function checks the size restrictions of a parameter.

            Arguments:
                    strParName:   [string]        name of the parameter
                    strDesc:      [string]        description of the parameter
                    parVal:                       parameter to be checked
                    strRefName    [string]        name of a reference
                    refVal                        reference
                    strRes        [string]        restriction, allowed values:
                                                  'size equal to', 'size higher than', 'size higher or equal to',
                                                  'size lower than', 'size lower or equal to'
                    dRes          [dictionary]    dictionary with all the restriction data 

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        lCoef = dRes['coeff']              # Get the list with coefficients
        strErrNote = dRes['strErrNote']    # Get the error note

        # Take the size of the tested parameter
        iSize = self.__checkSiz_sizParam(parVal, strParName)

        # Take the reference size
        iRefSize = self.__checkSiz_sizRef(strParName, refVal, strRefName, strRes)

        # Check the restriction, if it is ok, return
        if not self.__checkSiz_engine(iSize, iRefSize, lCoef, strRes):
            self.__checkSiz_error(strParName, strDesc, strRefName, refVal, lCoef, strErrNote, strRes, iSize, iRefSize)

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
            strError = strError + '            ( > %s < is of type: %s )' % (strParName, type(parVal))
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
                    iRefSize:     [number]        reference of size restriction

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
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
            strError = 'Only numbers, strings, tuples, lists, and numpy arrays can be a reference for size restriction!\n'
            strError = strError + 12 * ' ' + '%s (restriction for > %s < ) is of type: %s)' \
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
        """

        iMul = lCoef[0]     # Take the linear coefficients
        iAdd = lCoef[1]     # Take the linear coefficients

        iRefSize = iMul * iRefSize + iAdd  # Apply the linear coefficients

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

    def __checkSiz_error(self, strParName, strDesc, strRefName, refVal, lCoef, strErrNote, strRes, iSize, iRefSize):
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
                    iRefSize      [number]        reference for size restriction

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # If error note was given, use it
        if not strErrNote == '':
            raise SizeError(strErrNote)

        # Change linear coefficients into strings
        (strMul, strAdd) = self.__linearCoef2Strings(lCoef)

        # Construct the error message:

        # Reference is a number or a parameter
        if isinstance(refVal, (int, float)):

            # Reference was given as a direct number
            if (self.__strOnlyNumb(strRefName)):

                # No linear coefficients
                if (strMul == '') and (strAdd == ''):   # Only numbers and no linear coefficients
                    strErrNote = 'Parameter > %s < (%s) must have %s %s!\n' \
                        % (strParName, strDesc, strRes, strRefName)

                # Linear coefficients were given
                else:
                    strErrNote = 'Parameter > %s < (%s) must have %s %s%s%s (=%s)!\n' \
                        % (strParName, strDesc, strRes, strMul, strRefName, strAdd, self.__n2s(lCoef[0] * refVal + lCoef[1]))

            # Reference is a parameter which contains a number
            else:
                # No linear coefficients
                if (strMul == '') and (strAdd == ''):
                    strErrNote = 'Parameter > %s < (%s) must have %s the value of %s (=%s)!\n' \
                        % (strParName, strDesc, strRes, strRefName, self.__n2s(refVal))

                # Linear coefficients were given
                else:
                    strErrNote = 'Parameter > %s < (%s) must have %s the value of %s%s%s (%s%s%s = %s)!\n' \
                        % (strParName, strDesc, strRes, strMul, strRefName, strAdd, strMul, iRefSize, strAdd, self.__n2s(lCoef[0] * refVal + lCoef[1]))

        # Reference is a size of a parameter
        else:
                # No linear coefficients
                if (strMul == '') and (strAdd == ''):
                    strErrNote = ('Parameter > %s < (%s) must have %s the size of %s (=%s)!\n') \
                        % (strParName, strDesc, strRes, strRefName, self.__n2s((iRefSize)))

                # Linear coefficients were given
                else:
                    strErrNote = ('Parameter > %s < (%s) must have %s %sthe size of %s%s (%s%s%s = %s)!\n') \
                        % (strParName, strDesc, strRes, strMul, strRefName, strAdd, strMul, iRefSize, strAdd, self.__n2s(lCoef[0] * iRefSize + lCoef[1]))

        strErrNote = strErrNote + 11 * ' ' + 'The current size of > %s < is %d!' % (strParName, iSize)
        raise SizeError(strErrNote)

    def __checkNDim(self, strParName, strDesc, parVal, strRefName, refVal, strRes, dRes):
        """
            Function checks restrictions imposed on the number of dimensions of a parameter.

            Arguments:
                    strParName:   [string]        name of the parameter
                    strDesc:      [string]        description of the parameter
                    parVal:                       parameter to be checked
                    strRefName    [string]        name of a reference
                    refVal                        reference
                    strRes        [string]        restriction, allowed values:
                                                  'number of dimensions equal to', 'number of dimensions higher than',
                                                  'number of dimensions higher or equal to', 'number of dimensions lower than',
                                                  'number of dimensions lower or equal to'
                    dRes          [dictionary]    dictionary with all the restriction data

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
5
        """

        lCoef = dRes['coeff']              # Get the list with coefficients
        strErrNote = dRes['strErrNote']    # Get the error note

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
            strError = strError + '            ( > %s < is of type: %s )' % (strParName, type(parVal))
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
        """

        # If error note was given, use it
        if not (strErrNote == ''):
            raise NDimError(strErrNote)

        # Construct the error message:

        # Change linear coefficients into strings
        (strMul, strAdd) = self.__linearCoef2Strings(lCoef)

        # Reference was a number or a parameter
        if isinstance(refVal, (int, float)):

            # Reference was given directly as a number
            if (self.__strOnlyNumb(strRefName)):

                # No linear coefficients
                if (strMul == '') and (strAdd == ''):
                    strError = ('Parameter > %s < (%s) must have the %s %s!\n') \
                        % (strParName, strDesc, strRes, strRefName)

                # Linear coefficients were given
                else:
                    strError = ('Parameter > %s < (%s) must have the %s %s%s%s (=%s)!\n') \
                        % (strParName, strDesc, strRes, strMul, strRefName, strAdd, self.__n2s(lCoef[0] * refVal + lCoef[1]))

            # Reference is a parameter which contains a number
            else:

                # No linear coefficients
                if (strMul == '') and (strAdd == ''):
                    strError = ('Parameter > %s < (%s) must have the %s the value of %s (=%s)!\n') \
                        % (strParName, strDesc, strRes, strRefName, self.__n2s(refVal))

                # Linear coefficients were given
                else:
                    strError = ('Parameter > %s < (%s) must have the %s the value of %s%s%s (%s%s%s = %s)\n') \
                        % (strParName, strDesc, strRes, strMul, strRefName, strAdd, strMul, iRefNDim, strAdd, self.__n2s(lCoef[0] * refVal + lCoef[1]))

        # reference was the number of diemsnions in another parameter
        else:

            strError = ('Parameter > %s < (%s) must have the %s\n') \
                % (strParName, strDesc, strRes)

            # No linear coefficients
            if (strMul == '') and (strAdd == ''):
                strError = strError + 11 * ' ' + ('the number of dimensions of %s (%s)!\n') \
                    % (strRefName, self.__n2s(iRefNDim))

            # Linear coefficients were given
            else:
                strError = strError + 11 * ' ' + ('%sthe number of dimensions of %s %s (%s%s%s = %s)!\n') \
                    % (strMul, strRefName, strAdd, strMul, self.__n2s(iRefNDim), strAdd, self.__n2s(lCoef[0] * iRefNDim + lCoef[1]))

        # Add info about the number of dimensions in the tested parameter and the reference
        strError = strError + 11 * ' ' + 'The number of dimensions in parameter > %s < is %d!\n' % (strParName, iNDim)
        raise NDimError(strError)

    def __checkDimSiz(self, strParName, strDesc, parVal, strRefName, refVal, strRes, dRes):
        """
            Function checks restriction imposed on the size of a dimension of a parameter.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of the parameter
                    parVal:                       the parameter to be checked
                    strRefName    [string]        name of a reference
                    refVal                        reference
                    strRes        [string]        restriction, allowed values:
                                                  'dimension size equal to', 'dimension size higher than',
                                                  'dimension size lower than', 'dimension size higher or equal to',
                                                  'dimension size lower or equal to'
                    dRes          [dictionary]    dictionary with all the restriction data
                                        
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        strErrNote = dRes['strErrNote']    # Get the error note
        lCoeff = dRes['coeff']             # List with coefficients

        # Take the dimensions indices and 'pedantic' flag
        (iDim, iRefDim, bPedantic, _, _, dRes) = self.__checkDimSiz_dimensions(parVal, refVal, dRes)

        # Take the size of restricted dimension of the tested parameter
        iDimSize = self.__checkDimSiz_dimSizInParam(parVal, iDim, bPedantic, strParName, strDesc, dRes)

        # Take the size of dimension in reference
        iRefDimSize = self.__checkDimSiz_dimSizInRef(strParName, strDesc, iDim, refVal, dRes, strRefName, iRefDim, bPedantic, strRes)

        # Check the restriction
        if not self.__checkDimSiz_engine(iDimSize, iRefDimSize, lCoeff, strRes):
            self.__checkDimSiz_error(strParName, strDesc, parVal, strRefName, refVal, dRes, strErrNote, strRes, iDimSize, iRefDimSize)
        return

    def __checkDimSiz_dimensions(self, parVal, refVal, dRes):
        """
            Function return indices of dimensions to be checked and 'pedantic' flag.

            Arguments:
                    parVal:                       the parameter to be checked
                    refVal:                       reference
                    dRes          [dictionary]    dictionary with all the restriuction data

            Output:
                    iDim          [number]        index of dimension to be checked
                    iRefDim       [number]        index of reference dimension
                    bPedantic     [number]        'pedantic' flag
                    dimension     [string]        Human readable name of a dimension, if the name was recognized, otherwise an emtpy string
                    refdim        [string]        Human readable name of a reference dimension, if the name was recognized,
                                                  otherwise an emtpy string
                    dRes          [dictionary]    dictionary with all the restriuction data

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        # Take the dimensions indices and 'pedantic' flag
        bPedantic = dRes['bPedantic']      # 'pedantic' flag
        dimension = dRes['dimension']      # dimension code
        refdim = dRes['refdim']            # reference dimension 

        # If the dimension index of a reference is NaN,
        # it must be equal to the dimension index of a tested parameter
        if isinstance(refdim, float):
            if np.isnan(refdim):
                refdim = dimension
                dRes['refdim'] = refdim

        # If dimension is a string, check if the code of a dimension is correct
        if isinstance(dimension, str):
            if dimension == 'columns':
                pass
            elif dimension == 'rows':
                pass
            elif dimension == 'pages':
                pass
            else:
                strErrNote = '> %s < is an unknown code of a dimension!' % dimension
                raise ValueError(strErrNote)

        # If dimension is an integer, it must be higher than 0
        else:
            if (dimension < 0):
                strErrNote = 'Dimension index must be higher than 0!'
                raise ValueError(strErrNote)

        # If dimension is a string, decode it
        if isinstance(dimension, str):

            # If the parameter to be checked is a number or a tuple or a list:
            if isinstance(parVal, (int, float, tuple, list)):
                if dimension == 'columns':
                    iDim = 0
                    dimension = ''
                elif dimension == 'rows':
                    iDim = 1
                    dimension = ''
                elif dimension == 'pages':
                    iDim = 2
                    dimension = ''

            # If the parameter to be checked is a Numpy array:
            elif isinstance(parVal, np.ndarray):
                if dimension == 'columns':
                    iDim = parVal.ndim - 1
                    dimension == ' (columns) '
                elif dimension == 'rows':
                    iDim = parVal.ndim - 2
                    dimension == ' (rows) '
                elif dimension == 'pages':
                    iDim = parVal.ndim - 3
                    dimension == ' (pages) '
                else:
                    strErrNote = '> %s < is an unknown code of a dimension!' % dimension
                    raise ValueError(strErrNote)

                # All dimensions lower than 0 are -1
                if (iDim < 0):
                    iDim = -1
        else:
            iDim = dimension

            # Add name of a dimension, if it is a Numpy array
            if isinstance(parVal, np.ndarray):
                # Columns
                if (iDim == (parVal.ndim - 1)):
                    dimension = ' (columns) '

                # Rows
                elif (iDim == (parVal.ndim - 2)):
                    dimension = ' (rows) '

                # Pages
                elif (iDim == (parVal.ndim - 3)):
                    dimension = ' (pages) '

                # Uknown
                else:
                    dimension = ''

            # It is is not a Numpy array, there is no name for the dimension
            else:
                dimension = ''

        # Reference dimension:

        # If reference dimension is a string, check if the code of a dimension is correct
        if isinstance(refdim, str):
            if refdim == 'columns':
                pass
            elif refdim == 'rows':
                pass
            elif refdim == 'pages':
                pass
            else:
                strErrNote = '> %s < is an unknown code of a dimension!' % refdim
                ValueError(strErrNote)

        # If dimension is an integer, it must be higher than 0
        else:
            if (refdim < 0):
                strErrNote = 'Dimension index must be higher than 0!'
                ValueError(strErrNote)

        # If dimension is a string, decode it
        if isinstance(refdim, str):

            # If the parameter to be checked is a number or a tuple or a list:
            if isinstance(refVal, (int, float, tuple, list)):
                if refdim == 'columns':
                    iRefDim = 0
                    refdim = ''
                elif refdim == 'rows':
                    iRefDim = 1
                    refdim = ''
                elif refdim == 'pages':
                    iRefDim = 2
                    refdim = ''

            # If the parameter to be checked is a Numpy array:
            elif isinstance(refVal, np.ndarray):
                if refdim == 'columns':
                    iRefDim = refVal.ndim - 1
                    refdim = ' (columns) '
                elif refdim == 'rows':
                    iRefDim = refVal.ndim - 2
                    refdim = ' (rows) '
                elif refdim == 'pages':
                    iRefDim = refVal.ndim - 3
                    refdim = ' (pages) '

                # All dimensions lower than 0 are -1
                if (iRefDim < 0):
                    iRefDim = -1
        else:
            iRefDim = refdim
            # Add name of a dimension, if it is a Numpy array
            if isinstance(refVal, np.ndarray):
                # Columns
                if (iDim == (refVal.ndim - 1)):
                    refdim = ' (columns) '

                # Rows
                elif (iDim == (refVal.ndim - 2)):
                    refdim = ' (rows) '

                # Pages
                elif (iDim == (refVal.ndim - 3)):
                    refdim = ' (pages) '

                # Uknown
                else:
                    refdim = ''

            # It is is not a Numpy array, there is no name for the dimension
            else:
                refdim = ''

        return (iDim, iRefDim, bPedantic, dimension, refdim, dRes)

    def __checkDimSiz_dimSizInParam(self, parVal, iDim, bPedantic, strParName, strDesc, dRes):
        """
            Function gets the size of checked dimension of a tested parameter.

            Arguments:
                    parVal:                       the parameter to be checked
                    iDim          [number]        index of a dimension to be checked
                    bPedantic     [number]        'pedantic' flag
                    strParName:   [string]        name of the parameter to be checked
                    strDesc:      [string]        description of the parameter
                    dRes:         [dictionary]    dictionary with all the data for the restriction

            Output:
                    iDimSize      [number]        size of dimension

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        dimension = dRes['dimension']   # Get the dimension of a tested parameter

        # Parameter is a number
        if isinstance(parVal, (int, float)):
            if (iDim == 0):
                iDimSize = 1
            elif (bPedantic == 0):
                iDimSize = 1
            else:
                strError = 'Error in size restriction of dimension #%d for parameter > %s < (%s)!\n' % (iDim, strParName, strDesc)
                strError = strError + 13 * ' ' + 'Numbers do not have dimension #%d, and I was asked to be pedantic!\n' \
                    % (iDim)
                strError = strError + 13 * ' ' + '( > %s < (%s) is of type %s!)' % (strParName, strDesc, type(parVal))
                raise DimSizError(strError)

        # Parameter is a tuple or a list
        elif isinstance(parVal, (tuple, list)):
            if (iDim == 0):
                iDimSize = len(parVal)
            elif (bPedantic == 0):
                iDimSize = 1
            else:
                if isinstance(parVal, tuple):
                    strType = 'Tuples'
                else:
                    strType = 'Lists'
                strError = 'Error in size restriction of dimension #%d for parameter > %s < (%s)!\n' % (iDim, strParName, strDesc)
                strError = strError + 13 * ' ' + '%s do not have dimension #%d, and I was asked to be pedantic!\n' \
                    % (strType, iDim)
                strError = strError + 13 * ' ' + '( > %s < (%s) is of type %s!)' % (strParName, strDesc, type(parVal))
                raise DimSizError(strError)

        # Parameter is a Numpy array
        elif isinstance(parVal, np.ndarray):
            iNDimPar = parVal.ndim
            if ((iDim >= 0) and (iDim < iNDimPar)):
                iDimSize = parVal.shape[iDim]
            elif (bPedantic == 0):
                iDimSize = 1
            else:
                strError = 'Error in size restriction of dimension '
                if isinstance(dimension, str):
                    strError = strError + '\'%s\' for parameter > %s < (%s)!\n' % (dimension, strParName, strDesc)
                else:
                    strError = strError + '#%d for parameter > %s < (%s)!\n' % (dimension, strParName, strDesc)

                strError = strError + 13 * ' ' + 'Numpy array > %s < (%s) do not have dimension ' \
                    % (strParName, strDesc)
                if isinstance(dimension, str):
                    strError = strError + '\'%s\', and I was asked to be pedantic! \n' % (dimension)
                else:
                    strError = strError + '#%d, and I was asked to be pedantic! \n' % (dimension)
                raise DimSizError(strError)

        # Illegal type of a parameter
        else:
            strError = 'Only numbers, tuples, lists, and numpy arrays can have size restricted dimensions!\n'
            strError = strError + '            ( > %s < (%s) is of type: %s )' % (strParName, strDesc, type(parVal))
            raise TypeError(strError)

        return iDimSize

    def __checkDimSiz_dimSizInRef(self, strParName, strDesc, iDim, refVal, dRes, strRefName, iRefDim, bPedantic, strRes):
        """
            Function gets a reference for a restriction imposed on the size of dimension.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    iDim          [number]        index of dimension to be checked
                    refVal                        reference
                    dRes          [dictionary]    dictionary with all the data for the restriction
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
        """
        dimension = dRes['dimension']      # dimension code
        refdim = dRes['refdim']            # reference dimension 

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
            elif (bPedantic == 0):
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
            if ((iRefDim >= 0) and (iRefDim < iNDimRef)):
                iRefDimSize = refVal.shape[iRefDim]
            elif (bPedantic == 0):
                iRefDimSize = 1
            else:
                strError = 'Error in size restriction of dimension '
                if isinstance(dimension, str):
                    strError = strError + '\'%s\' for parameter > %s < (%s)!\n' % (dimension, strParName, strDesc)
                else:
                    strError = strError + '#%d for parameter > %s < (%s)!\n' % (dimension, strParName, strDesc)

                strError = strError + '            Reference %s do not have dimension ' % (strRefName)
                if isinstance(refdim, str):
                    strError = strError + '\'%s\', and I was asked to be pedantic!\n' \
                        % (refdim)
                else:
                    strError = strError + '#%d, and I was asked to be pedantic!\n' \
                        % (refdim)
                strError = strError + '            (Reference %s for > %s < is of type %s. )' \
                    % (strRefName, strParName, type(refVal))
                raise ValueError(strError)

        # Illegal type of the reference
        else:
            strError = 'Only numbers, lists, and numpy arrays can be a reference for restriction of size of dimension!\n'
            strError = strError + '            %s (restriction for > %s < ) is of type: %s)' \
                % (strRefName, strParName, type(refVal))
            raise ValueError(strError)

        return iRefDimSize

    def __checkDimSiz_engine(self, iDimSize, iRefDimSize, lCoeff, strRes):
        """
            Engine of check of restriction imposed on size of a dimension.

            Arguments:
                    iDimSize:         [number]         size of a dimensions in a checked parameter
                    iRefDimSize:      [number]         reference
                    lCoeff            [list]           list with 'mul' and 'add' coefficients
                    strRes            [string]         restriction, allowed values:
                                                       'dimension size equal to', 'dimension size higher than',
                                                       'dimension size lower than', 'dimension size higher or equal to',
                                                       'dimension size lower or equal to'
            Output:
                    1 - restriction correct
                    0 - restriction incorrect

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        iMul = lCoeff[0]     # Take the linear coefficients
        iAdd = lCoeff[1]     # Take the linear coefficients

        iRefDimSize = iMul * iRefDimSize + iAdd   # Apply the linear coefficients

        if (strRes == 'dimension size equal to'):
            return (iDimSize == iRefDimSize)
        elif (strRes == 'dimension size higher than'):
            return (iDimSize > iRefDimSize)
        elif (strRes == 'dimension size lower than'):
            return (iDimSize < iRefDimSize)
        elif (strRes == 'dimension size higher or equal to'):
            return (iDimSize >= iRefDimSize)
        elif (strRes == 'dimension size lower or equal to'):
            return (iDimSize <= iRefDimSize)
        else:
            strError = '%s is an unknown type of a relation!' % strRes
            raise RuntimeError(strError)

    def __checkDimSiz_error(self, strParName, strDesc, parVal, strRefName, refVal, dRes, strErrNote, strRes, iDimSize, iRefDimSize):
        """
            Function raises an error if a restriction imposed on the size of dimensions was broken.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    parVal:                       the parameter to be checked
                    strRefName    [string]        name of a reference
                    refVal                        value of a reference
                    dRes          [dictionary]    dictionary with all the data for the restriction
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
        """
        # If error note was given, use it
        if not (strErrNote == ''):
            raise DimSizError(strErrNote)

        dimension = dRes['dimension']      # dimension code
        refdim = dRes['refdim']            # reference dimension

        # Get indices and names of dimensions which was checked
        (iDim, iRefDim, _, dimension, refdim, dRes) = self.__checkDimSiz_dimensions(parVal, refVal, dRes)

        # Change linear coefficients into strings
        lCoeff = dRes['coeff']             # List with coefficients
        (strMul, strAdd) = self.__linearCoef2Strings(lCoeff)

        # Invoke the error:

        # Index of a dimension was given
        if isinstance(dimension, int):
            strErrNote = 'Parameter > %s < (%s) must have the size of dimension #%d%s%s' \
                % (strParName, strDesc, iDim, dimension, self.__checkDimSiz_error_restriction(strRes))

        # Name of a dimension was given
        else:

            # Requested dimension exists in a parameter
            if (iDim >= 0):  #
                strErrNote = 'Parameter > %s < (%s) must have the number of %s (dimension #%d) %s' \
                    % (strParName, strDesc, dimension, iDim, self.__checkDimSiz_error_restriction(strRes))
            else:
                strErrNote = 'Parameter > %s < (%s) must have the number of %s %s' \
                    % (strParName, strDesc, dimension, self.__checkDimSiz_error_restriction(strRes))

        # Construct the requirement:

        # If the reference is a number it is easy to construct the error info...
        if isinstance(refVal, (int, float)):

            # Reference was given as a direct number
            if (self.__strOnlyNumb(strRefName)):

                # No linear coefficients
                if (strMul == '') and (strAdd == ''):   # Only numbers and no linear coefficients
                    strErrNote = strErrNote + '%s!\n' % (strRefName)

                else:
                    strErrNote = strErrNote + ': %s%s%s (=%s)!\n' \
                        % (strMul, strRefName, strAdd, self.__n2s(lCoeff[0] * refVal + lCoeff[1]))

            # Reference was a size of a dimension of another parameter
            else:
                # No linear coefficients
                if (strMul == '') and (strAdd == ''):   # Only numbers and no linear coefficients
                    strErrNote = strErrNote + 'the value of %s (=%s)!\n' % (strRefName, refVal)

                else:
                    strErrNote = strErrNote + ': %sthe value of %s%s (%s%s%s = %s)!\n' \
                        % (strMul, strRefName, strAdd, strMul, refVal, strAdd, self.__n2s(lCoeff[0] * refVal + lCoeff[1]))

        # Reference was the size of a dimension of a tuple or list
        elif isinstance(refVal, (tuple, list)):
            if (iRefDim == 0):

                # No linear coefficients
                if (strMul == '') and (strAdd == ''):   # Only numbers and no linear coefficients
                    strErrNote = strErrNote + 'the size of %s (=%d)!\n' % (strRefName, iRefDimSize)

                else:
                    strErrNote = strErrNote + ': %sthe size of %s%s (%s%s%s = %s)!\n' \
                        % (strMul, strRefName, strAdd, strMul, iRefDimSize, strAdd, self.__n2s(lCoeff[0] * iRefDimSize + lCoeff[1]))

            else:
                # No linear coefficients
                if (strMul == '') and (strAdd == ''):   # Only numbers and no linear coefficients
                    strErrNote = strErrNote + 'dimension #%d of %s!\n' % (iRefDim, strRefName)
                    strErrNote = strErrNote + 13 * ' ' + '(Dimension #%d in %s  does not exist...so it is assumed = 1)!\n' % (iRefDim, strRefName)

                else:
                    strErrNote = strErrNote + ': %sdimension #%d of %s%s (%s%s%s = %s)!\n' \
                        % (strMul, iRefDim, strRefName, strAdd, strMul, self.__n2s(iRefDimSize), strAdd, self.__n2s(lCoeff[0] * iRefDimSize + lCoeff[1]))
                    strErrNote = strErrNote + 13 * ' ' + '(Dimension #%d in %s  does not exist...so it is assumed = 1)!\n' % (iRefDim, strRefName)

        # Reference was a Numpy array
        else:
            # Index of the reference dimension was given
            if isinstance(refdim, int):

                # No linear coefficients
                if (strMul == '') and (strAdd == ''):   # Only numbers and no linear coefficients
                    strErrNote = strErrNote + 'dimension #%d%s of %s (=%d)!\n' % (iRefDim, refdim, strRefName, iRefDimSize)
                else:
                    strErrNote = strErrNote + ': %sdimension #%d%s of %s%s (%s%s%s = %s)!\n' \
                        % (strMul, iRefDim, refdim, strRefName, strAdd, strMul, self.__n2s(iRefDimSize), strAdd, self.__n2s(lCoeff[0] * iRefDimSize + lCoeff[1]))

            # Name of the rteference dimension was given
            else:
                # No linear coefficients
                if (strMul == '') and (strAdd == ''):   # Only numbers and no linear coefficients
                    strErrNote = strErrNote + 'the number of %s in %s (=%d)!\n' % (refdim, strRefName, iRefDimSize)

                else:
                    strErrNote = strErrNote + ': %sthe number of %s of %s%s (%s%s%s = %s)!\n' \
                        % (strMul, refdim, strRefName, strAdd, strMul, self.__n2s(iRefDimSize), strAdd, self.__n2s(lCoeff[0] * iRefDimSize + lCoeff[1]))

        # Construct the info about the size of a dimension of a parameter:

        # Index of a dimension was given
        if isinstance(dimension, int):
            strErrNote = strErrNote = strErrNote + 13 * ' ' + 'The size of a dimension #%d of parameter > %s < is %d!' \
                % (iDim, strParName, iDimSize)

        # Name of a dimension was given
        else:
            strErrNote = strErrNote = strErrNote + 13 * ' ' + 'The number of %s in parameter > %s < is %d!' \
                % (dimension, strParName, iDimSize)

        raise DimSizError(strErrNote)

    def __checkDimSiz_error_restriction(self, strRel):
        """
            Function changes string 'dimension size [relation]' into '[relation]'.
            This function is used to construct an error message.

            Arguments:
                    strRel      [string]          string to be transformed

            Output:
                    strRel      [string]          transformed string

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk

            Last modification:
                    19 June 2015
        """
        if (strRel == 'dimension size equal to'):
            return 'equal to '
        elif (strRel == 'dimension size higher than'):
            return 'higher than '
        elif (strRel == 'dimension size lower than'):
            return 'lower than '
        elif (strRel == 'dimension size higher or equal to'):
            return 'higher or equal to '
        elif (strRel == 'dimension size lower or equal to'):
            return 'lower or equal to '
            
    def  __checkUnique(self, strParName, strDesc, parVal, dRes):
        """
            Function checks restriction imposed on uniqness of elements of a parameter.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of the parameter
                    parVal:                       the parameter to be checked
                    dRes:         [dictionary]    dictionary with all the data for the restriction
            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """

        strErrNote = dRes['strErrNote']    # Get the error note
                
        # Parameter is a tuple or a list
        if isinstance(parVal, (tuple, list)):

            # Check if all the elements are numbers, lists or strings
            self.__checkUnique_elTypeCheck(parVal)

            parValUnique = list(set(parVal))  # Create a list with only unique elements
            if len(parValUnique) != len(parVal):
                self.__checkUnique_error(strParName, strDesc, len(parValUnique), len(parVal), strErrNote)

        # Parameter is a Numpy array
        elif isinstance(parVal, np.ndarray):
            
            # If the Numpy array is empty, there is nothing to be checked
            if parVal.size == 0:
                return
            
            # Check if all the elements are numbers, lists or strings
            self.__checkUnique_elTypeCheck(parVal)            

            parVal.shape = (parVal.size, )      # Change the parameter to 1-dim
            parValUnique = np.unique(parVal)    # 
            
            if (parValUnique.size != parVal.size):
                self.__checkUnique_error(strParName, strDesc, parValUnique.size, parVal.size, strErrNote)

        # Parameter is of illegal type for uniqness check
        else:
            strError = ('Uniqness check can be assigned only to tuples, lists and Numpy arrays!\n')
            strError = strError + ('            Parameter > %s < (%s) is of type %s') \
                % (strParName, strDesc, type(parVal))
            raise ValueError(strError)

    def __checkUnique_elTypeCheck(self, parVal):
        """
            Function checks if a parameter which is supposed to be checked for 
            uniqness contains only allowed elements (numbers or strings).

            Arguments:
                    parVal:   [list/tuple/Numpy array]   parameter to be checked

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        # Parameter is a tuple or a list
        if isinstance(parVal, (tuple, list)):
            for iEl in parVal:
                if not isinstance(iEl, (int, float, str)):
                    strError = 'Parameter checked for uniqness must contain only numbers or strings!'
                    raise ValueError(strError)
                    
        # Parameter is a Numpy array                 
        else:
            parVal.shape = (parVal.size, )  # Change the parameter to 1-dim
            if not isinstance(parVal[0], (int, float, str)):
                strError = 'Parameter checked for uniqness must contain only numbers or strings!'
                raise ValueError(strError)


    def __checkUnique_error(self, strParName, strDesc, iParSize, iUniqParSize, strErrNote):            
        """
            Function raises an error if a restriction imposed on the uniqness is broken.

            Arguments:
                    strParName:   [string]        name of a parameter
                    strDesc:      [string]        description of a parameter
                    iParSize      [number]        size of parameter which was checked
                    iUniqParSize  [number]        the number of uniqe elements
                    strErrNote    [string]        error note to be displayed if the restriction is broken
                                                  (might be empty, then a default note is generated)

            Output:
                    none

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        if strErrNote != '':
            raise UniqnessError(strErrNote)
            
        strError = ('Parameter > %s < (%s) of size = %d contains only %d unique elements!') \
            % (strParName, strDesc, iUniqParSize, iParSize)            
        raise UniqnessError(strError)


    def __getReference(self, dRes):
        """
            This function gets the value of the reference and name of 
            the reference based on the reference data in dRes dictionary.

            Arguments:
                    dRes   [dictionary]        the dictionary with restriction

            Output:
                    refVal          value of the reference
                    strRefNamae     name of the reference

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        
        if not 'reference' in dRes:
            # If reference does not exist, it means we do not need it
            # But a restriction check function may have a different opinion....
            refVal = np.nan
            strRefName = '> (empty) <'
            return (refVal, strRefName)
            
        reference = dRes['reference']     # Get the reference name

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
            refVal = reference                        # value

            # string with name of the reference
            if isinstance(reference, float):
                strRefName = ('%s') % self.__n2s(reference)   # float
            elif isinstance(reference, int):
                strRefName = ('%s') % self.__n2s(reference)   # int
            elif isinstance(reference, tuple):
                strRefName = 'the given tuple'          # tuple
            elif isinstance(reference, list):
                strRefName = 'the given list'           # list
            elif isinstance(reference, np.ndarray):
                strRefName = 'the given numpy array'    # numpy array
            else:
                strRefName = 'the given variable'      # everythin else

        return (refVal, strRefName)


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
        """

        iMul = lResData[0]     # Take the linear coefficients
        iAdd = lResData[1]     # Take the linear coefficients

        # Change linear coefficients into strings
        if (iMul == 1):
            strMul = ''
        else:
            strMul = '%s * ' % self.__n2s(iMul)
        if (iAdd == 0):
            strAdd = ''
        elif (iAdd < 0):
            strAdd = ' - %s' % self.__n2s(abs(iAdd))
        else:
            strAdd = ' + %s' % self.__n2s(iAdd)

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
        """

        if isinstance(iX, int):
            strX = ('%d') % iX
            return strX

        iMaxDigits = 24  # Maximum precision
        for iPrec in range(1, iMaxDigits + 1):
            strFormat = ('%%.%df') % iPrec          # Change the numer to
            strEval = ('\'%s\' %% iX') % strFormat  # a string
            strX = eval(strEval)                    # ^

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

    def __strOnlyNumb(self, strString):
        """
            Function checks if a given string contains only a number.
            Arguments:
                    strString [str]    a string to be checked

            Output:
                    1            only numbers
                    0            something else beside a number

            Author:
                    Jacek Pierzchlewski jap@es.aau.dk
        """
        for c in strString:
            if ((c == '0') or (c == '1') or (c == '2') or (c == '3') or (c == '4') or (c == '5') or
               (c == '6') or (c == '7') or (c == '8') or (c == '9') or (c == '.') or (c == '-')):
                continue
            else:
                return 0
        return 1
        
    def isequal(self, iX, iY, iMargin):
        """
        This function checks if a difference between two values is in the
        given allowed margin.

        Args:
            iX: the first value |br|
            iY: the second value |br|
            iMargin: the allowed margin |br|
    
        Returns:
            1: if the difference between the given values does not exceed the
               given margin |br|
            0: if the difference between the given values does exceed the
               given margin |br|
        """
        
        iTSM = 1e-21  # Too small margin
        bTooSmall = (0 < iX < iTSM) or (0 < iY < iTSM) or (0 < iMargin < iTSM)
        if bTooSmall == 1:  # <- very small values may create problems due to
                            #    floating point representation problems
            return 1
       
        if (abs(iX - iY) <= abs(iMargin)):
            return 1
        else:
            return 0
        

class ErrorTemplate(Exception):
    """
        Error template for the local errors.
    """
    def __call__(self, *args):
        return self.__class__(*(self.args + args))


class ParameterMissingError(ErrorTemplate):
    """
        Error: Parameter missing
    """
    pass


class ParameterTypeError(ErrorTemplate):
    """
        Error: Parameter type
    """
    pass


class ElementTypeError(ErrorTemplate):
    """
        Error: Parameter element type
    """
    pass


class AllowedValuesError(ErrorTemplate):
    """
        Error: Allowed values of a parameter
    """
    pass


class RelationalError(ErrorTemplate):
    """
        Error: Parameter value (relational)
    """
    pass


class SizeError(ErrorTemplate):
    """
        Error: Parameter size
    """
    pass


class NDimError(ErrorTemplate):
    """
        Error: The number of dimensions
    """
    pass


class DimSizError(ErrorTemplate):
    """
        Error: Dimension size
    """
    pass

class UniqnessError(ErrorTemplate):
    """
        Error: Uniqness of elements
    """
    pass
