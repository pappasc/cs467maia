# test_distributer.py
import datetime
import logging
import unittest
from ...award_interface.distributer import Distributer
from ...db_interface.query_tool import QueryTool

class TestDistributer(unittest.TestCase):
    """Test Distributer class
    """
    
    @classmethod
    def setUp(cls): 
        """Set up test
        """
        logging.basicConfig(filename='TestDistributer-{}.log'.format(datetime.datetime.now()), level=logging.DEBUG)
        cls.connection_data = { 
            'environment': 'dev',
            'username': 'api_user', 
            'password': 'tj348$', 
            'database': 'maia',
            'connection_name': '127.0.0.1' 
        }

    def test_update_distributed_in_database(self): 
        """Tests updated_distributed_in_database()
        """
        logging.debug('Test: update_distributed_in_database')

        # Post a test award (without any validation)
        query = QueryTool(self.connection_data)
        post_data = {
            'authorizing_user_id': 2, 
            'receiving_user_id': 1, 
            'distributed': False, 
            'awarded_datetime': '2018-09-14 0:00:00', 
            'type': 'week'
        }
        post_result = query.post('awards', post_data)
        award_id = post_result['award_id']

        distributer = Distributer(award_id)
        distributer.update_distributed_in_database(self.connection_data)

        # Check distributed was updated
        get_result = query.get_by_id('awards', {'award_id': award_id})

        # Delete test award
        query.delete_by_id('awards',  {'award_id': award_id})

        # Verify distributed bool flipped
        self.assertEquals(bool(get_result['distributed']), True, msg='Distributed value was {}'.format(get_result['distributed']))

