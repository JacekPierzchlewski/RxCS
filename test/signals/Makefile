#
# This is the subdirectory Makefile of the RxCS toolbox.
#
#	targets:
#
#		a.  pep8 : analyze pep8 in the current dir and its subdirs
#
#		b.  clean : clean the code in the current dir and its subdirs
#
#
# Author:
# 	Jacek Pierzchlewski, Aalborg University, Denmark
# 	email: j a p (at) es _dot_ aau _dot_ dk
#
# Version:
#
#	0.1 | 13-MAY-2014: * Initial version
#	0.2 | 20-MAy-2014: * PEP8 and cleaner do not treat softlink to rxcs as a subdirectory
#
# License:
#
#	BSD 2-Clause

# Get a list of subdirectories (all except subdirs which begin with __)
SRC_DIR := $(shell ls -d */ 2>/dev/null | sed '/__/d' | sed '/rxcs/d')

# Get a list of python files (all .py files except files which begin with __)
PYTHON_FILES := $(shell ls *.py 2>/dev/null | sed '/__/d')

# Get a list with .pyc files
PYC_FILES := $(shell ls *.pyc 2>/dev/null)

# Get the name of the current dir
CUR_DIR := $(shell pwd  | sed 's/^.*rxcs/rxcs/')


# #############################################################################
#
# P E P   8   C H E C K
#
# #############################################################################
pep8:
ifneq ($(PYTHON_FILES),)
	@echo $(CUR_DIR):
	pep8 $(PYTHON_FILES)	
endif
	for i in $(SRC_DIR); do \
		cd "$$i"; make pep8; cd ..; \
	done

# #############################################################################
#
# C L E A N   ( R E M O V E   .P Y C    F I L E S )
#
# #############################################################################
clean:
	@echo -n .
ifneq ($(PYC_FILES),)
	rm -f $(PYC_FILES)
endif
ifneq ($(BAK_FILES),)
	rm -f $(BAK_FILES)
endif
	for i in $(SRC_DIR); do \
		cd "$$i"; make clean; cd ..; \
	done
