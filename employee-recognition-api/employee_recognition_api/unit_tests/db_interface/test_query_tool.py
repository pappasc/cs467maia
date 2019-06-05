import datetime
import json
import logging
import os 
from ...db_interface.query_tool import QueryTool
import unittest
import os 

class TestQueryTool(unittest.TestCase): 
    """Test QueryTool class
    """
    @classmethod
    def setUpClass(cls): 
        """Sets up class for unit tests, creating query variable & 
        test data for later use

        Arguments: cls 
        """
        # Make connection to cloud sql proxy 
        logging.basicConfig(filename='TestQueryTool-{}.log'.format(datetime.datetime.now()), level=logging.DEBUG)
        connection_data = { 
            'environment': 'dev',
            'username': 'api_user', 
            'password': 'tj348$', 
            'database': 'maia',
            'connection_name': '127.0.0.1' 
        }
        logging.debug('Connecting to database')
        cls.query = QueryTool(connection_data)

        # Define test data 
        logging.debug('Defining test data')
        cls.static_test_data = {'users': [], 'admins': [], 'awards': []}
        cls.static_test_data['users'].append({
            'user_id': 1,  
            'first_name': 'Natasha', 
            'last_name': 'Kvavle', 
            'email_address': 'kvavlen@oregonstate.edu', 
            'created_timestamp': '2019-04-15 08:52:00', 
            'signature_path': '1_kvavlen_sig.jpg',
            'password': 'encryptme'
        })
        cls.static_test_data['users'].append({
            'first_name': 'Patrick', 
            'last_name': 'DeLeon', 
            'user_id': 2, 
            'signature_path': '2_deleonp_sig.jpg', 
            'created_timestamp': '2019-04-15 08:52:00',  
            'email_address': 'deleonp@oregonstate.edu',
            'password': 'encryptme'
        })
        cls.static_test_data['admins'].append({
            'admin_id': 1,
            'first_name': 'Conner',
            'last_name': 'Pappas',  
            'created_timestamp': '2019-04-15 08:52:00', 
            'password': 'encryptme', 
            'email_address': 'pappasc@oregonstate.edu',
            'password': 'encryptme'
        })
        cls.static_test_data['awards'].append({
            'award_id': 1,
            'authorizing_user_id': 1,
            'receiving_user_id': 2, 
            'type': 'week', 
            'distributed': True, 
            'awarded_datetime': '2019-04-27 10:00:00'
        })

        # Test data used for insertions, updates, deletions
        cls.dyn_test_data = {'users': [], 'admins': [], 'awards': []}
        cls.dyn_test_data['users'].append({
            'first_name': 'Jill',
            'last_name': 'Jones', 
            'signature_path': 'jonesj_sig.jpg', 
            'created_timestamp': '2019-04-27 10:00:00', 
            'password': 'encryptme', 
            'email_address': 'jonsj@oregonstate.edu'
        })
        cls.dyn_test_data['users'].append({
            'first_name': 'Jill',
            'last_name': 'Jones', 
            'signature_path': 'jonesj_sig2.jpg', 
            'created_timestamp': '2019-04-27 10:00:00', 
            'password': 'encryptme2', 
            'email_address': 'jonesj@oregonstate.edu'
        })
        cls.dyn_test_data['admins'].append({
            'first_name': 'Bat',
            'last_name': 'Man', 
            'signature_path': 'BatMan.jpg', 
            'created_timestamp': '2019-04-27 10:00:00', 
            'password': 'encryptme', 
            'email_address': 'nanananananananananananananananabatman@oregonstate.edu'
        })
        cls.dyn_test_data['admins'].append({
            'first_name': 'Bat',
            'last_name': 'WoMan', 
            'signature_path': 'BatWoMan.jpg', 
            'created_timestamp': '2019-04-27 10:00:00', 
            'password': 'encryptme', 
            'email_address': 'nanananananananananananananananabatwoman@oregonstate.edu'
        })
        cls.dyn_test_data['awards'].append({
            'authorizing_user_id': 2,
            'receiving_user_id': 1,
            'type': 'month', 
            'distributed': False,
            'awarded_datetime': '2018-04-30 00:00:00'
        })

    @classmethod
    def tearDownClass(cls): 
        """Tears down class for unit tests, deconnecting from database

        Arguments: cls
        """
        logging.debug('Disconnecting from database')
        cls.query.disconnect()

    # Helper functions
    def test_get(self): 
        """Tests get() function

        Arguments: self
        """
        logging.debug('Test: get()')
        entities = ['user', 'admin', 'award']
        for entity in entities: 
            key = '{}_id'.format(entity)
            logging.debug('Table: {}s table'.format(entity))
            result = self.query.get('{}s'.format(entity))
            logging.debug('Function Result: {}'.format(result))

            # TEst: Result equal to test data
            logging.debug('Checking: Result contains static test data') 
            for entry in self.static_test_data['{}s'.format(entity)]:
                if entity == 'user' or entity == 'admin': 
                    self.assertEquals(self.static_test_data['{}s'.format(entity)][0][key], result['{}_ids'.format(entity)][0][key], msg='{}: result does not equal test data: {}'.format(entity, result['{}_ids'.format(entity)][0][key]))
                    self.assertEquals(self.static_test_data['{}s'.format(entity)][0]['first_name'], result['{}_ids'.format(entity)][0]['first_name'], msg='{}: result does not equal test data: {}'.format(entity, result['{}_ids'.format(entity)][0]['first_name']))
                    self.assertEquals(self.static_test_data['{}s'.format(entity)][0]['last_name'], result['{}_ids'.format(entity)][0]['last_name'], msg='{} result does not equal test data: {}'.format(entity, result['{}_ids'.format(entity)][0]['last_name']))
                    self.assertEquals(self.static_test_data['{}s'.format(entity)][0]['email_address'], result['{}_ids'.format(entity)][0]['email_address'], msg='{} result does not equal test data: {}'.format(entity, result['{}_ids'.format(entity)][0]['email_address']))
                    self.assertEquals(self.static_test_data['{}s'.format(entity)][0]['created_timestamp'], result['{}_ids'.format(entity)][0]['created_timestamp'], msg='{} result does not equal test data: {}'.format(entity, result['{}_ids'.format(entity)][0]['created_timestamp']))
            
                if entity == 'user': 
                    self.assertEquals(self.static_test_data['{}s'.format(entity)][0]['signature_path'], result['{}_ids'.format(entity)][0]['signature_path'], msg='{} result does not equal test data: {}'.format(entity, result['{}_ids'.format(entity)][0]['signature_path']))

                if entity == 'award': 
                    self.assertIn(self.static_test_data['{}s'.format(entity)][0], result['award_ids'], msg='Result is not equal to test data: {}'.format(result['award_ids']))
        
            # Test: Result does not contain test data that has not yet been inserted
            logging.debug('Checking: Result does not contain dynamic test data')
            self.assertNotIn(self.dyn_test_data['{}s'.format(entity)][0], result['{}_ids'.format(entity)], msg='Result contains test data we did not expect: {}'.format(result['{}_ids'.format(entity)]))
        
    def test_get_by_id(self):
        """Tests get_by_id() function

        Arguments: self 
        """
        logging.debug('Test: get_by_id()')
        entities = ['user', 'admin', 'award']

        for entity in entities:
            key = '{}_id'.format(entity)

            logging.debug('Table: {}s table'.format(entity))
            result = self.query.get_by_id('{}s'.format(entity), {'{}_id'.format(entity): 1})
            logging.debug('Function Result: {}'.format(result))

            # Test: Result equal to test data 
            logging.debug('Checking: Result equals static test data')
            if entity == 'user' or entity == 'admin': 
                self.assertEquals(self.static_test_data['{}s'.format(entity)][0][key], result[key], msg='{}: result is not equal to test data: {}'.format(entity, result[key]))
                self.assertEquals(self.static_test_data['{}s'.format(entity)][0]['first_name'], result['first_name'], msg='{}: result is not equal to test data: {}'.format(entity, result['first_name']))
                self.assertEquals(self.static_test_data['{}s'.format(entity)][0]['last_name'], result['last_name'], msg='{} result is not equal to test data: {}'.format(entity, result['last_name']))
                self.assertEquals(self.static_test_data['{}s'.format(entity)][0]['email_address'], result['email_address'], msg='{} result is not equal to test data: {}'.format(entity, result['email_address']))
                self.assertEquals(self.static_test_data['{}s'.format(entity)][0]['created_timestamp'], result['created_timestamp'], msg='{} result is not equal to test data: {}'.format(entity, result['created_timestamp']))
        
            if entity == 'user': 
                self.assertEquals(self.static_test_data['{}s'.format(entity)][0]['signature_path'], result['signature_path'], msg='{} result is not equal to test data: {}'.format(entity, result['signature_path']))

            if entity == 'award': 
                self.assertEquals(self.static_test_data['{}s'.format(entity)][0], result, msg='Result is not equal to test data: {}'.format(result))
    
    def test_get_awards_by_filter(self): 
        """Tests get_awards_by_filter() function 

        Arguments: self
        """
        logging.debug('Test: get_awards_by_filter()')
        filters = ['authorizing_user_id', 'receiving_user_id', 'type', 'awarded_datetime', 'distributed']
        filters_test_data = {
            'authorizing_user_id': 1, 
            'receiving_user_id': 2, 
            'type': 'week',
            'awarded_datetime': '2018-04-01 00:00:00', 
            'distributed': True
        }

        for column in filters:
            logging.debug('Filter: {}'.format(column))
            result = self.query.get_awards_by_filter(column, filters_test_data)
            logging.debug('Function Result: {}'.format(result))

            # Test: Result includes our static test data 
            logging.debug('Checking: Result equals static test data')
            self.assertIn(self.static_test_data['awards'][0], result['award_ids'], msg='Result does not include test data: {}'.format(result))
        
    def test_get_login_by_id(self):
        """Tests get_login_by_id() function

        Arguments: self
        """
        logging.debug('Test: get_login_by_id()')
        entities = ['user', 'admin']

        for entity in entities: 
            logging.debug('Table: {}s'.format(entity))
            result = self.query.get_login_by_id('{}s'.format(entity), {'{}_id'.format(entity): 1}) 
            logging.debug('Function Result: {}'.format(result))

            # Test: Result is a password
            logging.debug('Checking: Result is a password')
            self.assertEquals(result.keys(), ['password'], msg='Result is not a password: {}'.format(result))
        
            # Test: Result is equal to test data 
            logging.debug('Checking: Result equals static test data')
            self.assertEquals(result['password'], self.static_test_data['{}s'.format(entity)][0]['password'], msg='Result is not equal to test data: {}'.format(result))

    def test_post(self):
        """Tests post() function

        Arguments: self
        """
        logging.debug('Test: post()')
        entities = ['user', 'admin']

        for entity in entities: 
            logging.debug('Table: {}s'.format(entity))
            result = self.query.post('{}s'.format(entity), self.dyn_test_data['{}s'.format(entity)][0])
            logging.debug('Function Result: {}'.format(result))

            # Test: Result is a user_id
            logging.debug('Checking: Result is a {}_id'.format(entity))
            self.assertEquals(result.keys(), ['{}_id'.format(entity)], msg='Result is not a {}_id: {}'.format(entity, result))

            # Clean up test
            self.query.delete_by_id('{}s'.format(entity), {'{}_id'.format(entity): int(result['{}_id'.format(entity)]) })

    def test_put_login_by_id(self): 
        """Tests put_login_by_id() function

        Arguments: self
        """       
        logging.debug('Test: put_login_by_id()')
        entities = ['user', 'admin']

        for entity in entities: 
            logging.debug('Table: {}s'.format(entity))
            # Set up test
            # INSERT dynamic test data and capture user_id
            result = self.query.post('{}s'.format(entity), self.dyn_test_data['{}s'.format(entity)][0])
            id = int(result['{}_id'.format(entity)])

            # Add user_id to dynamic test data for UPDATE command
            self.dyn_test_data['{}s'.format(entity)][1]['{}_id'.format(entity)] = id

            # Make UPDATE query
            result = self.query.put_login_by_id('{}s'.format(entity), self.dyn_test_data['{}s'.format(entity)][1])
            logging.debug('Function Result: {}'.format(result))

            # Test: Result is an id 
            logging.debug('Checking: Result is a {}_id'.format(entity))
            self.assertEquals(result.keys(), ['{}_id'.format(entity)], msg='Result is not a {}_id: {}'.format(entity, result))

            # Test: Result is the correct id
            logging.debug('Checking: Result is correct {}_id'.format(entity))
            self.assertEquals(int(result['{}_id'.format(entity)]), id, msg='Result is not the correct {}_id: {}'.format(entity, result))

            # Clean up
            self.query.delete_by_id('{}s'.format(entity), {'{}_id'.format(entity): int(result['{}_id'.format(entity)])})

    def test_put_by_id(self):
        """Tests put_by_id() function

        Arguments: self
        """
        logging.debug('Test: put_by_id()')
        entities = ['user', 'admin', 'award']

        for entity in entities: 
            logging.debug('Table: {}s'.format(entity))
            # Set up test
            # INSERT dynamic test data and capture user_id
            result = self.query.post('{}s'.format(entity), self.dyn_test_data['{}s'.format(entity)][0])
            id = int(result['{}_id'.format(entity)])

            # award doesn't have as many test cases
            if entity == 'award':
                tc = 0 
            else:
                tc = 1

            # Add id to dynamic test data for UPDATE command
            self.dyn_test_data['{}s'.format(entity)][tc]['{}_id'.format(entity)] = id

            # Make UPDATE query
            result = self.query.put_by_id('{}s'.format(entity), self.dyn_test_data['{}s'.format(entity)][tc])
            logging.debug('Function Result: {}'.format(result))

            # Test: Result is an id 
            logging.debug('Checking: Result is a {}_id'.format(entity))
            self.assertEquals(result.keys(), ['{}_id'.format(entity)], msg='Result is not a {}_id: {}'.format(entity, result))

            # Test: Result is the correct id
            logging.debug('Checking: Result is correct {}_id'.format(entity))
            self.assertEquals(int(result['{}_id'.format(entity)]), id, msg='Result is not the correct {}_id: {}'.format(entity, result))

            # Clean up
            self.query.delete_by_id('{}s'.format(entity), {'{}_id'.format(entity): int(result['{}_id'.format(entity)])})

    def test_delete_by_id(self): 
        """
        Tests delete_by_id() function

        Arguments: self
        """
        logging.debug('Test: delete_by_id()')
        entities = ['user', 'admin', 'award']

        for entity in entities:
            logging.debug('Table: {}s'.format(entity))
            # Set up
            # INSERT dynamic test data and capture user_id
            post_result = self.query.post('{}s'.format(entity), self.dyn_test_data['{}s'.format(entity)][0])

            # DELETE inserted test data 
            delete_result = self.query.delete_by_id('{}s'.format(entity), {'{}_id'.format(entity): int(post_result['{}_id'.format(entity)])})
            logging.debug('Function Result: {}'.format(delete_result))

            # Test: DELETE result is a user_id
            logging.debug('Checking: DELETE result is a {}_id'.format(entity))
            self.assertEquals(delete_result.keys(), ['{}_id'.format(entity)], msg='Result is not a {}_id: {}'.format(entity, delete_result))

            # Test: DELETE result is a None user_id
            logging.debug('Checking: DELETE result is a {}_id of None'.format(entity))
            self.assertEquals(delete_result['{}_id'.format(entity)], None, msg='Result is not None: {}'.format(delete_result))

            # Test: GET result is an error
            logging.debug('Checking: GET result is an error'.format(entity))
            get_result = self.query.get_by_id('{}s'.format(entity), {'{}_id'.format(entity): int(post_result['{}_id'.format(entity)])})
            self.assertEquals(get_result.keys(), ['errors'], msg='Result of verification get query shows no errors: {}'.format(get_result))
        
if __name__ == '__main__': 
    unittest.main()

# References: 
# [1] https://cloud.google.com/sql/docs/mysql/sql-proxy re: proxy
# [2] https://cloud.google.com/sql/docs/mysql/connect-external-app#proxy
# [3] https://www.google.com/search?client=firefox-b-1-d&q=setting+up+cloudsql+proxy#kpvalbx=1
