import datetime
import json
import logging
import os 
from ...db_interface.input_validator_tool import InputValidatorTool
import unittest
import os 

class TestInputValidatorTool(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        """Sets up TestInputValidatorTool class

        Arguments: cls 
        """
        logging.basicConfig(filename='TestInputValidatorTool-{}.log'.format(datetime.datetime.now()), level=logging.DEBUG)
        logging.debug('setUpClass')

        # Setup test cases
        cls.happy_path = {
            'password': ['test1234', 'encryptme'],
            'name': ['Natasha', 'Sarah', 'Ian', 'Patrick', 'Conner', 'Kvavle', 'DeLeon', 'Pappas'],
            'time': ['2019-12-04 00:00:00', '2019-02-02 05:03:00'],
            'signature_path': ['test.jpg', 'nkvavle_sig.jpg', 'deleonp_sig.jpg'],
            'email_address': [ 'helloitsme@oregonstate.edu', 'kvavlen@oregonstate.edu']
        }

        cls.sad_path = {
            'password': ['a', '1', 'supercalifragilisticexpialidocious'],
            'name': [''],
            'time': ['2018-5-30:00:00', '2019-', 'May 3, 2019 0:00:00', '2019-23-03 00:25:61'],
            'signature_path': ['test.png', 'jpg.png', 'test.txt', 'test'],
            'email_address': ['']
        }

        cls.input_validator = InputValidatorTool()

    @classmethod
    def tearDownClass(cls):
        """Tears down TestInputValidatorTool class

        Arguments: cls
        """ 
        logging.debug('tearDownClass')

    def test_template_response(self):
        """Tests template_response() 

        Arguments: self
        """
        logging.debug('Test: template_response()')

        # Setup test cases
        tests = [
            'password', 
            'first_name', 
            'last_name', 
            'created_timestamp', 
            'awarded_datetime', 
            'signature_path'
        ]

        # Test: Response is correct based on field
        logging.debug('Checking: Response includes field specified')
        for field in tests: 
            response = self.input_validator.template_response(field)
            self.assertEquals(response, {'field': field, 'message': 'invalid value'}, msg='Response is not correct: {}'.format(response))

    def test_valid_password(self):
        """Tests valid_password() 

        Arguments: self
        """
        logging.debug('Test: template_response()')

        # Test: Happy Path
        logging.debug('Checking: Happy Path passwords yield None response')
        for pwd in self.happy_path['password']:
            response = self.input_validator.valid_password(pwd)
            self.assertEquals(response, None, msg='Response was not None: {}'.format(response))
        
        # Test: Sad Path
        logging.debug('Checking: Sad Path passwords yield error response')
        for pwd in self.sad_path['password']:
            response = self.input_validator.valid_password(pwd)
            self.assertEquals(response, {'field': 'password', 'message': 'invalid value'}, msg='Response was not an error: {}'.format(response))

    def test_valid_name(self): 
        """Tests valid_name() 

        Arguments: self
        """
        logging.debug('Test: valid_name()')

        # Setup test cases
        tests = ['first_name', 'last_name']

        # Test: First name, Last name
        for test in tests: 

            # Test: Happy Path
            logging.debug('Checking: Happy Path for {} yield None response'.format(test))
            for name in self.happy_path['name']:
                response = self.input_validator.valid_name(name, test)
                self.assertEquals(response, None, msg='Response was not None')

            # Test: Sad Path
            logging.debug('Checking: Sad Path for {} yield None response'.format(test))
            for name in self.sad_path['name']: 
                response = self.input_validator.valid_name(name, test)
                self.assertEquals(response, {'field': test, 'message': 'invalid value'}, msg='Response was not an error: {}'.format(response))

    def test_valid_time(self): 
        """Tests valid_time() 

        Arguments: self
        """
        logging.debug('Test: valid_time()')

        # Setup test cases
        tests = ['created_datetime', 'awarded_timestamp']

        # Test: 'created_datetime', 'awarded_timestamp'
        for test in tests: 
            
            # Test: Happy Path
            for time in self.happy_path['time']: 
                response = self.input_validator.valid_time(time, test)
                self.assertEquals(response, None, msg='Response was not None: {}'.format(response))

            # Test: Sad Path
            for time in self.sad_path['time']: 
                response = self.input_validator.valid_time(time, test)  
                self.assertEquals(response, {'field': test, 'message': 'invalid value'}, msg='Response was not an error: {}'.format(response))
    
    def test_valid_signature_path(self): 
        """Tests valid_signature_path() 

        Arguments: self
        """
        logging.debug('Test: valid_signature_path()')

        # Test: Happy Path
        for signature_path in self.happy_path['signature_path']: 
            response = self.input_validator.valid_signature_path(signature_path)
            self.assertEquals(response, None, msg='Response was not None: {}'.format(response))

        # Test: Sad Path
        for signature_path in self.sad_path['signature_path']: 
            response = self.input_validator.valid_signature_path(signature_path)
            self.assertEquals(response, {'field': 'signature_path', 'message': 'invalid value'}, msg='Response was not an error: {}'.format(response))
    
    def test_valid_email(self):
        """Tests valid_email()
    
        Arguments: self
        """    
        logging.debug('Test: valid_email()')

        # Test: Happy Path
        for email in self.happy_path['email_address']: 
            response = self.input_validator.valid_email(email)
            self.assertEquals(response, None, msg='Response was not None: {}'.format(response))

        # Test: Sad Path
        for email in self.sad_path['email_address']: 
            response = self.input_validator.valid_email(email)
            self.assertEquals(response, {'field': 'email_address', 'message': 'invalid value'}, msg='Response was not an error: {}'.format(response))
    
    def test_validate_login(self): 
        """Tests validate_login() 

        Arguments: self
        """        
        all_happy = { 
            'password': self.happy_path['password'][0]
        }
        response = self.input_validator.validate_login(all_happy)
        self.assertEquals(response, None, msg='Response was not None: {}'.format(response))
       
        # Test: Sad Path
        all_sad = {
            'password': self.sad_path['password'][0]
        }
        response = self.input_validator.validate_login(all_sad)
        expected = {
            'errors': [
                {'field': 'password', 'message': 'invalid value'},
            ]
        }
        self.assertEquals(response, expected, msg='This Response was not correct errors: {}'.format(response))


    def test_validate_users(self):
        """Tests validate_users() 

        Arguments: self
        """
        logging.debug('Test: validate_users()')

        # Test: POST Happy Path 
        all_happy = {
            'first_name': self.happy_path['name'][0],
            'last_name': self.happy_path['name'][1],
            'created_timestamp': self.happy_path['time'][0],
            'password': self.happy_path['password'][0],
            'signature_path': self.happy_path['signature_path'][0],
            'email_address': self.happy_path['email_address'][0]
        }
        response = self.input_validator.validate_users('POST', all_happy)
        self.assertEquals(response, None, msg='Response was not None: {}'.format(response))

        # Test: POST Half Sad Path
        half_sad = { 
            'first_name': self.happy_path['name'][0],
            'last_name': self.happy_path['name'][1],
            'created_timestamp': self.sad_path['time'][0],
            'password': self.sad_path['password'][0],
            'signature_path': self.sad_path['signature_path'][0],
            'email_address': self.happy_path['email_address'][0]
        }

        response = self.input_validator.validate_users('POST', half_sad)
        logging.info('Half sad data: {}'.format(half_sad))
        expected = {'errors': [
            {'field': 'signature_path', 'message': 'invalid value'}, 
            {'field': 'created_timestamp', 'message': 'invalid value'}, 
            {'field': 'password', 'message': 'invalid value'}
        ]}

        self.assertEquals(response, expected, msg='Response was not correct errors: {}'.format(response))

        # Test: POST Sad Path
        all_sad = {
            'first_name': self.sad_path['name'][0],
            'last_name': self.sad_path['name'][0],
            'created_timestamp': self.sad_path['time'][0],
            'password': self.sad_path['password'][0],
            'signature_path': self.sad_path['signature_path'][0], 
            'email_address': self.sad_path['email_address'][0]
        }
        response = self.input_validator.validate_users('POST', all_sad)
        logging.info('All sad data: {}'.format(all_sad))
        expected = {'errors': [
            {'field': 'first_name', 'message': 'invalid value'}, 
            {'field': 'last_name', 'message': 'invalid value'}, 
            {'field': 'email_address', 'message': 'invalid value'}, 
            {'field': 'signature_path', 'message': 'invalid value'}, 
            {'field': 'created_timestamp', 'message': 'invalid value'}, 
            {'field': 'password', 'message': 'invalid value'}
        ]}
        self.assertEquals(response, expected, msg='Response was not correct errors: {}'.format(response))
    
    def test_validate_admins(self):
        """Tests validate_admins() 

        Arguments: self
        """
        logging.debug('Test: validate_admins()')

        # Test: POST Happy Path 
        all_happy = {
            'first_name': self.happy_path['name'][0],
            'last_name': self.happy_path['name'][1],
            'created_timestamp': self.happy_path['time'][0],
            'password': self.happy_path['password'][0],
            'email_address': self.happy_path['email_address'][0]
        }
        response = self.input_validator.validate_admins('POST', all_happy)
        self.assertEquals(response, None, msg='Response was not None: {}'.format(response))

        # Test: POST Half Sad Path
        half_sad = { 
            'first_name': self.happy_path['name'][0],
            'last_name': self.happy_path['name'][1],
            'created_timestamp': self.sad_path['time'][0],
            'password': self.sad_path['password'][0],
            'email_address': self.sad_path['email_address'][0]
        }

        response = self.input_validator.validate_admins('POST', half_sad)
        expected = {
            'errors': [
                {'field': 'email_address', 'message': 'invalid value'}, 
                {'field': 'created_timestamp', 'message': 'invalid value'}, 
                {'field': 'password', 'message': 'invalid value'}
            ]}
        self.assertEquals(response, expected, msg='Response was not correct errors: {}'.format(response))

        # Test: POST Sad Path
        all_sad = {
            'first_name': self.sad_path['name'][0],
            'last_name': self.sad_path['name'][0],
            'created_timestamp': self.sad_path['time'][0],
            'password': self.sad_path['password'][0],
            'email_address': self.sad_path['email_address'][0]
        }
        response = self.input_validator.validate_admins('POST', all_sad)
        expected = {
            'errors': [
                {'field': 'first_name', 'message': 'invalid value'}, 
                {'field': 'last_name', 'message': 'invalid value'}, 
                {'field': 'email_address', 'message': 'invalid value'}, 
                {'field': 'created_timestamp', 'message': 'invalid value'}, 
                {'field': 'password', 'message': 'invalid value'}
            ]}

        self.assertEquals(response, expected, msg='Response was not correct errors: {}'.format(response))
    
if __name__ == '__main__': 
    unittest.main()