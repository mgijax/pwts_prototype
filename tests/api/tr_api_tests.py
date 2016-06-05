"""
Test the TR REST API
"""
import sys
import os
import json
# adjust the path for running the tests locally, so that it can find app (i.e. 2 dirs up)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../..'))

from tests import test_config

import unittest
from pwts import app

tc = app.test_client()
class TRApiTest(unittest.TestCase):

    # Test the api.tr_api views
    def test_create_tr(self):
            
        # Create a TR
        r = tc.post('/api/tr',
                data=json.dumps(dict(
                  tr_title='Testing TR Creation'
                )),
                content_type = 'application/json'
        )
        
        assert 'Testing TR Creation' in r.data, "check TR Title"
        
    def test_delete_tr(self):
            
         # Create a TR
        r = tc.post('/api/tr',
                data=json.dumps(dict(
                  tr_title='Testing TR Creation'
                )),
                content_type = 'application/json'
        )
        
        trackrec = json.loads(r.data)
       
        r = tc.delete('/api/tr/%d' % trackrec['key'])
        result = json.loads(r.data)
        assert result['result'] == True, "check successful delete"
        
        
    def test_get_tr(self):
            
         # Create a TR
        r = tc.post('/api/tr',
                data=json.dumps(dict(
                  tr_title='Testing TR Creation'
                )),
                content_type = 'application/json'
        )
        
        trackrec = json.loads(r.data)
       
        r = tc.get('/api/tr/%d' % trackrec['key'])
        trackrec = json.loads(r.data)
        self.assertEqual(trackrec['title'], 'Testing TR Creation')
   
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TRApiTest))
    return suite

if __name__ == '__main__':
    unittest.main()
