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
        cls.interpreter = Interpreter()

    def test_interpret(self):
        logging.info('test_interpet() cannot be tested due to dependency on google app engine urlfetch')


    def test_write_award_to_bucket(self):
        logging.info('write_award_to_bucket() cannot be tested due to dependency on google app engine storage bucket')

if __name__ == '__main__': 
    unittest.main()