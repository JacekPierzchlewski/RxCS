from __future__ import division
import numpy as np

# Import the main tested object
from RxCSobject import _RxCSobject

# Import errors
from RxCSobject import ParameterMissingError
from RxCSobject import ParameterTypeError
from RxCSobject import ElementTypeError
from RxCSobject import AllowedValuesError
from RxCSobject import RelationalError
from RxCSobject import SizeError


class RxCS_object_tester1():
    

    def __init__(self):
        self.iMaxCols = 100
        self.iNTests = 0        
        
    def run(self):
        
        # Are mandatory defined parameters in place?
        self.__defined_parameters()

        # Type check
        self.__types_of_parameters()
        self.__types_of_elements_of_parameters()

        # Allowed elements:
        self.__allowed_elements()

        # Relational restrictions:        
        self.__relational_restrictions_on_numbers()

        self.__relational_restrictions_on_tuples()
        self.__relational_restrictions_on_lists()
        
        self.__relational_restrictions_on_NumpyVectors()
        self.__relational_restrictions_on_NumpyMatrices()
    
        # Size restriction
        self.__size_restrictions()    

        # Restrictions on the number of dimensions
        self.__NDim_restrictions()
        
        # Restrictions on sizes of dimensions
        self.__DimSiz_restrictions()

    
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
         self.__relational_restriction_incorrect_parameter_vs_number()
         self.__relational_restriction_correct_parameter_vs_parameter()
         self.__relational_restriction_incorrect_parameter_vs_parameter()
         print('')


    def __relational_restrictions_on_tuples(self):
         print('TESTS ON RELATIONAL RESTRICTIONS ON TUPLES:')
         self.__relational_restriction_correct_tuple_vs_number()
         self.__relational_restriction_incorrect_tuple_vs_number()
         self.__relational_restriction_correct_tuple_vs_parameter()
         self.__relational_restriction_incorrect_tuple_vs_parameter()
         self.__relational_restriction_correct_tuple_vs_list()
         self.__relational_restriction_incorrect_tuple_vs_list()
         print('')


    def __relational_restrictions_on_lists(self):
         print('TESTS ON RELATIONAL RESTRICTIONS ON LISTS:')
         self.__relational_restriction_correct_list_vs_number()
         self.__relational_restriction_incorrect_list_vs_number()
         self.__relational_restriction_correct_list_vs_parameter()
         self.__relational_restriction_incorrect_list_vs_parameter()
         self.__relational_restriction_correct_list_vs_tuple()
         self.__relational_restriction_incorrect_list_vs_tuple()
         self.__relational_restriction_correct_list_vs_list()
         self.__relational_restriction_incorrect_list_vs_list()
         self.__relational_restriction_correct_list_vs_NumpyVector()
         self.__relational_restriction_incorrect_list_vs_NumpyVector()
         print('')


    def __relational_restrictions_on_NumpyVectors(self):
         print('TESTS ON RELATIONAL RESTRICTIONS ON NUMPY VECTORS:')
         self.__relational_restriction_correct_NumpyVector_vs_number()
         self.__relational_restriction_incorrect_NumpyVector_vs_number()
         self.__relational_restriction_correct_NumpyVector_vs_parameter()
         self.__relational_restriction_incorrect_NumpyVector_vs_parameter()
         self.__relational_restriction_correct_NumpyVector_vs_tuple()
         self.__relational_restriction_incorrect_NumpyVector_vs_tuple()
         self.__relational_restriction_correct_NumpyVector_vs_list()
         self.__relational_restriction_incorrect_NumpyVector_vs_list()
         self.__relational_restriction_correct_NumpyVector_vs_NumpyVector()
         self.__relational_restriction_incorrect_NumpyVector_vs_NumpyVector()
         print('')


    def __relational_restrictions_on_NumpyMatrices(self):
         print('TESTS ON RELATIONAL RESTRICTIONS ON NUMPY MATRICES:')
         self.__relational_restriction_correct_NumpyMatrix_vs_number()
         self.__relational_restriction_incorrect_NumpyMatrix_vs_number()
         self.__relational_restriction_correct_NumpyMatrix_vs_parameter()
         self.__relational_restriction_incorrect_NumpyMatrix_vs_parameter()
         self.__relational_restriction_correct_NumpyMatrix_vs_tuple()
         self.__relational_restriction_incorrect_NumpyMatrix_vs_tuple()
         self.__relational_restriction_correct_NumpyMatrix_vs_list()
         self.__relational_restriction_incorrect_NumpyMatrix_vs_list()
         self.__relational_restriction_correct_NumpyMatrix_vs_NumpyVector()
         self.__relational_restriction_incorrect_NumpyMatrix_vs_NumpyVector()
         print('')

    def __size_restrictions(self):    
         print('TESTS ON SIZE RESTRICTIONS:')
         self.__size_restriction_correct_string_number()
         self.__size_restriction_incorrect_string_number()
         self.__size_restriction_correct_string_parameter()
         self.__size_restriction_incorrect_string_parameter()
         self.__size_restriction_correct_string_string()
         self.__size_restriction_inccorrect_string_string()
         self.__size_restriction_correct_string_tuple()
         self.__size_restriction_inccorrect_string_tuple()
         self.__size_restriction_correct_string_list()
         self.__size_restriction_inccorrect_string_list()
         
         self.__size_restriction_correct_tuple_number()
         self.__size_restriction_incorrect_tuple_number()
         self.__size_restriction_correct_tuple_parameter()
         self.__size_restriction_incorrect_tuple_parameter()

         self.__size_restriction_correct_list_number()
         self.__size_restriction_incorrect_list_number()
         self.__size_restriction_correct_list_parameter()
         self.__size_restriction_incorrect_list_parameter()
         self.__size_restriction_correct_list_list()
         self.__size_restriction_incorrect_list_list()

         self.__size_restriction_correct_vector_number()
         self.__size_restriction_incorrect_vector_number()
         self.__size_restriction_correct_vector_tuple()
         self.__size_restriction_incorrect_vector_tuple()
         self.__size_restriction_correct_vector_vector()
         self.__size_restriction_incorrect_vector_vector()
         
         self.__size_restriction_correct_matrix_number()
         self.__size_restriction_incorrect_matrix_number()
         self.__size_restriction_correct_matrix_parameter()
         self.__size_restriction_incorrect_matrix_parameter()
         self.__size_restriction_correct_matrix_string()
         self.__size_restriction_incorrect_matrix_string()
         self.__size_restriction_correct_matrix_matrix()
         self.__size_restriction_incorrect_matrix_matrix()
         print('')


    def __NDim_restrictions(self):    
         print('TESTS ON RESTRICTIONS ON THE NUMBER OF DIMENSIONS:')
         print('')

    def __DimSiz_restrictions(self):    
         print('TESTS ON DIMENSION RESTRICTIONS')
         print('')


    def __mandatory_after_optional(self):
        """
            Test of mandatory/optional parameter check. 
            Wanted output: RuntimeError
        """
    
        strTestName = 'Mandatory parameter cannot be defined after optional (incorrect)'
        RxCSObject = _RxCSobject()

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
            Wanted output: ParameterMissingError
        """

        strTestName = 'Mandatory parameter must be given (incorrect)'
        RxCSObject = _RxCSobject()
    
        RxCSObject.paramAddMan('mandatory_parameter', 'Mandatory parameter')

        self.__parametersCheck_error(RxCSObject, ParameterMissingError, strTestName)


    def __mandatory_is_given(self):
        """
            Test of mandatory/optional parameter check. 
            Wanted output: correct
        """
    
        strTestName = 'Mandatory parameter is given (incorrect)'
        RxCSObject = _RxCSobject()
    
        RxCSObject.paramAddMan('mandatory_parameter', 'Mandatory parameter')
        RxCSObject.mandatory_parameter = 1

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __optional_is_not_given(self):
        """
            Test of mandatory/optional parameter check. 
            Wanted output: correct
        """
        
        strTestName = 'Optional parameter is not given (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddOpt('optional_parameter', 'Optional parameter')
    
        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __type_correct_int(self):
        """
            Test of parameter type check. 
            Wanted output: correct
        """
        
        strTestName = 'Type (int) is given (correct)'
        RxCSObject = _RxCSobject()
    
        RxCSObject.paramAddOpt('parameter1', 'type \'int\' parameter')
        RxCSObject.paramType('parameter1', (int))
        RxCSObject.parameter1 = int(1)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __type_incorrect_int(self):
        """
            Test of parameter type check. 
            Wanted output: ParameterTypeError
        """
        
        strTestName = 'Type (int instead of float) is given (incorrect)' 
        RxCSObject = _RxCSobject()
    
        RxCSObject.paramAddOpt('parameter1', 'types \'int\' or \'float\' parameter')
        RxCSObject.paramType('parameter1', (int, float))
        RxCSObject.parameter1 = 1
        
        RxCSObject.paramAddOpt('parameter2', 'type \'int\' parameter')
        RxCSObject.paramType('parameter2', (int))
        RxCSObject.parameter2 = int(2)

        RxCSObject.paramAddOpt('parameter3', 'type \'int\' parameter')
        RxCSObject.paramType('parameter3', (int))
        RxCSObject.parameter3 = float(3)

        self.__parametersCheck_error(RxCSObject, ParameterTypeError, strTestName)



    def __type_correct_tuple(self):
        """
            Test of parameter type check. 
            Wanted output: Correct
        """
        
        strTestName = 'Type (tuple) is given (correct)'
        RxCSObject = _RxCSobject()
    
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
            Wanted output: ParameterTypeError
        """

        strTestName = 'Type (dict instead of tuple or list) is given (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddOpt('parameter1', 'type \'tuple\' parameter')
        RxCSObject.paramType('parameter1', (tuple))
        RxCSObject.parameter1 = (1, 4)

        RxCSObject.paramAddOpt('parameter2', 'type \'tuple or list\' parameter')
        RxCSObject.paramType('parameter2', (tuple, list))
        RxCSObject.parameter2 = {}

        self.__parametersCheck_error(RxCSObject, ParameterTypeError, strTestName)
        

    def __type_of_elements_correct_floats_in_list(self):
        """
            Test of parameter elements type check. 
            Wanted output: Correct
        """
        strTestName = 'Float elements in a list (correct)'
        RxCSObject = _RxCSobject()

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
            Wanted output: ElementTypeError
        """
        strTestName = 'Float elements in a list (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'type \'tuple\' parameter')
        RxCSObject.paramType('parameter1', (tuple))
        RxCSObject.paramTypeEl('parameter1', (tuple))
        RxCSObject.parameter1 = (1.2, 4.9)

        self.__parametersCheck_error(RxCSObject, ElementTypeError, strTestName)


    def __type_of_elements_incorrect_dicts_in_tuple(self):
        """
            Test of parameter elements type check.
            Wanted output: ElementTypeError
        """
        strTestName = 'Elements (dicts) given in a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'type \'tuple\' parameter #1')
        RxCSObject.paramType('parameter1', (tuple))

        RxCSObject.paramAddMan('parameter2', 'type \'tuple\' parameter #2')
        RxCSObject.paramType('parameter2', (tuple))
        RxCSObject.paramTypeEl('parameter2', (int))

        RxCSObject.parameter1 = (1, 10)
        dD1 = {}
        dD2 = {}
        RxCSObject.parameter2 = (dD1, dD2)

        self.__parametersCheck_error(RxCSObject, ElementTypeError, strTestName)


    def __type_of_elements_incorrect_elem_in_dict(self):
        """
            Test of parameter elements type check.
            Wanted output: ValueError
        """
        strTestName = 'Elements type check assigned to a dictionary (incorrect)'
        RxCSObject = _RxCSobject()

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
            Wanted output: Correct
        """
        strTestName = 'Int elements in a long Numpy vector (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'long Numpy vector')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramTypeEl('parameter1', (float))

        RxCSObject.parameter1 = np.random.randn(1e6)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __type_of_elements_incorrect_float_in_Numpy_vector(self):
        """
            Test of parameter elements type check. 
            Wanted output: ElementTypeError
        """
        strTestName = 'Float elements in a Numpy vector (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy vector #1')
        RxCSObject.paramType('parameter1', np.ndarray)
        RxCSObject.paramTypeEl('parameter1', (float))

        RxCSObject.paramAddMan('parameter2', 'Numpy vector #2')
        RxCSObject.paramType('parameter2', np.ndarray)
        RxCSObject.paramTypeEl('parameter2', (int))

        RxCSObject.parameter1 = np.random.randn(1e2)
        RxCSObject.parameter2 = np.random.randn(1e2)

        self.__parametersCheck_error(RxCSObject, ElementTypeError, strTestName)


    def __type_of_elements_incorrect_dict_in_long_list(self):
        """
            Test of parameter elements type check. 
            Wanted output: ElementTypeError
        """
        strTestName = 'Element in a long list (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'long list')
        RxCSObject.paramType('parameter1', list)
        RxCSObject.paramTypeEl('parameter1', (str))

        lLongList = int(1e6) * ['string1', 'string2']
        lLongList[len(lLongList) - 1] = {}
        RxCSObject.parameter1 = lLongList

        self.__parametersCheck_error(RxCSObject, ElementTypeError, strTestName)


    def __allowed_values_correct_string(self):
        """
            Test of allowed values of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Values of a string (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'string')
        RxCSObject.paramType('parameter1', str)
        RxCSObject.paramAllowed('parameter1', ['Allowed string #1', 'Allowed string #2'])
        
        RxCSObject.parameter1 = 'Allowed string #2'

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __allowed_values_inccorrect_string(self):
        """
            Test of allowed values of a parameter check. 
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a string (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'number #1')
        RxCSObject.paramAddMan('parameter2', 'number #2')

        RxCSObject.paramAddMan('parameter3', 'string')
        RxCSObject.paramType('parameter3', str)
        RxCSObject.paramAllowed('parameter3', ['Allowed string #1', 'Allowed string #2'])

        RxCSObject.parameter1 = 11
        RxCSObject.parameter2 = 21        
        RxCSObject.parameter3 = 'Allowed string #3'

        self.__parametersCheck_error(RxCSObject, AllowedValuesError, strTestName)


    def __allowed_values_correct_number(self):
        """
            Test of allowed values of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Values of a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'number #1')
        RxCSObject.paramAddMan('parameter2', 'number #2')
        RxCSObject.paramAllowed('parameter2', range(10))

        RxCSObject.parameter1 = 11
        RxCSObject.parameter2 = 0        
  
        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __allowed_values_inccorrect_number(self):
        """
            Test of allowed values of a parameter check. 
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'number #1')
        RxCSObject.paramAddMan('parameter2', 'number #2')
        RxCSObject.paramAllowed('parameter2', range(10))

        RxCSObject.parameter1 = 11
        RxCSObject.parameter2 = 1.4

        self.__parametersCheck_error(RxCSObject, AllowedValuesError, strTestName)


    def __allowed_values_correct_tuple(self):
        """
            Test of allowed values of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Values of a tuple (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'tuple')
        RxCSObject.paramAllowed('parameter1', ('Allowed string #1', 'Allowed string #2', 3, 4, 11))
        RxCSObject.parameter1 = (11, 3, 'Allowed string #1')

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __allowed_values_incorrect_list(self):
        """
            Test of allowed values of a parameter check. 
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a list (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'tuple')
        RxCSObject.paramAddMan('parameter2', 'list')

        RxCSObject.paramAllowed('parameter2', ('Allowed string #1', 'Allowed string #2', 3, 4, 11))
        RxCSObject.parameter1 = (1, 3, 4)
        RxCSObject.parameter2 = [11, 3, 'Allowed string #1', 'Allowed string #11']

        self.__parametersCheck_error(RxCSObject, AllowedValuesError, strTestName)


    def __allowed_values_incorrect_vector(self):
        """
            Test of allowed values of a parameter check. 
            Wanted output: AllowedValuesError
        """
        strTestName = 'Values of a Numpy Array 1D (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy Array 1D')
        RxCSObject.paramAllowed('parameter1', range(int(1e4)))
        
        vA = np.random.randint(1, 1e3, 1e3)
        vA[vA.size-1] = 2e4
        RxCSObject.parameter1 = vA

        self.__parametersCheck_error(RxCSObject, AllowedValuesError, strTestName)


    def __allowed_values_correct_matrix(self):
        """
            Test of allowed values of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Values of a Numpy Array 2D (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy Array 2D')
        RxCSObject.paramAllowed('parameter1', range(int(2e3)))
        RxCSObject.parameter1 = np.random.randint(1, 1e3, (1e2, 1e1))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __allowed_values_incorrect_list_with_allowed_values(self):
        """
            Test of allowed values of a parameter check. 
            Wanted output: ValueError
        """
        strTestName = 'Value NaN given in a list with allowed values (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('parameter1', 'Numpy Array 2D')
        RxCSObject.paramAllowed('parameter1', range(int(2e3))  + [np.NaN])
        RxCSObject.parameter1 = np.random.randint(1, 1e3, (1e2, 1e1))

        self.__parametersCheck_error(RxCSObject, ValueError, strTestName)


    def __relational_restriction_correct_parameter_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'A parameter higher than a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)
        RxCSObject.paramH('iParameter1', 2)

        RxCSObject.iParameter1 = 4

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_parameter_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'A parameter lower than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('iParameter1', 'Int parameter')
        RxCSObject.paramType('iParameter1', int)
        RxCSObject.paramH('iParameter1', 2, mul=0.5, add=3)  # In English, iParameter must be higher than 4 

        RxCSObject.iParameter1 = 4

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_parameter_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Parameter lower or equal to a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, the parameter 2 must be lower or equal to 3*iRefParameter-4 
        RxCSObject.paramAddMan('iParameter2', 'Int parameter')
        RxCSObject.paramType('iParameter2', int)
        RxCSObject.paramLE('iParameter2', 'iRefParameter1', mul=3, add=-4)  # In English, iParameter must be higher than 4 

        RxCSObject.iRefParameter1 = 3 
        RxCSObject.iParameter2 = 5
        
        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_parameter_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Parameter higher or equal to a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, the parameter 2 must be lower or equal to 3*iRefParameter-4 
        RxCSObject.paramAddMan('iParameter2', 'Int parameter')
        RxCSObject.paramType('iParameter2', int)
        RxCSObject.paramHE('iParameter2', 'iRefParameter1', mul=3, add=-4)  # In English, iParameter must be higher than 4 

        RxCSObject.iRefParameter1 = 3 
        RxCSObject.iParameter2 = 4

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_tuple_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Tuple higher or equal to a number (correct)'
        RxCSObject = _RxCSobject()
        
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramHE('tParameter1', 10, mul=0.2)  # In English, all the elements of the tuple
                                                        # must be higher or equal to 2

        RxCSObject.tParameter1 = (3, 8, 9, 11, 2, 5, 7, 101)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_tuple_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Tuple lower or equal to a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramLE('tParameter1', 2, mul=4, add=-3)  # In English, all the elements of the tuple
                                                             # must be lower or equal to 5
        RxCSObject.tParameter1 = (13, 8, 9, 11, 2, 5, 7, 101)

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_tuple_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Tuple lower than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a tuple
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramL('tParameter1', 'iRefParameter1', mul=2, add=1)  

        RxCSObject.iRefParameter1 = 3
        RxCSObject.tParameter1 = (1, 2, 3, 4, 5, 6, -1, -101)

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_tuple_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Tuple lower than a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)
 
        # Now, let us define a tuple
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramL('tParameter1', 'iRefParameter1', mul=2, add=1)  

        RxCSObject.iRefParameter1 = 3
        RxCSObject.tParameter1 = (1, 2, 3, 4, 5, 7, -1, -101)

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_tuple_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Tuple higher than a list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a tuple
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramH('tParameter1', 'lRefParameter1', mul=3, add=-1)  

        RxCSObject.lRefParameter1 = [0, 1, 2]
        RxCSObject.tParameter1 = (1, 12, 13)
 
        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_tuple_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Tuple higher or equal to a list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a tuple
        RxCSObject.paramAddMan('tParameter1', 'Tuple parameter')
        RxCSObject.paramType('tParameter1', tuple)
        RxCSObject.paramHE('tParameter1', 'lRefParameter1', mul=-3)  

        RxCSObject.lRefParameter1 = [0, 1, 2]
        RxCSObject.tParameter1 = (-101, 2, 3)

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_list_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'List higher or equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramHE('lParameter1', 1, mul=3)

        RxCSObject.lParameter1 = [3, 8, 9, 11, 3, 5, 7, 101]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_list_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'List lower than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramL('lParameter1', 1)

        RxCSObject.lParameter1 = [3, 8, 9, 11, 3, 5, 7, 101]

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_list_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'List lower than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramL('lParameter1', 'iRefParameter1', add=4)

        RxCSObject.iRefParameter1 = 0
        RxCSObject.lParameter1 = [3, 1, -9, 2, 2, 3, 0, -101]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_list_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'List lower than a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramL('lParameter1', 'iRefParameter1', add=4)

        RxCSObject.iRefParameter1 = 0
        RxCSObject.lParameter1 = [3, 1, -9, 12, 2, 3, 0, -101]

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_list_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'List lower or equal to a tuple (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramLE('lParameter1', 'tRefParameter1', mul=-0.2, add=4)

        RxCSObject.tRefParameter1 = (5, 10, 15)  # (-1, 2, 1)
        RxCSObject.lParameter1 = [-3, 1, 1]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_list_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'List higher or equal to a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramHE('lParameter1', 'tRefParameter1', mul=-0.2, add=4)

        RxCSObject.tRefParameter1 = (5, 10, 15)  # (-1, 2, 1)
        RxCSObject.lParameter1 = [-3, 1, 1]

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_list_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'List higher than a list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List reference parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramH('lParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [5, 10, 15, 20]
        RxCSObject.lParameter1 = [6, 11, 16, 21]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_list_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'List lower than a list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List reference parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramL('lParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [5, 10, 15, 20]
        RxCSObject.lParameter1 = [4, 11, 16, 21]

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_list_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'List lower or equal to a Numpy vector (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Numpy 1D array reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramLE('lParameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.array([5, 10, 15, 20])
        RxCSObject.lParameter1 = [4, 5, 7, 20]

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_list_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'List lower or equal to a Numpy vector (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Numpy 1D array reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a list
        RxCSObject.paramAddMan('lParameter1', 'List parameter')
        RxCSObject.paramType('lParameter1', list)
        RxCSObject.paramLE('lParameter1', 'vRefParameter1',add=1)

        RxCSObject.vRefParameter1 = np.array([5, 10, 15, 20])
        RxCSObject.lParameter1 = [4, 5, 7, 120]

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_NumpyVector_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Numpy vector lower or equal to a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramLE('vParameter1', 5)

        RxCSObject.vParameter1 = np.array([4, 2, 1, -1, -4])
        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyVector_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector lower or equal to a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramLE('vParameter1', 5, mul=1.4)

        RxCSObject.vParameter1 = np.array([4, 2, 11, -1, -4])

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_NumpyVector_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Numpy vector higher than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a vector parameter  
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramH('vParameter1', 'iRefParameter1', mul=2)

        RxCSObject.iRefParameter1 = 2
        RxCSObject.vParameter1 = np.array([5, 12, 11, 10, 14])

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyVector_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector lower than a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a vector parameter  
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramL('vParameter1', 'iRefParameter1', mul=2)

        RxCSObject.iRefParameter1 = 2
        RxCSObject.vParameter1 = np.array([5, 12, 11, 10, 14])

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_NumpyVector_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Numpy vector lower or equal to a tuple (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramLE('vParameter1', 'tRefParameter1', mul=4)

        RxCSObject.tRefParameter1 = (10, 10, 20, 10, 15)
        RxCSObject.vParameter1 = np.array([5, 12, 11, 10, 14])

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyVector_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector lower or equal to a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramLE('vParameter1', 'tRefParameter1')

        RxCSObject.tRefParameter1 = (10, 10, 20, 10, 15)
        RxCSObject.vParameter1 = np.array([15, 42, 11, 10, 14])

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_NumpyVector_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Numpy vector higher or equal to a list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramHE('vParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [10, 10, 20, 10, 15]
        RxCSObject.vParameter1 = np.array([15, 42, 20, 10, 16])

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyVector_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector higher than a list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramH('vParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [10, 10, 20, 10, 15]
        RxCSObject.vParameter1 = np.array([15, 42, 20, 10, 16])

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_NumpyVector_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Numpy vector higher or equal to a Numpy vector (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Vector reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramHE('vParameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.array([10, 10, 20, 10, 15])
        RxCSObject.vParameter1 = np.array([15, 42, 20, 10, 16])

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyVector_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Numpy vector higher than a Numpy vector (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Vector reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a vector parameter
        RxCSObject.paramAddMan('vParameter1', 'Vector parameter')
        RxCSObject.paramType('vParameter1', np.ndarray)
        RxCSObject.paramH('vParameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.array([10, 10, 20, 10, 15])
        RxCSObject.vParameter1 = np.array([15, 42, 20, 10, 16])

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_NumpyMatrix_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix higher than a number (correct)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramH('mParameter1', 0)

        RxCSObject.mParameter1 = np.random.randint(1, 10, (2,2))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyMatrix_vs_number(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix higher than a number (incorrect)'
        RxCSObject = _RxCSobject()

        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramH('mParameter1', 11)

        RxCSObject.mParameter1 = np.random.randint(1, 10, (2,2))

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_NumpyMatrix_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix lower than a parameter (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramL('mParameter1', 'iRefParameter1', mul=4)

        RxCSObject.iRefParameter1 = 1
        RxCSObject.mParameter1 = np.random.randint(1, 3, (2,2))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyMatrix_vs_parameter(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix lower or equal to a parameter (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('iRefParameter1', 'Int parameter')
        RxCSObject.paramType('iRefParameter1', int)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramLE('mParameter1', 'iRefParameter1', mul=4)

        RxCSObject.iRefParameter1 = 1
        RxCSObject.mParameter1 = np.random.randint(1, 3, (2,2))
        RxCSObject.mParameter1[1,1] = 15

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_NumpyMatrix_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix higher or equal to a tuple (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramHE('mParameter1', 'tRefParameter1', add=-2)

        RxCSObject.tRefParameter1 = (1, 1, 2, 1)
        RxCSObject.mParameter1 = np.random.randint(2, 9, (2,2))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyMatrix_vs_tuple(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix higher than a tuple (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('tRefParameter1', 'Tuple parameter')
        RxCSObject.paramType('tRefParameter1', tuple)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramH('mParameter1', 'tRefParameter1')

        RxCSObject.tRefParameter1 = (1, 1, 2, 1, 3, 33)
        RxCSObject.mParameter1 = np.random.randint(2, 9, (3,2))

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_NumpyMatrix_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix higher or equal to a list (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramHE('mParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [-1, -1, -2, -1, -3, -33]
        RxCSObject.mParameter1 = np.random.randint(1, 9, (3,2))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyMatrix_vs_list(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix higher or equal to a list (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('lRefParameter1', 'List parameter')
        RxCSObject.paramType('lRefParameter1', list)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramHE('mParameter1', 'lRefParameter1')

        RxCSObject.lRefParameter1 = [-1, -1, -2, -1, -3, 33]
        RxCSObject.mParameter1 = np.random.randint(1, 9, (3,2))

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __relational_restriction_correct_NumpyMatrix_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: Correct
        """
        strTestName = 'Numpy matrix lower than a Numpy Vector (correct)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Vector reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramL('mParameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.random.randint(8, 9, 1e2*1e2)
        RxCSObject.mParameter1 = np.random.randint(1, 6, (1e2, 1e2))

        self.__parametersCheck_error(RxCSObject, 'correct', strTestName)


    def __relational_restriction_incorrect_NumpyMatrix_vs_NumpyVector(self):
        """
            Test of relational restriction of a parameter check. 
            Wanted output: RelationalError
        """
        strTestName = 'Numpy matrix lower than a Numpy Vector (incorrect)'
        RxCSObject = _RxCSobject()

        # Firstly, let us define a reference parameter
        RxCSObject.paramAddMan('vRefParameter1', 'Vector reference parameter')
        RxCSObject.paramType('vRefParameter1', np.ndarray)

        # Now, let us define a matrix parameter
        RxCSObject.paramAddMan('mParameter1', 'Matrix parameter')
        RxCSObject.paramType('mParameter1', np.ndarray)
        RxCSObject.paramL('mParameter1', 'vRefParameter1')

        RxCSObject.vRefParameter1 = np.random.randint(1, 9, 1e3*1e2)
        RxCSObject.mParameter1 = np.random.randint(1, 9, (1e3, 1e2))

        self.__parametersCheck_error(RxCSObject, RelationalError, strTestName)


    def __size_restriction_correct_string_number(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_incorrect_string_number(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_correct_string_parameter(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_incorrect_string_parameter(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_correct_string_string(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_inccorrect_string_string(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_correct_string_tuple(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_inccorrect_string_tuple(self):
        """
            Test of parameter size restriction check. 
            ....
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_correct_string_list(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_inccorrect_string_list(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_correct_tuple_number(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_incorrect_tuple_number(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_correct_tuple_parameter(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_incorrect_tuple_parameter(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_correct_list_number(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)



    def __size_restriction_incorrect_list_number(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_correct_list_parameter(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_incorrect_list_parameter(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_correct_list_list(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)


    def __size_restriction_incorrect_list_list(self):
        """
            Test of parameter size restriction check. 
            Wanted output: 
        """

        strTestName = ''
        RxCSObject = _RxCSobject()

        self.__parametersCheck_error(RxCSObject, SizeError, strTestName)



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
