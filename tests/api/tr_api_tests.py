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
from pwts import app, db
from pwts.model import TrackRec


tc = app.test_client()
class TRApiTest(unittest.TestCase):
        
    def setUp(self):
            
        # Prevent Flask-SQLAlchemy from removing session after each request
        def doNothing():
            pass
        self.oldDbSessionRemove = db.session.remove
        db.session.remove = doNothing
            
            
    def tearDown(self):
            db.session.rollback()
            self.oldDbSessionRemove()

    # Test the api.tr_api views
    def test_create_tr(self):
            
        # Create a TR
        r = tc.post('/api/tr',
                data=json.dumps(dict(
                  title='Testing TR Creation'
                )),
                content_type = 'application/json'
        )
        
        
        trackrec = json.loads(r.data)
         
        self.assertEqual(trackrec['title'], "Testing TR Creation")
         
        # try to load from db session
        trackrec = TrackRec.query.filter_by(key=trackrec['key']).first()
        self.assertEqual(trackrec.title, "Testing TR Creation")
        
    def test_delete_tr(self):
            
        newKey = self.add_mock_tr()
       
        r = tc.delete('/api/tr/%d' % newKey)
        result = json.loads(r.data)
        assert result['result'] == True, "check successful delete"
        
        # try to query for deleted TR
        trackrec = TrackRec.query.filter_by(key=newKey).first()
        self.assertEqual(trackrec, None)
        
        
    def test_get_tr(self):
            
        newKey = self.add_mock_tr()
       
        r = tc.get('/api/tr/%d' % newKey)
        trackrec = json.loads(r.data)
        self.assertEqual(trackrec['title'], 'Testing TR Creation')
        
        
    def test_update_tr(self):
            
        newKey = self.add_mock_tr()
       
        r = tc.put('/api/tr/%d' % newKey,
                data=json.dumps(dict(
                    title="Testing Updated Title"    
                )),
                content_type = "application/json"
        )
        trackrec = json.loads(r.data)
        self.assertEqual(trackrec['title'], 'Testing Updated Title')
        
        # test updated from db session
        trackrec = TrackRec.query.filter_by(key=newKey).first()
        self.assertEqual(trackrec.title, 'Testing Updated Title')
        
        
    # Helpers
    def add_mock_tr(self):
        """
        Insert a test TR into db session
        """
        trackrec = TrackRec()
        trackrec.key = db.session.query(db.func.max(TrackRec.key).label("max_key")) \
                .one().max_key + 1
        trackrec.title = "Testing TR Creation"
        
        db.session.add(trackrec)
        
        return trackrec.key
   
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TRApiTest))
    return suite

if __name__ == '__main__':
    unittest.main()
