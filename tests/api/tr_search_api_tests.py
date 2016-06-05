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
from pwts.model import Priority, Size, Status, TrackRec


tc = app.test_client()
class TRSearchApiTest(unittest.TestCase):
        
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
    def test_search_title(self):
            
        # add a fake TR to test
        tr1 = self.add_mock_tr()
        tr1.title = "Test Title FAKESTRING 12345"
            
        # Create a TR
        r = tc.get('/api/tr/search?search_string=fakestring',
        )
        
        
        response = json.loads(r.data)
        trackrecs = response['trackrecs']
        # verify tr1 came back
        self.assertEqual(len(trackrecs), 1)
        self.assertEqual(trackrecs[0]['key'], tr1.key)
        
        
    def test_search_description(self):
            
        # add a fake TR to test
        tr1 = self.add_mock_tr()
        tr1.description = "Test Desc FAKESTRING 12345"
            
        # Create a TR
        r = tc.get('/api/tr/search?search_string=fakestring',
        )
        
        
        response = json.loads(r.data)
        trackrecs = response['trackrecs']
        # verify tr1 came back
        self.assertEqual(len(trackrecs), 1)
        self.assertEqual(trackrecs[0]['key'], tr1.key)
        
        
    def test_search_priority(self):
            
        # add 3 fake TRs to test
        # with 3 fake priority values
        priority1 = self.add_mock_vocab("test_priority1", Priority)
        priority2 = self.add_mock_vocab("test_priority2", Priority)
        priority3 = self.add_mock_vocab("test_priority3", Priority)
        tr1 = self.add_mock_tr()
        tr1.priority = priority1
        
        tr2 = self.add_mock_tr()
        tr2.priority = priority2
        
        tr3 = self.add_mock_tr()
        tr3.priority = priority3
            
        # search TRs by priority
        r = tc.get('/api/tr/search?priority=test_priority1&priority=TEST_priority2',
        )
        
        response = json.loads(r.data)
        trackrecs = response['trackrecs']
        # verify only t1 and tr2 come back
        self.assertEqual(len(trackrecs), 2)
        self.assertEqual(trackrecs[0]['key'], tr1.key)
        self.assertEqual(trackrecs[1]['key'], tr2.key)
        
        
    def test_search_size(self):
            
        # add 3 fake TRs to test
        # with 3 fake size values
        size1 = self.add_mock_vocab("test_size1", Size)
        size2 = self.add_mock_vocab("test_size2", Size)
        size3 = self.add_mock_vocab("test_size3", Size)
        tr1 = self.add_mock_tr()
        tr1.size = size1
        
        tr2 = self.add_mock_tr()
        tr2.size = size2
        
        tr3 = self.add_mock_tr()
        tr3.size = size3
            
        # search TRs by size
        r = tc.get('/api/tr/search?size=test_size1&size=TEST_size2',
        )
        
        response = json.loads(r.data)
        trackrecs = response['trackrecs']
        # verify only t1 and tr2 come back
        self.assertEqual(len(trackrecs), 2)
        self.assertEqual(trackrecs[0]['key'], tr1.key)
        self.assertEqual(trackrecs[1]['key'], tr2.key)
        
        
    def test_search_status(self):
            
        # add 3 fake TRs to test
        # with 3 fake status values
        status1 = self.add_mock_vocab("test_status1", Status)
        status2 = self.add_mock_vocab("test_status2", Status)
        status3 = self.add_mock_vocab("test_status3", Status)
        tr1 = self.add_mock_tr()
        tr1.status = status1
        
        tr2 = self.add_mock_tr()
        tr2.status = status2
        
        tr3 = self.add_mock_tr()
        tr3.status = status3
            
        # search TRs by status
        r = tc.get('/api/tr/search?status=test_status1&status=TEST_status2',
        )
        
        response = json.loads(r.data)
        trackrecs = response['trackrecs']
        # verify only t1 and tr2 come back
        self.assertEqual(len(trackrecs), 2)
        self.assertEqual(trackrecs[0]['key'], tr1.key)
        self.assertEqual(trackrecs[1]['key'], tr2.key)
        
        
    # Helpers
    def add_mock_tr(self):
        """
        Insert a test TR into db session
        """
        trackrec = TrackRec()
        trackrec.key = db.session.query(db.func.max(TrackRec.key).label("max_key")) \
                .one().max_key + 1
        
        db.session.add(trackrec)
        
        return trackrec

    def add_mock_vocab(self, name, cvClass):
        """
        Insert a test controlled vocab record into db session
           cvClass determines the vocab model to use
        """
        cvObj = cvClass()
        cvObj.key = db.session.query(db.func.max(cvClass.key).label("max_key")) \
                .one().max_key + 1
        cvObj.name = name
        
        db.session.add(cvObj)
        
        return cvObj
   
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TRSearchApiTest))
    return suite

if __name__ == '__main__':
    unittest.main()
