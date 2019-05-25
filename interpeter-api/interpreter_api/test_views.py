import datetime
import json
import logging
import unittest
from flask import Flask
from views import interpreter_api

class TestViews(unittest.TestCase): 
    """Test Interpeter API 
    
    This is based off of test_views.py in employee_recognition_api/unit_tests/views
    Much like that file, this file focus on the happy path as a quick check that these 
    functions are suitable. 
    """
    @classmethod
    def setUpClass(cls): 
        """Sets up the TestUsers class, 
           initializing log file & creating a test client

        Arguments: cls 
        """
        logging.basicConfig(filename='TestViews-{}.log'.format(datetime.datetime.now()), level=logging.DEBUG)
        # Set up the test client built into Flask 
        cls.interpreter_api = interpreter_api.test_client()
        cls.interpreter_api.testing = True     

    def test_image(self): 
        """Test endpoints defined in image()

        Arguments: self
        """
        
        # Test: GET /image
        logging.debug('TEST: GET /image')
        get_result = self.interpreter_api.get('/image/test_image.jpg')
        
        logging.debug('Checking: Status code is 400')
        self.assertEqual(get_result.status_code, 400, 'Status code was {}'.format(get_result.status_code))
        
        # Test: POST /image
        logging.debug('TEST: POST /image')
        
        # Get test image file
        file = open('kvavlen_sig.jpg', 'r')
        image = file.read()
        
        # Send to flask app
        logging.debug('Checking: Status code is 200')
        post_result = self.interpreter_api.post('/image/test_image.jpg', data=image)
        self.assertEqual(post_result.status_code, 200, 'Status code was {}'.format(post_result.status_code))

        # Check file exists
        logging.debug('Checking: Image successfully written to disk')
        get_result = self.interpreter_api.get('/image/test_image.jpg')
        self.assertEqual(get_result.status_code, 200, 'Status code was {}'.format(get_result.status_code))
        
        # Test: DELETE /image
        logging.debug('TEST: DELETE /image')
        
        # Send to flask app
        logging.debug('Checking: Status code is 200')
        delete_result = self.interpreter_api.delete('/image/test_image.jpg')
        self.assertEqual(delete_result.status_code, 200, 'Status code was {}'.format(delete_result.status_code))

        # Check file no longer exists
        logging.debug('Checking: Image successfully deleted')
        get_result = self.interpreter_api.get('/image/test_image.jpg')
        self.assertEqual(get_result.status_code, 400, 'Status code was {}'.format(get_result.status_code))
        
    def test_pdf(self): 
        logging.debug('pdf() cannot easily be tested locally as it requires a texlive distribution')

if __name__ == '__main__': 
    unittest.main()
    
# References
# [1] https://damyanon.net/post/flask-series-testing/        re: example to model unit tests for flask applications from
# [2] http://flask.pocoo.org/docs/1.0/testing/               re: how to make different requests with flask testing framework