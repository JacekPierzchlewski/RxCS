#
# This is the main Makefile of the RxCS toolbox.
#
#	targets:
#
#		a.  pep8 : analyze the pep8-compatibility of the code 
#
#		b.  htmldoc : generate the documentation in html 
#
#		c.  clean : clean the code (remove temporary files)
#
#
# Author:
# 	Jacek Pierzchlewski, Aalborg University, Denmark 
# 	email: j a p (at) es _dot_ aau _dot_ dk
#
# Version:
#
#	0.1 | 13-MAY-2014: * Initial version
#
# License: 
#
#	BSD 2-Clause


# #############################################################################
#
# D O C U M E N T A T I O N
#
# #############################################################################
DIR_WITH_DOCUMENTATION = "doc"

htmldoc:
	make -C $(DIR_WITH_DOCUMENTATION) html

# #############################################################################
#
# P E P   8   C H E C K
#
# #############################################################################
DIR_WITH_PYTHON = "py_code"

pep8:
	@echo ================================================
	@echo
	@echo      '"'RXCS'"' system - pep8 checker
	@echo
	@echo ================================================
	@make --quiet -C rxcs pep8
	@make --quiet -C examples pep8

# #############################################################################
#
# C L E A N   ( R E M O V E   . P Y C    F I L E S )
#
# #############################################################################
clean:
	@echo -n '"'RxCS'"' system - removing .pyc files
	@make --quiet -C rxcs clean
	@make --quiet -C examples clean
	@echo done!
