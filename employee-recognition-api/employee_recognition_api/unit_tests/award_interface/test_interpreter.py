import datetime
import logging
import os
import unittest
from ...award_interface.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    """No tests available at this time due to complexities with dependencies.
    """

    @classmethod
    def setUp(cls):
        """Set up unit test class

        Arguments: class
        """
        logging.basicConfig(filename='TestInterpreter-{}.log'.format(datetime.datetime.now()), level=logging.DEBUG)
        cls.interpreter = Interpreter()

    def test_save_image_to_disk(self): 
        logging.debug('save_image_to_disk() cannot be tested locally due to dependency on google app engine urlfetch')

    def test_interpret(self):
        logging.debug('interpet() cannot be tested locally due to dependency on google app engine urlfetch')

    def test_write_award_to_bucket(self):
        logging.debug('write_award_to_bucket() cannot be tested locally due to dependency on google app engine storage bucket')

if __name__ == '__main__': 
    unittest.main()