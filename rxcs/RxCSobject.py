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
                    strName: [string]   name of the parameter, will become public class member
                    strDesc: [string]   short description of the parameter
                    unit:    [string]   unit of the parameter
                    noprint: [int]      switch off priting the parameter to the console by 'parametersPrint' function
                                        (optional, default is 0 = print the parameter)

                    unitprefix [string] prefered unit prefix of a parameter to be printed
                                        (optional, default is - = CPU decides,
                                        allowed values = f:femto, p:pico, n:nano, u:micro, m:mili,
                                        ' ':one, k:kilo, M:mega, G:giga, T:tera)

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
        dParameter['bNaNAllowed'] = 0               # NaN is not allowed for mandatory parameters        
        dParameter['bNaNAllowedEl'] = 0             # By default NaN elements are not allowed
        dParameter['lRes'] = []                     # List of restriction
        dParameter['lResErrNote'] = []              # List of error notes for restrictions
        dParameter['lResReference'] = []            # List of references for restrictions
        dParameter['lResData'] = []                 # List of additional data for restrictions

        self.lParameters.append(dParameter)
        
        self.iManParam = self.iManParam + 1  # The number of mandatory parameters


    def paramAddOpt(self, strName, strDesc, unit='', noprint=0, unitprefix='-', default=0):
        """
            Add an optional parameter to the object.
    
            Arguments:
            Arguments:
                    strName: [string]   name of the parameter, will become public class member
                    strDesc: [string]   short description of the parameter
                    unit:    [string]   unit of the parameter
                    noprint: [int]      switch off priting the parameter to the console by 'parametersPrint' function
                                        (optional, default is 0 = print the parameter)
                                    
                    unitprefix [string] prefered unit prefix of a parameter to be printed
                                        (optional, default is - = CPU decides,
                                        allowed values = f:femto, p:pico, n:nano, u:micro, m:mili,
                                        ' ':one, k:kilo, M:mega, G:giga, T:tera)
                    default             default value
                                        (optional, by default it is 0)

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
        dParameter['bNaNAllowed'] = 1               # NaN is allowed for optional arguments
        dParameter['bNaNAllowedEl'] = 0             # By default NaN elements are not allowed
        dParameter['lResErrNote'] = []              # List of error notes for restrictions
        dParameter['lResReference'] = []            # List of references for restrictions
        dParameter['lResData'] = []                 # List of additional data for restrictions
 
        self.lParameters.append(dParameter)        

        self.iOptParam = self.iOptParam + 1  # The number of optional parameters

    
    def __isParameterNameOK(self, strName):
        """
            Check if a name of the parameter is correct.
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


    def NaNAllowedEl(self, strName):

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
            If types are assigned, it will be checked if elements of the parameter 
            are of correct types.
            It will be checked only if the parameter is of type:
            
                - list
                - tuple
                - numpy array
                                
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
            raise ValueError('Allowed types of elements of parameter must be a type, a tuple of types, or a list of types!')
        
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


    def paramAllowed(self, strName, lAllowed, errnote=''):

        # Error checks -------------------------------------------------------
        
        # Parameter to be checked        
        if not isinstance(strName, str):
            raise ValueError('Name of a parameter must be a string!')

        (bDefined, inxParam) = self.__parameterWasDefined(strName)
        if not bDefined:
            strError = ('Parameter > %s < was not yet defined!') % strName
            raise RuntimeError(strError)

        # List of allowed values
        if not isinstance(lAllowed, list):                       
             raise ValueError('Allowed values must be grouped in a list!')
             
        # Error note
        if not isinstance(errnote, str):
            raise ValueError('Error note must be a string!')

        #---------------------------------------------------------------------
        self.lParameters[inxParam]['lRes'].append('paramAllowed')
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
        self.__paramAddRelRestriction('paramH', strName, reference, mul, add, errnote)


    def paramL(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - lower than a reference 

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
        self.__paramAddRelRestriction('paramL', strName, reference, mul, add, errnote)


    def paramHE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - higher or equal to a reference 
                                            
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
        self.__paramAddRelRestriction('paramHE', strName, reference, mul, add, errnote)


    def paramLE(self, strName, reference, mul=1, add=0, errnote=''):
        """
            Assign relational restriction to a parameter - lower or equal to a reference 
                                            
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
        self.__paramAddRelRestriction('paramLE', strName, reference, mul, add, errnote)


    def __paramAddRelRestriction(self, strResCode, strName, reference, iMul, iAdd, strErrNote):
        """
            Assign relational restriction to a parameter
                                            
            Arguments:
                    
                    strResCode:   [string]          code of the restriction
                    strName:      [string]          name of the parameter
                    reference:    [string/number]   reference, it can be a number or a name of another parameter
                    iMul:         [number]          multiply coefficient, reference will be multipled by this 
                    iAdd:         [number]          add coefficient, will be added to a reference AFTER multiplication by mul
                    errnote       [string]          optional error note, will be displayed if the restriction is broken
            
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
            raise ValueError('Reference must be a string, a real number, a tuple, a list or a numpy array!')
        if isinstance(reference, float) :
            if np.isnan(reference): 
                raise ValueError('Reference must not be nan!')

        #---------------------------------------------------------------------
        self.lParameters[inxParam]['lRes'].append(strResCode)
        self.lParameters[inxParam]['lResErrNote'].append(strErrNote)
        self.lParameters[inxParam]['lResReference'].append(reference)
        self.lParameters[inxParam]['lResData'].append([iMul, iAdd])

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


    def parametersProcess(self, *args):
        """
            Process the parameters given to a function as arguments.
                                            
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


    def parametersCheck(self):
        """
            Function checks the parameters.            
     
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
                    strError = ('Mandatory parameter >%s< is not given!') % strParName
                    raise ValueError(strError)


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
            lTypes = self.lParameters[inxPar]['lTypes']        # Allowed types of the current parameter
            parameter = self.__dict__[strParName]              # Get the parameter

            # Check the type
            if not (isinstance(parameter,tuple(lTypes))):
                strError = ('Type %s is incorrect for parameter >%s< !') % (type(parameter), strParName)
                raise ValueError(strError)
            
            # Check types of elements, if needed
            if isinstance(parameter, (np.ndarray, list, tuple)):
                if not 'lTypesEl' in self.lParameters[inxPar]:
                    continue
                lTypesEl = self.lParameters[inxPar]['lTypesEl']   # Allowed types of elements of the current parameter

                # Service for numpy array
                if isinstance(parameter, np.ndarray):
                    if (parameter.size > 0):
                        if not (isinstance(parameter[0], tuple(lTypesEl))):
                            strError = ('Parameter >%s< contains elements of an illegal type (%s)!') \
                                % (strParName, type(parameter[0]))
                            raise ValueError(strError)
                    return

                # Service for a tuple or a list
                for inxEl in range(len(parameter)):       # Loop over all elements of the current parameter
                    if not (isinstance(parameter[inxEl], tuple(lTypesEl))):
                        strError = ('Parameter >%s< on position %d contains an element of an illegal type (%s)!') \
                            % (strParName, inxEl, type(parameter[inxEl]))
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
        parVal = self.__dict__[strParName]      # The parameter itself

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
                    # If reference is an empty string it means we do not need it
                    pass
            else:
                refVal=reference                        # value
                
                # string with name of the reference
                if isinstance(reference, float):         
                    strRefName = ('%f') % (reference)   # float
                elif isinstance (reference, int):
                    strRefName = ('%d') % (reference)   # int
                elif isinstance (reference, tuple):     
                    strRefName = 'the given tuple'          # tuple
                elif isinstance (reference, list):     
                    strRefName = 'the given list'           # list
                elif isinstance (reference, np.ndarray):     
                    strRefName = 'the given numpy array'    # numpy array

            # Run the correct parameter restriction check function
            if (strRes == 'paramAllowed'):
                self.__parameterRestrictionAllowed(strParName, strDesc, parVal, lResData, strErrNote, bNaNAllowedEl)                
            elif (strRes == 'paramH'):
                self.__parameterRestrictionRel(strParName, strDesc, parVal, strRefName, refVal, lResData, strErrNote, 'higher than', bNaNAllowedEl)
            elif (strRes == 'paramHE'):
                self.__parameterRestrictionRel(strParName, strDesc, parVal, strRefName, refVal, lResData, strErrNote, 'higher or equal to', bNaNAllowedEl)
            elif (strRes == 'paramL'):
                self.__parameterRestrictionRel(strParName, strDesc, parVal, strRefName, refVal, lResData, strErrNote, 'lower than', bNaNAllowedEl)
            elif (strRes == 'paramLE'):
                self.__parameterRestrictionRel(strParName, strDesc, parVal, strRefName, refVal, lResData, strErrNote, 'lower or equal to', bNaNAllowedEl)
            else:
                raise RuntimeError('Something went seriously wrong...[internal RxCSobject error]')


    def __parameterRestrictionAllowed(self, strParName, strDesc, parVal, lAllVal, strErrNote, bNaNAllowedEl):
        """
            Function checks the 'allowed values' restriction of a parameter.

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
                    29 may 2015
        """
        # -------------------------------------------------------------------
        # Error check
        type(parVal)
        if not isinstance(parVal, (float, int, str, tuple, list, np.ndarray)):
            strError = 'Only numbers, strings, tuples, lists, and numpy arrays can be restricted with allowed values!'
            strError = strError+'(>%s< is of type: %s)' % (strParName, type(parVal))
            raise ValueError(strError)
        # -------------------------------------------------------------------

        # Run the correct function dependently on the parameter type
        if isinstance(parVal, (str, float, int)):
            self.__parameterRestrictionAllowed_numstr(strParName, strDesc, parVal, lAllVal, strErrNote)
        else:
            self.__parameterRestrictionAllowed_atl(strParName, strDesc, parVal, lAllVal, strErrNote, bNaNAllowedEl)
        return


    def __parameterRestrictionAllowed_numstr(self, strParName, strDesc, parVal, lAllVal, strErrNote):

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
                strErrNote = ('%s is an incorrect value for parameter > %s < (\'%s\')') % (self.__n2s(parVal), strParName, strDesc)
            elif isinstance(parVal, (str)):
                strErrNote = ('%s is an incorrect value for parameter > %s < (\'%s\')') % (parVal, strParName, strDesc)
        raise ValueError(strErrNote)


    def __parameterRestrictionAllowed_atl(self, strParName, strDesc, parVal, lAllVal, strErrNote, bNaNAllowedEl):
        
        inxEl = 0  # Reset the index of elements in tuple, list or a numpy array              
        
        # Loop over all elements of the parameter
        for par in parVal:
            
            # An element of the tested parameter must be either a string or a number            
            if not isinstance(par, (str, float, int)):
                strError = 'Only number or string elements can be restricted with allowed values!\n'
                strError = strError+'            Element #%d of > %s < (%s) is of type %s' \
                    % (inxEl, strParName, strDesc, type(par))
                raise ValueError(strError)
                raise ValueError(strErrNote)

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
            raise ValueError(strErrNote)
        return
        
        
    def __parameterRestrictionRel(self, strParName, strDesc, parVal, strReference, refVal, lCoef, strErrNote, strRelation, bNaNAllowedEl):
        """
            Function checks the 'higher than', 'higher or equal to', 'lower than', 'lower or equal to' 
            relative restriction of a parameter.

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
        # -------------------------------------------------------------------
        # Error check
        if not isinstance(parVal, (float, int, tuple, list, np.ndarray)):
            strError = 'Only numbers, lists, tuples and numpy arrays can be restricted \'%s...\'! '  % (strRelation)
            strError = strError+'(>%s< is of type: %s)' % (strParName, type(parVal))
            raise ValueError(strError)

        # -------------------------------------------------------------------

        # Switch to correct function dependently on type of the parameter:
        if isinstance(parVal, (float, int)):
            self.__parameterRestrictionRel_num(strParName, strDesc, parVal, strReference, refVal, lCoef, strErrNote, strRelation)
        else:
            self.__parameterRestrictionRel_atl(strParName, strDesc, parVal, strReference, refVal, lCoef, strErrNote, strRelation, bNaNAllowedEl)

        return

        # -------------------------------------------------------------------

    def __parameterRestrictionRel_num(self, strParName, strDesc, parVal, strReference, refVal, lCoef, strErrNote, strRelation):

        # -------------------------------------------------------------------
        # Error check    
        if not isinstance(refVal, (float, int)):
            strError = 'Only numbers can be a reference for restriction \'%s...\' for numbers!\n' % (strRelation)
            strError = strError+'                 (>%s< is of type: %s)' % (strReference, type(refVal))
            raise ValueError(strError)

        # -------------------------------------------------------------------
        
        # If reference is NaN, restriction can not be checked, it is assumed that the value is correct
        if isinstance(refVal, float):
            if np.isnan(refVal):
                return

        iMul = lCoef[0]     # Take the linear coefficients
        iAdd = lCoef[1]     # Take the linear coefficients 

        # Check the restriction
        bError = 0
        if (strRelation == 'higher than'):
            if not (parVal > refVal*iMul + iAdd):
                bError = 1
        elif (strRelation == 'higher or equal to'):
            if not (parVal >= refVal*iMul + iAdd):
                bError = 1
        elif (strRelation == 'lower than'):
            if not (parVal < refVal*iMul + iAdd):
                bError = 1
        elif (strRelation == 'lower or equal to'):
            if not (parVal <= refVal*iMul + iAdd):
                bError = 1
        else:
            strError = '%s is an unknown type of a relation!' % strRelation
            raise RuntimeError(strError)

        # Throw the error, if needed
        if (bError == 1):
            if strErrNote == '':
                if (iMul == 1):
                    strMul = ''
                else:
                    strMul = '%s *' % self.__n2s(iMul)
                if (iAdd == 0):
                    strAdd = ''
                else:
                    strAdd = '+ %s' % self.__n2s(iAdd)
           
                strErrNote = '%s > %s < must be %s %s %s %s!' \
                    % (strDesc, strParName, strRelation, strMul, strReference, strAdd)
            raise ValueError(strErrNote)

        return


    def __parameterRestrictionRel_atl(self, strParName, strDesc, parVal, strRefName, refVal, lCoef, strErrNote, strRelation, bNaNAllowedEl):
        
        # -------------------------------------------------------------------
        # Error check        
        
        # Take the lenght of the checked parameter        
        if isinstance(parVal, np.ndarray):
            iLen = parVal.size
        else:
            iLen = len(parVal)
            
        # Take the lenght and type of the reference
        if isinstance(refVal, tuple):
            iLenRef = len(refVal)
            strRefType = 'Tuple'
            strDelimStart = '('
            strDelimLast = ')'
  
        elif isinstance(refVal, list):
            iLenRef = len(refVal)            
            strRefType = 'List'
            strDelimStart = '['
            strDelimLast = ']'
        elif isinstance(refVal, np.ndarray):
            iLenRef = refVal.size
            strRefType = 'Numpy array'
            strDelimStart = '['
            strDelimLast = ']'
        elif isinstance(refVal, (float, int)):
            # If reference is NaN, restriction can not be checked, it is assumed that the value is correct
           if np.isnan(refVal):
                return 
        else:
            strError = 'Only numbers, lists, tuples and numpy arrays can be a reference for restriction \'%s...\'!\n' % (strRelation)
            strError = strError+'       (>%s< is of type: %s)' % (strRefName, type(refVal))
            raise ValueError(strError)
            
        # Compare the lenghts with the lenght of the reference, if the reference is a list, a tuple or a numpy array
        if isinstance(refVal, (list, tuple, np.ndarray)):
            if not (iLen == iLenRef):
                strError = '%s reference must be of equal size to the restricted parameter!\n' % strRefType
                strError = strError+'            Parameter > %s < is of size %d, its reference (%s) is of size %d!' \
                    % (strParName, iLen, strRefName, len(refVal))
                raise ValueError(strError)
                
        # -------------------------------------------------------------------

        iMul = lCoef[0]     # Take the linear coefficients
        iAdd = lCoef[1]     # Take the linear coefficients

        # Check the restriction
        bError = 0               # Restriction error flag
        bParTypeError = 0        # Error of parameter element type
        bRefTypeError = 0        # Error of reference element type        
        inxElErr = -1            # Index of an element with error

        # Vectorize the parameter, if it is a numpy array
        if isinstance(parVal, np.ndarray):
            parVal.shape = (parVal.size, )

        # Vectorize the reference, if it is a numpy array
        if isinstance(refVal, np.ndarray):
            refVal.shape = (refVal.size, )

        # Check the restriction:
        if isinstance(refVal, (int, float)):        # Check for number reference
            # Loop over all elements in the checked parameter             
            for inxEl in range(len(parVal)):
                # Get the current element of the checked parameter and check if it is a number                                
                parEl = parVal[inxEl]
                if not isinstance(parEl, (float, int)):
                    bParTypeError = 1
                    inxElErr = inxEl    
                    break

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
                if not (self.__relation(parEl, refVal*iMul + iAdd, strRelation)):
                    bError = 1
                    inxElErr = inxEl
                    break
        else:              # Check for tuple, list, numpy array reference
            # Loop over all elements in the checked parameter             
            for inxEl in range(len(parVal)):
                
                # Get the current element of the checked parameter and check if it is a number                
                parEl = parVal[inxEl]
                if not isinstance(parEl, (float, int)):                        
                    bParTypeError = 1
                    inxElErr = inxEl
                    break

                # Check if the current elements of the checked parameter is NaN
                if isinstance(parEl, float):
                    if np.isnan(parEl):
                        if (bNaNAllowedEl == 1):
                            continue
                        else:
                            strError = 'Element %d of > %s < (%s) is NaN, which is not allowed!' \
                                % (inxEl, strParName, strDesc)
                            raise ValueError(strError)

                # Get the current element of the reference and check if it is a number                                                
                refEl = refVal[inxEl]
                if not isinstance(refEl, (float, int)):                        
                    print(inxEl)        
                    bRefTypeError = 1
                    inxElErr = inxEl
                    break
                # Check if the reference element is NaN. If it is, continue
                if isinstance(refEl, float):
                    if np.isnan(refEl):
                        continue

                # Check the reference                                
                if not (self.__relation(parEl,refEl*iMul + iAdd, strRelation)):
                    bError = 1
                    inxElErr = inxEl               
                    break

        # Throw the error of parameter element type , if it was found above
        if (bParTypeError == 1):
            strError = 'Only numbers can be checked for restriction  \'%s...\'!\n'  % (strRelation)
            strError = strError+'            Element #%d of > %s < is of type %s!' % (inxEl, strParName, type(parEl))
            raise ValueError(strError)
    
        # Throw the error pf reference parameter element type , if it was found above
        if (bRefTypeError == 1):
            strError = 'Only numbers can be a reference for restriction  \'%s...\'!\n'  % (strRelation)
            strError = strError+'            Element #%d of %s (reference for > %s< ) is of type %s!' \
                % (inxEl, strRefName, strParName, type(refEl))
            raise ValueError(strError)

        # Retrun from function if the relational error was not found
        if bError == 0:
            return 
            
        # Throw out an error, if the error note was already given            
        if not (strErrNote == ''):
            raise ValueError(strErrNote)

        # Construct the error note:

        # Firstly, change linear coefficients into strings
        if (iMul == 1):
            strMul = ''
        else:
            strMul = '%s *' % self.__n2s(iMul)
        if (iAdd == 0):
            strAdd = ''
        else:
            strAdd = '+ %s' % self.__n2s(iAdd)
        
        # If the reference is a number it is easy to construct the error info... 
        if isinstance(refVal, (int, float)):
            strErrNote = 'All elements of %s > %s < must be %s %s %s %s! (error on element # %d)!' \
                % (strDesc, strParName, strRelation, strMul, strRefName, strAdd, inxElErr)
            raise ValueError(strErrNote)
                
        # If the reference is an array, a tuple or a list, it is getting complicated... 
        if (strMul == '') and (strAdd == ''):
            strErrNote = 'Elements of > %s < (%s) must be %s the corresponding elements of %s' \
                % (strParName, strDesc, strRelation, strRefName)
        else:
            strErrNote = 'Elements of > %s < (%s) must be %s %s x %s, where x are the corresponding elements of %s' \
                % (strParName, strDesc, strRelation, strMul, strAdd, strRefName)
        
        # Print the reference if its size is lower than 10
        if (iLenRef <= 10):
            strErrNote = strErrNote + ' %s' % strDelimStart
            for el in refVal:
                strErrNote = strErrNote + ' %s' % self.__n2s(el)
            strErrNote =  strErrNote + ' %s' % strDelimLast
            strErrNote = strErrNote + '!\n'
            
        # Add info about the element which brakes the restriction                  
        strErrNote=strErrNote+'            Element #%d of > %s < is %s, element #%d of %s is %s!' \
            % (inxEl, strParName, self.__n2s(parVal[inxEl]), inxEl, strRefName, self.__n2s(refVal[inxEl]))
        
        # Ok, throw out an error            
        raise ValueError(strErrNote)


    def __relation(self, iPar, iRef, strRelation):

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
            It is assumed that the leemnts are indexed starting from 0
  
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


    def parametersPrint(self):
        """
            Function prints parameters of the module.

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
                iPar = self.__dict__[strParName]             # The parameter itself
                
                # Run the correct function dependently on the type of the parameter           
                if isinstance(iPar,(int, float)):
                    rxcs.console.bullet_param(strDesc, iPar, strUnitPrefix, strUnit)
                elif isinstance(iPar,str):
                    rxcs.console.bullet_info(strDesc,iPar)
        print('')
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
        if self.bMute == 0:
            strName = ('%s: \'%s\' is starting') % (self.strRxCSgroup, self.strModuleName) 
            self.tStart = rxcs.console.module_progress(strName)


    def engineStopsInfo(self):
        if self.bMute == 0:
            strName = ('%s: \'%s\'.............') % (self.strRxCSgroup, self.strModuleName) 
            rxcs.console.module_progress(strName)
            rxcs.console.module_progress_done(self.tStart)



