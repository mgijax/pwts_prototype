"""
Run all API test suites
"""
import sys,os.path
# adjust the path for running the tests locally, so that it can find app (i.e. 2 dirs up)
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# disable SQLAlchemy Warnings
import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('ignore', category=SAWarning)

import unittest

# import all sub test suites
import tr_api_tests
import tr_search_api_tests

# add the test suites
def master_suite():
	suites = []
	suites.append(tr_api_tests.suite())
	suites.append(tr_search_api_tests.suite())
        
	master_suite = unittest.TestSuite(suites)
	return master_suite

if __name__ == '__main__':
	test_suite = master_suite()
	runner = unittest.TextTestRunner()
	
	ret = not runner.run(test_suite).wasSuccessful()
	sys.exit(ret)
