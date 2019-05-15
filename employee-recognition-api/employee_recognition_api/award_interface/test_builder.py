import unittest
from builder import Builder
from interpeter import Interpreter

class test_builder(unittest.TestCase):

	def test_init(self):
		builder_tool = Builder('month-test')
		test_block = {
			'authorizeFirstName': 'Natasha',
			'authorizeLastName': 'Kvavle',
			'receiveFirstName': 'Patrick',
			'receiveLastName': 'DeLeon',
			'signaturePath': 'test.jpg', 
			'month': 'May', 
			'day': '5',
			'year': '2019'
		}
		
		builder_tool.worker(test_block)

		interpeter_tool = Interpreter()
		interpeter_tool.interpret('award.tex')

if __name__ == '__main__': 
    unittest.main()