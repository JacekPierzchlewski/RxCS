



        self.paramAddMan('vSigIn', 'Input signal')
        self.paramType('vSigIn', np.ndarray)                #
        self.paramTypeEl('vSigIn', (float, int))            #
        

        self.paramL('vSigIn',  np.inf)                      # Only for int, float, ndarray, list, tuple. Elements must be int, float
        self.paramH('vSigIn', -np.inf)                      # Only for int, float, ndarray, list, tuple. Elements must be int, float 


        # -----------------------------------------------------------------------------------------------------------------------------------------

        # Size:        
        self.paramSizEq('vSigIn', 'fs', mul=0.5, add=1)     # Size equal. Only for ndarray, list, tuple, string.  Ref.  must be:               1) int - size equal to the number.   
                                                            #                                                                                  2) string - equal to a parameter named by the string.
                                                            #                                                                                     If a parameter is int then 1). 
                                                            #                                                                                     If a parameter is: 
                                                            #                                                                                     (list, tuple, ndarray, string) then equal to the 
                                                            #                                                                                     size of the parameter 

        self.paramSizH('vSigIn', 'fs',  mul=0.5, add=1)     # Size higher than. Only for ndarray, list, tuple, string. Ref. must be:           1) int, float - szie higher than the number.
                                                            #                                                                                  2) string - higher than a parameter named by the string.
                                                            #                                                                                     If a parameter is (int, float) then 1). 
                                                            #                                                                                     If a parameter is: 
                                                            #                                                                                     (list, tuple, ndarray, string) then higher than the 
                                                            #                                                                                     size of the parameter 

        self.paramSizHE('vSigIn', 'fs',  mul=0.5, add=1)    # Size higher or equal to. Only for ndarray, list, tuple, string. Ref. must be:    1) int, float - szie higher or equal to the number,   
                                                            #                                                                                  2) string - higher or equal to a parameter named by the string.
                                                            #                                                                                     If a parameter is (int, float) then 1). 
                                                            #                                                                                     If a parameter is: 
                                                            #                                                                                     (list, tuple, ndarray, string) then higher or equal to the 
                                                            #                                                                                     size of the parameter 


       self.paramSizL('vSigIn', 'fs',  mul=0.5, add=1)      # Size lower than. Only for ndarray, list, tuple, string. Ref. must be:            1) int, float - szie lower than the number.
                                                            #                                                                                  2) string - lower than a parameter named by the string.
                                                            #                                                                                     If a parameter is (int, float) then 1). 
                                                            #                                                                                     If a parameter is: 
                                                            #                                                                                     (list, tuple, ndarray, string) then lower than the 
                                                            #                                                                                     size of the parameter 

        self.paramSizLE('vSigIn', 'fs',  mul=0.5, add=1)    # Size lower or equal to. Only for ndarray, list, tuple, string. Ref. must be:     1) int, float - size lower or equal to the number.
                                                            #                                                                                  2) string - lower or equal to a parameter named by the string.
                                                            #                                                                                     If a parameter is (int, float) then 1). 
                                                            #                                                                                     If a parameter is: 
                                                            #                                                                                     (list, tuple, ndarray, string) then lower or equal to the 
                                                            #                                                                                     size of the parameter
 
        # -----------------------------------------------------------------------------------------------------------------------------------------
 
        # The number of dimensions:        
        self.paramNDimEq('vSigIn', 'fs',  mul=0.5, add=1)    # The number of dimensions (equal). Only for ndarray. Ref. must be either         1) int - the number of dimensions equal to the number.
                                                            #                                                                                 2) string - equal to something hidden in the string.
                                                            #                                                                                     If a parameter is (int) then 1). 
                                                            #                                                                                     If a parameter is (ndarray) then the number of dimension  
                                                            #                                                                                     equal to the number of dimensions in the parameter. 
                                                            #                                                                                     


        self.paramNDimH('vSigIn', 'fs',  mul=0.5, add=1)    # The number of dimensions (higher). Only for ndarray. Ref. must be either:        1) int, float - the number of dimensions higher than the number.   
                                                            #                                                                                  2) string - the number of dimensions higher than something 
                                                            #                                                                                     hidden in the string.
                                                            #                                                                                     If a parameter is (int, float) then 1).
                                                            #                                                                                     If a parameter is (ndarray) then the number of dimensions  
                                                            #                                                                                     higher than the number of dimensions in the parameter.

        self.paramNDimHE('vSigIn', 'fs',  mul=0.5, add=1)   # The number of dimensions (higher or equal to). Only for ndarray. Ref. must be either:     1) int, float - the number of dimensions higher than the number.   
                                                            #                                                                                           2) string - the number of dimensions higher than something 
                                                            #                                                                                                        hidden in the string.
                                                            #                                                                                            If a parameter is (int, float) then 1).
                                                            #                                                                                     If a parameter is (ndarray) then the number of dimensions  
                                                            #                                                                                     higher than the number of dimensions in the parameter.

        self.paramNDimL('vSigIn', 'fs',  mul=0.5, add=1)    # The number of dimensions (lower or equal to). Only for ndarray. Ref. must be either:         1) int, float - the number of dimensions lower than the number.   
                                                            #                                                                                  2) string - the number of dimensions lower than something 
                                                            #                                                                                     hidden in the string.
                                                            #                                                                                     If a parameter is (int, float) then 1).
                                                            #                                                                                     If a parameter is (ndarray) then the number of dimensions  
                                                            #                                                                                     lower than the number of dimensions in the parameter.

        self.paramNDimLE('vSigIn', 'fs',  mul=0.5, add=1)   # The number of dimensions (higher or equal to). Only for ndarray. Ref. must be either:     1) int, float - the number of dimensions higher than the number.   
                                                            #                                                                                           2) string - the number of dimensions higher than something 
                                                            #                                                                                                        hidden in the string.
                                                            #                                                                                            If a parameter is (int, float) then 1).
                                                            #                                                                                     If a parameter is (ndarray) then the number of dimensions  
                                                            #                                                                                     higher than the number of dimensions in the parameter.


        # -----------------------------------------------------------------------------------------------------------------------------------------

        # Shape:
        self.paramShapeEq('vSigIn', 'fs', pedantic=1)       # Shape equal. Only for numpy, second element must be either:                         1) (int, tuple of int) - equal to the numbers,   
                                                            #                                                                                     2) string - equal to the shape of something hidden in
                                                            #                                                                                                 the string
        
        # -----------------------------------------------------------------------------------------------------------------------------------------


        # Size of dimension #x:
        self.paramDimEq('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1)   # Dimension #iDim equal to. Only for numpy, second element must be either:                         1) (int, tuple of int) - equal to the numbers,   
                                                            #                                                                                     2) string - equal to the shape of something hidden in
             paramDimH
             paramDimL
             paramDimLE
             paramDimHE
                                                                #                                                                                                 the string


        # -----------------------------------------------------------------------------------------------------------------------------------------

        # The number of columns
        self.paramColsEq('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0)      # Dimension #iDim equal to. Only for numpy, second element must be either:                         1) (int, tuple of int) - equal to the numbe2) string - equal to the shape of something hidden in
         #                                                                                                 the string
        self.paramColsH('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramColsHE('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramColsL('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramColsLE('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 

        # The number of rows
        self.paramRowsEq('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramRowsH('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramRowsHE('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramRowsL('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramRowsLE('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 

        # The number of pages
        self.paramRowsEq('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramRowsH('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramRowsHE('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramRowsL('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 
        self.paramRowsLE('vSigIn', 'fs', iDim, ,  mul=1.0, add=0.0, pedantic=1) 











