from __future__ import division
import rxcs
import numpy as np
#from RxOtester import RxOtester1

class RxCS_object_tester1():
    

    def __init__(self):
        self.iMaxCols = 100
        self.iNTests = 0        
        
    def run(self):
        
        self.__defined_parameters()

        self.__types_of_parameters()
        self.__types_of_elements_of_parameters()

        self.__allowed_elements()
        
        self.__relational_restrictions_on_numbers()

        self.__relational_restrictions_on_tuples()
        self.__relational_restrictions_on_lists()
        
        self.__relational_restrictions_on_NumpyVectors()
        self.__relational_restrictions_on_NumpyMatrices()
    
    
    
    def __defined_parameters(self):

         print('TESTS ON DEFINED PARAMETERS:')        
         self.__mandatory_after_optional()
         self.__mandatory_is_not_given()
         self.__mandatory_is_given()
         self.__optional_is_not_given()
         print('')


    def __types_of_parameters(self):
         print('TESTS ON TYPES OF PARAMETERS:')
         self.__type_correct_int()
         self.__type_incorrect_int()
         self.__type_correct_tuple()
         self.__type_incorrect_tuple_lists()
         print('')


    def __types_of_elements_of_parameters(self):
         print('TESTS ON TYPES OF ELEMENTS OF PARAMETERS:')
         self.__type_of_elements_correct_floats_in_list()
         self.__type_of_elements_incorrect_floats_in_tuple()
         self.__type_of_elements_incorrect_dicts_in_tuple()
         self.__type_of_elements_incorrect_elem_in_dict()
         self.__type_of_elements_correct_long_Numpy_vector()
         self.__type_of_elements_incorrect_float_in_Numpy_vector()
         self.__type_of_elements_incorrect_dict_in_long_list()
         print('')


    def __allowed_elements(self):
         print('TESTS ON ALLOWED VALUES OF PARAMETERS:')
         self.__allowed_values_correct_string()
         self.__allowed_values_inccorrect_string()
         self.__allowed_values_correct_number()
         self.__allowed_values_inccorrect_number()
         self.__allowed_values_correct_tuple()
         self.__allowed_values_incorrect_list()
         self.__allowed_values_incorrect_vector()
         self.__allowed_values_correct_matrix()
         self.__allowed_values_incorrect_list_with_allowed_values()
         print('')


    def __relational_restrictions_on_numbers(self):
         print('TESTS ON RELATIONAL RESTRICTIONS ON NUMBERS:')
         self.__relational_restriction_correct_parameter_vs_number()
         #self.__relational_restriction_incorrect_parameter_vs_number()
         #self.__relational_restriction_correct_parameter_vs_parameter()
         #self.__relational_restriction_incorrect_parameter_vs_parameter()
         print('')


    def __relational_restrictions_on_tuples(self):
         pass         
         #print('TESTS ON RELATIONAL RESTRICTIONS ON TUPLES:')
         #self.__relational_restriction_correct_tuple_vs_number()
         #self.__relational_restriction_incorrect_tuple_vs_number()
         #self.__relational_restriction_correct_tuple_vs_parameter()
         #self.__relational_restriction_incorrect_tuple_vs_parameter()
         #self.__relational_restriction_correct_tuple_vs_list()
         #self.__relational_restriction_incorrect_tuple_vs_list()
         #print('')


    def __relational_restrictions_on_lists(self):
         pass         
         #print('TESTS ON RELATIONAL RESTRICTIONS ON LISTS:')
         #self.__relational_restriction_correct_list_vs_number()
         #self.__relational_restriction_incorrect_list_vs_number()
         #self.__relational_restriction_correct_list_vs_parameter()
         #self.__relational_restriction_incorrect_list_vs_parameter()
         #self.__relational_restriction_correct_list_vs_tuple()
         #self.__relational_restriction_incorrect_list_vs_tuple()
         #self.__relational_restriction_correct_list_vs_list()
         #self.__relational_restriction_incorrect_list_vs_list()
         #self.__relational_restriction_correct_list_vs_NumpyVector()
         #self.__relational_restriction_incorrect_list_vs_NumpyVector()
         #print('')


    def __relational_restrictions_on_NumpyVectors(self):
         pass         
         #print('TESTS ON RELATIONAL RESTRICTIONS ON NUMPY VECTORS:')
         #self.__relational_restriction_correct_NumpyVector_vs_number()
         #self.__relational_restriction_incorrect_NumpyVector_vs_number()
         #self.__relational_restriction_correct_NumpyVector_vs_parameter()
         #self.__relational_restriction_incorrect_NumpyVector_vs_parameter()
         #self.__relational_restriction_correct_NumpyVector_vs_tuple()
         #self.__relational_restriction_incorrect_NumpyVector_vs_tuple()
         #self.__relational_restriction_correct_NumpyVector_vs_list()
         #self.__relational_restriction_incorrect_NumpyVector_vs_list()
         #self.__relational_restriction_correct_NumpyVector_vs_NumpyVector()
         #self.__relational_restriction_incorrect_NumpyVector_vs_NumpyVector()
         #print('')


    def __relational_restrictions_on_NumpyMatrices(self):
         pass         
         #print('TESTS ON RELATIONAL RESTRICTIONS ON NUMPY MATRICES:')
         #self.__relational_restriction_correct_NumpyMatrix_vs_number()
         #self.__relational_restriction_incorrect_NumpyMatrix_vs_number()
         #self.__relational_restriction_correct_NumpyMatrix_vs_parameter()
         #self.__relational_restriction_incorrect_NumpyMatrix_vs_parameter()
         #self.__relational_restriction_correct_NumpyMatrix_vs_tuple()
         #self.__relational_restriction_incorrect_NumpyMatrix_vs_tuple()
         #self.__relational_restriction_correct_NumpyMatrix_vs_list()
         #self.__relational_restriction_incorrect_NumpyMatrix_vs_list()
         #self.__relational_restriction_correct_NumpyMatrix_vs_NumpyVector()
         #self.__relational_restriction_incorrect_NumpyMatrix_vs_NumpyVector()
         #print('')


    def __mandatory_after_optional(self):
        """
            Test of mandatory/optional parameter check. 
            Mandatory parameter is defined after optional.
            Wanted output: RuntimeError
        """
    
        strTestName = 'Mandatory parameter cannot be defined after optional (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        self.iNTests = self.iNTests + 1
        strTestIndex = 'Test #%d:  '  % (self.iNTests)

        try:
            RxCSObject.paramAddOpt('iOpt', 'Temporary optional parameter')    
            RxCSObject.paramAddMan('iMan', 'Temporary optional parameter')
            
        except RuntimeError:
            print(strTestIndex + strTestName + (self.iMaxCols - len(strTestName) - len(strTestIndex)) * '.' + 'Test ok!')
        except:
            print(strTestIndex + strTestName + (self.iMaxCols - len(strTestName) - len(strTestIndex)) * '.' + 'Test failed!')


    def __mandatory_is_not_given(self):
        """
            Test of mandatory/optional parameter check. 
            Mandatory parameter is not given.
            Wanted output: ParameterMissingError
        """

        strTestName = 'Mandatory parameter must be given (incorrect)'
        RxCSObject = rxcs._RxCSobject()
    
        RxCSObject.paramAddMan('mandatory_parameter', 'Mandatory parameter')

        self.__parametersCheck_error(RxCSObject, rxcs.ParameterMissingError, strTestName)


    def __mandatory_is_given(self):
        """
            Test of mandatory/optional parameter check. 
            Madatory parameter is given. Cool.
            Wanted output: correct
        """
    
        strTestName = 'Mandatory parameter is given (incorrect)'
        RxCSObject = rxcs._RxCSobject()
    
        RxCSObject.paramAddMan('mandatory_parameter', 'Mandatory parameter')
        RxCSObject.mandatory_parameter = 1

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __optional_is_not_given(self):
        """
            Test of mandatory/optional parameter check. 
            Optional parameter is not given. So what? ;-) (parameter #1).
            Wanted output: correct
        """
        
        strTestName = 'Optional parameter is not given (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddOpt('optional_parameter', 'Optional parameter')
    
        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __type_correct_int(self):
        """
            Test of parameter type check. 
            Int given, int accepted (parameter #1).
            Wanted output: correct
        """
        
        strTestName = 'Type (int) is given (correct)'
        RxCSObject = rxcs._RxCSobject()
    
        RxCSObject.paramAddOpt('parameter1', 'type \'int\' parameter')
        RxCSObject.paramType('parameter1', (int))
        RxCSObject.parameter1 = int(1)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __type_incorrect_int(self):
        """
            Test of parameter type check. 
            Float given, only int accepted (parameter #3).
            Wanted output: ParameterTypeError
        """
        
        strTestName = 'Type (int instead of float) is given (incorrect)' 
        RxCSObject = rxcs._RxCSobject()
    
        RxCSObject.paramAddOpt('parameter1', 'types \'int\' or \'float\' parameter')
        RxCSObject.paramType('parameter1', (int, float))
        RxCSObject.parameter1 = 1
        
        RxCSObject.paramAddOpt('parameter2', 'type \'int\' parameter')
        RxCSObject.paramType('parameter2', (int))
        RxCSObject.parameter2 = int(2)

        RxCSObject.paramAddOpt('parameter3', 'type \'int\' parameter')
        RxCSObject.paramType('parameter3', (int))
        RxCSObject.parameter3 = float(3)

        self.__parametersCheck_error(RxCSObject, rxcs.ParameterTypeError, strTestName)



    def __type_correct_tuple(self):
        """
            Test of parameter type check. 
            List given, only tuple or list accepted (parameter #2).
            Wanted output: Correct
        """
        
        strTestName = 'Type (tuple) is given (correct)'
        RxCSObject = rxcs._RxCSobject()
    
        RxCSObject.paramAddOpt('parameter1', 'type \'tuple\' parameter')
        RxCSObject.paramType('parameter1', (tuple))
        RxCSObject.parameter1 = (1, 4)

        RxCSObject.paramAddOpt('parameter2', 'type \'list\' parameter')
        RxCSObject.paramType('parameter2', (list))
        RxCSObject.parameter2 = [10, 40]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __type_incorrect_tuple_lists(self):
        """
            Test of parameter type check. 
            Dictionary given, only tuple or list accepted (parameter #2).
            Wanted output: ParameterTypeError
        """

        strTestName = 'Type (dict instead of tuple or list) is given (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddOpt('parameter1', 'type \'tuple\' parameter')
        RxCSObject.paramType('parameter1', (tuple))
        RxCSObject.parameter1 = (1, 4)

        RxCSObject.paramAddOpt('parameter2', 'type \'tuple or list\' parameter')
        RxCSObject.paramType('parameter2', (tuple, list))
        RxCSObject.parameter2 = {}

        self.__parametersCheck_error(RxCSObject, rxcs.ParameterTypeError, strTestName)
        

    def __type_of_elements_correct_floats_in_list(self):
        """
            Test of parameter elements type check. 
            Correct float elements given in a list (parameter #3). 
            Wanted output: Correct
        """
        strTestName = 'Float elements in a list (correct)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'type \'tuple\' parameter')
        RxCSObject.paramType('parameter1', (tuple))
        RxCSObject.parameter1 = (1, 4)

        RxCSObject.paramAddMan('parameter2', 'type \'tuple or list\' parameter')
        RxCSObject.paramType('parameter2', (tuple, list))
        RxCSObject.parameter2 = [4, 5, 9]

        RxCSObject.paramAddMan('parameter3', 'type \'list\' parameter')
        RxCSObject.paramType('parameter3', (list))
        RxCSObject.paramTypeEl('parameter3', (float))
        RxCSObject.parameter3 = [4.1, 5.3, 9.0]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __type_of_elements_incorrect_floats_in_tuple(self):
        """
            Test of parameter elements type check. 
            Incorrect elements (float) given in a tuple, only tuple elements accepted (parameter #1).
            Wanted output: ElementTypeError
        """
        strTestName = 'Float elements in a list (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'type \'tuple\' parameter')
        RxCSObject.paramType('parameter1', (tuple))
        RxCSObject.paramTypeEl('parameter1', (tuple))
        RxCSObject.parameter1 = (1.2, 4.9)

        self.__parametersCheck_error(RxCSObject, rxcs.ElementTypeError, strTestName)


    def __type_of_elements_incorrect_dicts_in_tuple(self):
        """
            Test of parameter elements type check.
            Incorrect elements (dicts) given in a tuple, only int elements accepted (parameter #2).            
            Wanted output: ElementTypeError
        """
        strTestName = 'Elements (dicts) given in a tuple (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'type \'tuple\' parameter #1')
        RxCSObject.paramType('parameter1', (tuple))

        RxCSObject.paramAddMan('parameter2', 'type \'tuple\' parameter #2')
        RxCSObject.paramType('parameter2', (tuple))
        RxCSObject.paramTypeEl('parameter2', (int))

        RxCSObject.parameter1 = (1, 10)
        dD1 = {}
        dD2 = {}
        RxCSObject.parameter2 = (dD1, dD2)

        self.__parametersCheck_error(RxCSObject, rxcs.ElementTypeError, strTestName)


    def __type_of_elements_incorrect_elem_in_dict(self):
        """
            Test of parameter elements type check.
            Incorrect call for checking elements in a dictionary (parameter #1).
            Wanted output: ValueError
        """
        strTestName = 'Elements type check assigned to a dictionary (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'type \'dictionary\' parameter')
        RxCSObject.paramType('parameter1', (dict))
        RxCSObject.paramTypeEl('parameter1', (int))

        dD1 = {}
        dD1['field1'] = 3
        dD1['field2'] = 2
        dD1['field3'] = 13
        RxCSObject.parameter1 = dD1

        self.__parametersCheck_error(RxCSObject, ValueError, strTestName)


    def __type_of_elements_correct_long_Numpy_vector(self):
        """
            Test of parameter elements type check. 
            Correct elements (float) given in a long Numpy array (parameter #1).
            Wanted output: Correct
        """
        strTestName = 'Int elements in a long Numpy vector (correct)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'long Numpy vector')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramTypeEl('parameter1', (float))

        RxCSObject.parameter1 = np.random.randn(1e6)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __type_of_elements_incorrect_float_in_Numpy_vector(self):
        """
            Test of parameter elements type check. 
            Incorrect elements (float) given in a Numpy array, only int accepted.
            Wanted output: ElementTypeError
        """
        strTestName = 'Float elements in a Numpy vector (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy vector #1')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramTypeEl('parameter1', (float))

        RxCSObject.paramAddMan('parameter2', 'Numpy vector #2')
        RxCSObject.paramType('parameter2', np.ndarray)
        RxCSObject.paramTypeEl('parameter2', (int))

        RxCSObject.parameter1 = np.random.randn(1e2)
        RxCSObject.parameter2 = np.random.randn(1e2)

        self.__parametersCheck_error(RxCSObject, rxcs.ElementTypeError, strTestName)


    def __type_of_elements_incorrect_dict_in_long_list(self):
        """
            Test of parameter elements type check. 
            Incorrect element (dict) given in a long list, only strings accepted.
            Wanted output: ElementTypeError
        """
        strTestName = 'Element in a long list (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'long list')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramTypeEl('parameter1', (str))

        lLongList = int(1e6) * ['string1', 'string2']
        lLongList[len(lLongList) - 1] = {}
        RxCSObject.parameter1 = lLongList

        self.__parametersCheck_error(RxCSObject, rxcs.ElementTypeError, strTestName)


    def __allowed_values_correct_string(self):
        """
            Test of allowed values of a parameter check. 
            Correct values of a string.
            Wanted output: Correct
        """
        strTestName = 'Values of a string (correct)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'string')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramAllowed('parameter1', ['Allowed string #1', 'Allowed string #2'])
        
        RxCSObject.parameter1 = 'Allowed string #2'

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __allowed_values_inccorrect_string(self):
        """
            Test of allowed values of a parameter check. 
            Incorrect values of a string.
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a string (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'number #1')
        RxCSObject.paramAddMan('parameter2', 'number #2')

        RxCSObject.paramAddMan('parameter3', 'string')
        RxCSObject.paramType('parameter3', str)
        RxCSObject.paramAllowed('parameter3', ['Allowed string #1', 'Allowed string #2'])

        RxCSObject.parameter1 = 11
        RxCSObject.parameter2 = 21        
        RxCSObject.parameter3 = 'Allowed string #3'

        self.__parametersCheck_error(RxCSObject, rxcs.AllowedValuesError, strTestName)


    def __allowed_values_correct_number(self):
        """
            Test of allowed values of a parameter check. 
            Correct values of a number.
            Wanted output: Correct
        """
        strTestName = 'Values of a number (correct)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'number #1')
        RxCSObject.paramAddMan('parameter2', 'number #2')
        RxCSObject.paramAllowed('parameter2', range(10))

        RxCSObject.parameter1 = 11
        RxCSObject.parameter2 = 0        
  
        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __allowed_values_inccorrect_number(self):
        """
            Test of allowed values of a parameter check. 
            Incorrect values of a number.
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a number (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'number #1')
        RxCSObject.paramAddMan('parameter2', 'number #2')
        RxCSObject.paramAllowed('parameter2', range(10))

        RxCSObject.parameter1 = 11
        RxCSObject.parameter2 = 1.4

        self.__parametersCheck_error(RxCSObject, rxcs.AllowedValuesError, strTestName)


    def __allowed_values_correct_tuple(self):
        """
            Test of allowed values of a parameter check. 
            Correct values of a tuple (parameter #1).
            Wanted output: Correct
        """
        strTestName = 'Values of a tuple (correct)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'tuple')
        RxCSObject.paramAllowed('parameter1', ('Allowed string #1', 'Allowed string #2', 3, 4, 11))
        RxCSObject.parameter1 = (11, 3, 'Allowed string #1')

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __allowed_values_incorrect_list(self):
        """
            Test of allowed values of a parameter check. 
            Incorrect values of a list (parameter #2).
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a list (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'tuple')
        RxCSObject.paramAddMan('parameter2', 'list')

        RxCSObject.paramAllowed('parameter2', ('Allowed string #1', 'Allowed string #2', 3, 4, 11))
        RxCSObject.parameter1 = (1, 3, 4)
        RxCSObject.parameter2 = [11, 3, 'Allowed string #1', 'Allowed string #11']

        self.__parametersCheck_error(RxCSObject, rxcs.AllowedValuesError, strTestName)


    def __allowed_values_incorrect_vector(self):
        """
            Test of allowed values of a parameter check. 
            Incorrect values of a Numpy 1D array (parameter #1).
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a Numpy Array 1D (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy Array 1D')
        RxCSObject.paramAllowed('parameter1', range(int(1e4)))
        
        vA = np.random.randint(1, 1e3, 1e3)
        vA[vA.size-1] = 2e4
        RxCSObject.parameter1 = vA

        self.__parametersCheck_error(RxCSObject, rxcs.AllowedValuesError, strTestName)


    def __allowed_values_correct_matrix(self):
        """
            Test of allowed values of a parameter check. 
            Correct values of a Numpy 2D array (parameter #1).
            Wanted output: Correct
        """
        strTestName = 'Values of a Numpy Array 2D (correct)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy Array 2D')
        RxCSObject.paramAllowed('parameter1', range(int(2e3)))
        RxCSObject.parameter1 = np.random.randint(1, 1e3, (1e2, 1e1))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __allowed_values_incorrect_list_with_allowed_values(self):
        """
            Test of allowed values of a parameter check. 
            Incorrect value NaN given in a list with allowed values (parameter #1).
            Wanted output: ValueError
        """
        strTestName = 'Value NaN given in a list with allowed values (incorrect)'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy Array 2D')
        RxCSObject.paramAllowed('parameter1', range(int(2e3))  + [np.NaN])
        RxCSObject.parameter1 = np.random.randint(1, 1e3, (1e2, 1e1))

        self.__parametersCheck_error(RxCSObject, ValueError, strTestName)


    def __relational_restriction_correct_parameter_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            A parameter higher than a number.
            Wanted output: Correct
        """
        strTestName = 'A parameter higher than a number'
        RxCSObject = rxcs._RxCSobject()

        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)
        RxCSObject.paramH('iParameter1', 2)
        
        RxCSObject.iParameter1 = 4

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)
        RxCSObject.parametersCheck()


    def __relational_restriction_incorrect_parameter_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            A parameter lower than a number.
            Wanted output: RelationalError
        """
        strTestName = 'A parameter lower than a number'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_parameter_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Parameter lower or equal to a parameter.
            Wanted output: Correct
        """
        strTestName = 'Parameter lower or equal to a parameter'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_parameter_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Parameter higher or equal to a parameter.
            Wanted output: RelationalError
        """
        strTestName = 'Parameter higher or equal to a parameter'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_tuple_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Tuple higher or equal to a number.
            Wanted output: Correct
        """
        strTestName = 'Tuple higher or equal to a number'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_tuple_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Tuple lower or equal to a number.
            Wanted output: RelationalError
        """
        strTestName = 'Tuple lower or equal to a number'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_tuple_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Tuple lower than a parameter.
            Wanted output: Correct
        """
        strTestName = 'Tuple lower than a parameter'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_tuple_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Tuple lower than a parameter.
            Wanted output: RelationalError
        """
        strTestName = 'Tuple lower than a parameter'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_tuple_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Tuple higher than a list.
            Wanted output: Correct
        """
        strTestName = 'Tuple higher than a list'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_tuple_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Tuple higher or equal to a list.
            Wanted output: RelationalError
        """
        strTestName = 'Tuple higher or equal to a list'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_list_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            List higher or equal to a number.
            Wanted output: Correct
        """
        strTestName = 'List higher or equal to a number'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_list_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            List lower than a number.
            Wanted output: RelationalError
        """
        strTestName = 'List lower than a number'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_list_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            List lower than a parameter.
            Wanted output: Correct
        """
        strTestName = 'List lower than a parameter'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_list_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            List lower than a parameter.
            Wanted output: RelationalError
        """
        strTestName = 'List lower than a parameter'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_list_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            List lower or equal to a tuple.
            Wanted output: Correct
        """
        strTestName = 'List lower or equal to a tuple'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_list_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            List higher or equal to a tuple.
            Wanted output: RelationalError
        """
        strTestName = 'List higher or equal to a tuple'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_list_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            List higher than a list.
            Wanted output: Correct
        """
        strTestName = 'List higher than a list'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_list_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            List lower than a list.
            Wanted output: RelationalError
        """
        strTestName = 'List lower than a list'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_list_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            List lower or equal to a Numpy vector.
            Wanted output: Correct
        """
        strTestName = 'List lower or equal to a Numpy vector'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_list_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            List lower or equal to a Numpy vector.
            Wanted output: RelationalError
        """
        strTestName = 'List lower or equal to a Numpy vector'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_NumpyVector_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy vector lower or equal to a number.
            Wanted output: Correct
        """
        strTestName = 'Numpy vector lower or equal to a number'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyVector_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy vector lower or equal to a number.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector lower or equal to a number'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_NumpyVector_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy vector higher than a parameter.
            Wanted output: Correct
        """
        strTestName = 'Numpy vector higher than a parameter'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyVector_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy vector lower than a parameter.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector lower than a parameter'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_NumpyVector_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy vector lower or equal to a tuple.
            Wanted output: Correct
        """
        strTestName = 'Numpy vector lower or equal to a tuple'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyVector_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy vector lower or equal to a tuple.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector lower or equal to a tuple'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_NumpyVector_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy vector higher or equal to a list.
            Wanted output: Correct
        """
        strTestName = 'Numpy vector higher or equal to a list'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyVector_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy vector higher than a list.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector higher than a list'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_NumpyVector_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy vector higher or equal to a Numpy vector.
            Wanted output: Correct
        """
        strTestName = 'Numpy vector higher or equal to a Numpy vector'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyVector_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy vector higher than a Numpy vector.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector higher than a Numpy vector'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_NumpyMatrix_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy matrix higher than a number.
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix higher than a number'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyMatrix_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy matrix higher than a number.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix higher than a number'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_NumpyMatrix_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy matrix lower than a parameter.
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix lower than a parameter'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyMatrix_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy matrix lower or equal to a parameter.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix lower or equal to a parameter'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_NumpyMatrix_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy matrix higher or equal to a tuple.
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix higher or equal to a tuple'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyMatrix_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy matrix higher than a tuple.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix higher than a tuple'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_NumpyMatrix_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy matrix higher or equal to a list.
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix higher or equal to a list'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyMatrix_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy matrix higher or equal to a list.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix higher or equal to a list'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __relational_restriction_correct_NumpyMatrix_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy matrix lower than a Numpy Vector.
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix lower than a Numpy Vector'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyMatrix_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            Numpy matrix lower than a Numpy Vector.
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix lower than a Numpy Vector'
        RxCSObject = rxcs._RxCSobject()

        self.__parametersCheck_error(RxCSObject, rxcs.RelationalError, strTestName)


    def __parametersCheck_error(self, RxCSObject, error, strTestName):
        """
            Main engine of tests on RxCS object.
            
            Input:
                    RxCSObject:    the object being tested
                    error          wanted error, or string 'correct'
                    strTestName:   name of the current test
                    
            Output:
                    none
            
            Author:
                    Jacek Pierzchlewski
                    
            Last modification:
                    11 June 2015
            
        """
        self.iNTests = self.iNTests + 1
        strTestIndex = 'Test #%d:  '  % (self.iNTests)
        
        # Correct output is wanted
        if isinstance(error, str):
            try:
                RxCSObject.parametersCheck()
            except:
                print(strTestIndex + strTestName + (self.iMaxCols-len(strTestName)-len(strTestIndex)) * '.' + 'Test failed!')
            else:
                print(strTestIndex + strTestName + (self.iMaxCols-len(strTestName)-len(strTestIndex)) * '.' + 'Test ok!')     
  
        # Error is wanted
        else:
            try:
                RxCSObject.parametersCheck()
            except error:
                print(strTestIndex + strTestName + (self.iMaxCols-len(strTestName)-len(strTestIndex)) * '.' + 'Test ok!')     
            except:
                print(strTestIndex + strTestName + (self.iMaxCols-len(strTestName)-len(strTestIndex)) * '.' + 'Test failed!')
            else:
                print(strTestIndex + strTestName + (self.iMaxCols-len(strTestName)-len(strTestIndex)) * '.' + 'Test failed!')
        

if __name__ == "__main__":
    tester = RxCS_object_tester1()
    tester.run()
