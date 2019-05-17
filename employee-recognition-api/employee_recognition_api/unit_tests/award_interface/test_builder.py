import unittest
from ...award_interface.builder import Builder

class TestBuilder(unittest.TestCase):
    """Tests Builder class
    """

    @classmethod
    def setUp(cls):
        """Set up unit test class

        Arguments: class
        """
        cls.test_block = {
            'AuthorizeFirstName': 'Natasha',
            'AuthorizeLastName': 'Kvavle',
            'ReceiveFirstName': 'Patrick',
            'ReceiveLastName': 'DeLeon',
            'SignaturePath': 'test.jpg', 
            'Month': 'May', 
            'Day': '5',
            'Year': '2019'
        }   

    def test_generate_award_tex(self):
        """Tests generate_award_tex()
        """
        types = ['month', 'week']

        for type_string in types:
            builder_tool = Builder(type_string)
            mod_template = builder_tool.generate_award_tex(self.test_block)
            self.assertIn('Natasha', mod_template, msg='modified template does not contain Natasha: {}'.format(mod_template))
            self.assertIn('Kvavle', mod_template, msg='modified template does not contain Kvavle: {}'.format(mod_template))
            self.assertIn('Patrick', mod_template, msg='modified template does not contain Patrick: {}'.format(mod_template))
            self.assertIn('DeLeon', mod_template, msg='modified template does not contain DeLeon: {}'.format(mod_template))
            self.assertIn('test.jpg', mod_template, msg='modified template does not contain test.jpg: {}'.format(mod_template))
            self.assertIn('May', mod_template, msg='modified template does not contain May'.format(mod_template))
            self.assertIn('5', mod_template, msg='modified template does not contain 5'.format(mod_template))
            self.assertIn('2019', mod_template, msg='modified template does not contain 2019'.format(mod_template))
            self.assertIn(type_string, mod_template, msg='modified template does not contain {}'.format(mod_template, type_string))

if __name__ == '__main__': 
    unittest.main()