import unittest
from builder import Builder
from interpeter import Interpreter

class test_builder(unittest.TestCase):

	@classmethod
	def setUp(cls):
		cls.test_block = {
			'authorizeFirstName': 'Natasha',
			'authorizeLastName': 'Kvavle',
			'receiveFirstName': 'Patrick',
			'receiveLastName': 'DeLeon',
			'signaturePath': 'test.jpg', 
			'month': 'May', 
			'day': '5',
			'year': '2019'
		}	

	def test_gen(self):
		builder_tool = Builder('month') 
		builder_tool.replace_template(self.test_block)
		builder_tool.create_award_tex()
		interpeter_tool = Interpreter()
		interpeter_tool.interpret('award.tex')

	def test_replace_template(self): 
		builder_tool = Builder('month')

		mod_template = builder_tool.replace_template(self.test_block)
		
		#self.assertContains('Natasha', mod_template, msg='modified template is: {}'.format(mod_template))
		#self.assertContains('Kvavle', mod_template, msg='modified template is: {}'.format(mod_template))
		#self.assertContains('Patrick', mod_template, msg='modified template is: {}'.format(mod_template))
		#self.assertContains('DeLeon', mod_template, msg='modified template is: {}'.format(mod_template))
		#self.assertContains('test.jpg', mod_template, msg='modified template is: {}'.format(mod_template))
		#self.assertContains('May', mod_template, msg='modified template is: {}'.format(mod_template))
		#self.assertContains('5', mod_template, msg='modified template is: {}'.format(mod_template))
		#self.assertContains('2019', mod_template, msg='modified template is: {}'.format(mod_template))


if __name__ == '__main__': 
    unittest.main()