import unittest
from ...award_interface.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    """Tests Interpreter class
    """

    @classmethod
    def setUp(cls):
        """Set up unit test class

        Arguments: class
        """
        cls.interpreter = Interpreter()

    def test_interpret(self):
        # Read test .tex file into memory
        file = open('test.tex', 'r')
        tex = file.read()

        # Read test .jpg file into memory 
        image = open('test.jpg', 'r')
        jpg = image.read()

        pdf = self.interpreter.interpret(tex, jpg)
        self.assertNotEquals(None, pdf, msg='Result was None')


    def test_write_award_to_bucket(self):
        # Read test .tex file into memory
        file = open('test.tex', 'r')
        tex = file.read()

        # Read test .jpg file into memory 
        image = open('test.jpg', 'r')
        jpg = image.read()

        pdf = self.interpreter.interpret(tex, jpg)
        result = self.interpeter.test_write_award_to_bucket(pdf)

        self.assertEquals(0, result, msg='Result was {}'.format(result))
        

if __name__ == '__main__': 
    unittest.main()