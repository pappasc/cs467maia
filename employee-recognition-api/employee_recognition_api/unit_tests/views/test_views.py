import datetime
import json
import logging
import unittest
from flask import Flask
from ...views.main import app

class TestViews(unittest.TestCase): 
    """Test Users, Admins, Awards API 
        This an intentionally light-weight/happy-path test suite, since much of the
        functionality I would normally test here is handled by integration tests. This is more 
        of a quick check so that I know I haven't broken basic functionality and can 
        push to the App Engine.

        I've included all endpoints in this class since there is so much shared code.
    """
    @classmethod
    def setUpClass(cls): 
        """Sets up the TestUsers class, 
           initializing log file & creating a test client

        Arguments: cls 
        """
        logging.basicConfig(filename='TestViews-{}.log'.format(datetime.datetime.now()), level=logging.DEBUG)
        # Set up the test client built into Flask 
        cls.app = app.test_client()
        cls.app.testing = True     

    def check_status_code(self, result):         
        """Checks status code is 200 

        Arguments: 
            self
            result: result object from Flask application 
        """
        logging.debug('Checking: status code')
        self.assertEqual(result.status_code, 200, 'Status code was {}'.format(result.status_code))

    def check_keys(self, result, expected_keys): 
        """Checks result data has the correct keys 

        Arguments: 
            self
            result: result object from Flask application 
            expected_keys: list. list of expected keys in result.
        """          
        logging.debug('Checking: keys')
        data = json.loads(result.data)
        self.assertEqual(expected_keys, data.keys(), 'Keys in JSON-parsed response: {}'.format(data.keys()))

    def test_users(self): 
        """Test endpoints defined in users()

        Arguments: self
        """
        # Test: GET /users
        logging.debug('TEST: GET /users')
        get_result = self.app.get('/users') 
        self.check_status_code(get_result)
        self.check_keys(get_result, ['user_ids'])
  
        # Test: GET /users/1
        logging.debug('TEST: GET /users/1')
        get_one_result = self.app.get('/users/1') 
        self.check_status_code(get_one_result)
        self.check_keys(get_one_result, ['first_name', 'last_name', 'user_id', 'signature_path', 'created_timestamp', 'email_address'])

        # Test: POST /users
        logging.debug('TEST: POST /users')
        post_result = self.app.post('/users',
        json={
            'first_name': 'Amelia',
            'last_name': 'Bedelia', 
            'created_timestamp': '2019-05-11 0:00:00',
            'password': 'ameliabe',
            'signature_path': 'test.jpg',
            'email_address': 'ameliabedelia@fakesite.com' 
        })
        logging.debug(post_result)
        self.check_status_code(post_result)
        self.check_keys(post_result, ['user_id'])
        
        # Get user ID posted to database for later use
        user_id = json.loads(post_result.data)['user_id']
        logging.debug('User ID posted: {}'.format(user_id))
        
        # Test: PUT /users/{user_id}
        logging.debug('TEST: PUT /users/{}'.format(user_id))
        put_result = self.app.put('/users/{}'.format(user_id), 
            json={
                'first_name': 'Amelia',
                'last_name': 'Bedelia', 
                'signature_path': 'test.jpg',
                'email_address': 'ameliabedelia@fakesite.com'
            })
        self.check_status_code(put_result)
        self.check_keys(put_result, ['user_id'])

        logging.debug('TEST: PUT/users/{}/login'.format(user_id))
        put_login_result = self.app.put('/users/{}'.format(user_id), 
            json={
                'password': 'ameliabede',
            })
        self.check_status_code(put_login_result)
        self.check_keys(put_login_result, ['user_id'])

        # Test: DELETE /users/{user_id}
        logging.debug('TEST: DELETE /users/{}'.format(user_id))
        delete_result = self.app.delete('/users/{}'.format(user_id))
        self.check_status_code(delete_result)
        self.check_keys(delete_result, ['user_id'])

    def test_users_login(self): 
        """Test endpoints defined in users_login()

        Arguments: self
        """
        # Test: GET /users/1/login
        logging.debug('TEST: GET /users/1/login')
        get_login_result = self.app.get('/users/1/login')
        self.check_status_code(get_login_result)
        self.check_keys(get_login_result, ['password'])

    def test_admins(self): 
        """Test endpoints defined in admins()

        Arguments: self
        """      
        # Test: GET /admins
        logging.debug('TEST: GET /admins')
        get_result = self.app.get('/admins') 
        self.check_status_code(get_result)
        self.check_keys(get_result, ['admin_ids'])
  
        # Test: GET /admins/1
        logging.debug('TEST: GET /admins/1')
        get_one_result = self.app.get('/admins/1') 
        self.check_status_code(get_one_result)
        self.check_keys(get_one_result, ['created_timestamp', 'first_name', 'last_name', 'email_address', 'admin_id'])

        # Test: POST /admins
        logging.debug('TEST: POST /admins')
        post_result = self.app.post('/admins',
            json={
                'first_name': 'Amelia',
                'last_name': 'Bedelia', 
                'created_timestamp': '2019-05-11 0:00:00',
                'password': 'ameliabe',
                'email_address': 'ameliabedelia@fakesite.com' 
        })
        logging.debug(post_result)
        self.check_status_code(post_result)
        self.check_keys(post_result, ['admin_id'])
        
        # Get user ID posted to database for later use
        admin_id = json.loads(post_result.data)['admin_id']
        logging.debug('Admin ID posted: {}'.format(admin_id))
        
        # Test: PUT /admins/{admin_id}
        logging.debug('TEST: PUT /admins/{}'.format(admin_id))
        put_result = self.app.put('/admins/{}'.format(admin_id), 
            json={
                'first_name': 'Amelia',
                'last_name': 'Bedelia', 
                'email_address': 'ameliabedelia@fakesite.com'
            })
        self.check_status_code(put_result)
        self.check_keys(put_result, ['admin_id'])

        # Test: PUT /admins/{admin_id}/login
        logging.debug('TEST: PUT /admins/{}/login'.format(admin_id))
        put_login_result = self.app.put('/admins/{}/login'.format(admin_id), 
            json={
                'password': 'ameliabe',
            })
        self.check_status_code(put_login_result)
        self.check_keys(put_login_result, ['admin_id'])

        # Test: DELETE /admins/{admin_id}
        logging.debug('TEST: DELETE /admins/{}'.format(admin_id))
        delete_result = self.app.delete('/admins/{}'.format(admin_id))
        self.check_status_code(delete_result)
        self.check_keys(delete_result, ['admin_id'])


    def test_awards(self): 
        """Test endpoints defined in awards()

        Arguments: self
        """
        # Test: GET /awards/{award_id}
        logging.debug('TEST: GET /awards/1')
        get_result = self.app.get('/awards/1') 
        self.check_status_code(get_result)
        self.check_keys(get_result, ['authorizing_user_id', 'distributed', 'awarded_datetime', 'receiving_user_id', 'award_id', 'type'])
  
        # Test: POST /awards
        logging.debug('TEST: POST /awards')
        post_result = self.app.post('/awards',
            json={
                'authorizing_user_id': 1,
                'receiving_user_id': 2, 
                'awarded_datetime': '2051-05-11 00:00:00',
                'type': 'month'
        })
        logging.debug(post_result)
        self.check_status_code(post_result)
        self.check_keys(post_result, ['award_id'])
        
        # Get user ID posted to database for later use
        award_id = json.loads(post_result.data)['award_id']
        logging.debug('Award ID posted: {}'.format(award_id))
       
        # Test: DELETE /awards/{award_id}
        logging.debug('TEST: DELETE /awards/{}'.format(award_id))
        delete_result = self.app.delete('/awards/{}'.format(award_id))
        self.check_status_code(delete_result)
        self.check_keys(delete_result, ['award_id'])


    def test_awards_authorize(self): 
        """Test endpoints defined in awards_authorize()

        Arguments: self
        """       
        # Test: GET /awards/authorize/{user_id}
        logging.debug('TEST: GET /awards/authorize/1')
        get_result = self.app.get('/awards/authorize/1') 
        self.check_status_code(get_result)
        self.check_keys(get_result, ['award_ids'])
  
    def test_awards_receive(self): 
        """Test endpoints defined in awards_receive()

        Arguments: self
        """     
        # Test: GET /awards/receive/{user_id}
        logging.debug('TEST: GET /awards/receive/1')
        get_result = self.app.get('/awards/receive/1') 
        self.check_status_code(get_result)
        self.check_keys(get_result, ['award_ids'])
  
    def test_awards_type(self): 
        """Test endpoints defined in awards_type()

        Arguments: self
        """    
        # Test: GET /awards/type/{type}
        logging.debug('TEST: GET /awards/type/week')
        get_result = self.app.get('/awards/type/week') 
        self.check_status_code(get_result)
        self.check_keys(get_result, ['award_ids'])

        logging.debug('TEST: GET /awards/type/month')
        get_result = self.app.get('/awards/type/month') 
        self.check_status_code(get_result)
        self.check_keys(get_result, ['award_ids'])

    def test_awards_datetime(self): 
        """Test endpoints defined in awards_datetime()

        Arguments: self
        """    
        # Test: GET /awards/datetime/{date}
        logging.debug('TEST: GET /awards/datetime/2018-05-20')
        get_result = self.app.get('/awards/datetime/2018-05-20') 
        self.check_status_code(get_result)
        self.check_keys(get_result, ['award_ids'])

    def test_awards_distributed(self): 
        """Test endpoints defined in awards_distributed()

        Arguments: self
        """    
        # Test: GET /awards/datetime/{date}
        logging.debug('TEST: GET /awards/distributed/false')
        get_result = self.app.get('/awards/distributed/false') 
        self.check_status_code(get_result)
        self.check_keys(get_result, ['award_ids'])

if __name__ == '__main__': 
    unittest.main()
    
# References
# [1] https://damyanon.net/post/flask-series-testing/        re: example to model unit tests for flask applications from
# [2] http://flask.pocoo.org/docs/1.0/testing/               re: how to make different requests with flask testing framework