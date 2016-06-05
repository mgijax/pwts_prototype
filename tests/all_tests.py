"""
Run all PWTS test suites
"""
import sys,os.path
# adjust the path for running the tests locally, so that it can find app (i.e. 1 dirs up)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# disable SQLAlchemy Warnings
import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('ignore', category=SAWarning)

import unittest

# import all sub test suites
import api.all_tests as api_tests

# add the test suites
def master_suite():
	suites = []
	suites.append(api_tests.master_suite())
	
	master_suite = unittest.TestSuite(suites)
	return master_suite

if __name__ == '__main__':
	test_suite = master_suite()
	runner = unittest.TextTestRunner()
	
	ret = not runner.run(test_suite).wasSuccessful()
	sys.exit(ret)
