import unittest
import logging
from ...award_interface.builder import Builder

class TestBuilder(unittest.TestCase):
    """Tests Builder class
    """ 

    @classmethod
    def setUp(cls): 
        logging.basicConfig(filename='TestBuilder-{}.log'.format(datetime.datetime.now()), level=logging.DEBUG)
        cls.connection_data = { 
            'environment': 'dev',
            'username': 'api_user', 
            'password': 'tj348$', 
            'database': 'maia',
            'connection_name': '127.0.0.1' 
        }

    def test_query_database_for_data(self): 
        """Tests query_database_for_data() 
        """
        types = ['month', 'week']

        for type_string in types: 
            builder_tool = Builder(self.connection_data, type_string)
            request = { 
                'authorizing_user_id': 1,
                'receiving_user_id': 2,
                'award_id': 1,
            }
            result = builder_tool.query_database_for_data(request)
            logging.info(result)
            self.assertEquals(result['AuthorizeFirstName'], 'Natasha', msg='AuthorizeFirstName was {}'.format(result['AuthorizeFirstName']))
            self.assertEquals(result['AuthorizeLastName'], 'Kvavle', msg='AuthorizeLastName was {}'.format(result['AuthorizeLastName']))
            self.assertEquals(result['ReceiveFirstName'], 'Patrick', msg='ReceiveFirstName was {}'.format(result['ReceiveFirstName']))
            self.assertEquals(result['ReceiveLastName'], 'DeLeon', msg='ReceiveLastName was {}'.format(result['ReceiveLastName']))
            self.assertEquals(result['Month'], 'April', msg='Month was {}'.format(result['Month']))
            self.assertEquals(result['Year'], 2019, msg='Year was {}'.format(result['Year']))
            self.assertEquals(result['Day'], 27, msg='Day was {}'.format(result['Day']))

    def test_query_bucket_for_image(self): 
        logging.info('query_bucket_for_image() cannot be tested locally due to dependency on google appengine storage bucket.')

    def test_generate_award_tex(self):
        """Tests generate_award_tex()
        """
        types = ['Month', 'Week']
        
        self.test_block = {
            'AuthorizeFirstName': 'Natasha',
            'AuthorizeLastName': 'Kvavle',
            'ReceiveFirstName': 'Patrick',
            'ReceiveLastName': 'DeLeon',
            'SignaturePath': 'test.jpg', 
            'Month': 'April', 
            'Day': '27',
            'Year': '2019'
        }  

        for type_string in types:
            builder_tool = Builder(self.connection_data, type_string)
            mod_template = builder_tool.generate_award_tex(self.test_block)
            self.assertIn('Natasha', mod_template, msg='modified template does not contain Natasha: {}'.format(mod_template))
            self.assertIn('Kvavle', mod_template, msg='modified template does not contain Kvavle: {}'.format(mod_template))
            self.assertIn('Patrick', mod_template, msg='modified template does not contain Patrick: {}'.format(mod_template))
            self.assertIn('DeLeon', mod_template, msg='modified template does not contain DeLeon: {}'.format(mod_template))
            self.assertIn('test.jpg', mod_template, msg='modified template does not contain test.jpg: {}'.format(mod_template))
            self.assertIn('April', mod_template, msg='modified template does not contain May'.format(mod_template))
            self.assertIn('27', mod_template, msg='modified template does not contain 5'.format(mod_template))
            self.assertIn('2019', mod_template, msg='modified template does not contain 2019'.format(mod_template))
            self.assertIn(type_string, mod_template, msg='modified template does not contain {}'.format(mod_template, type_string))

if __name__ == '__main__': 
    unittest.main()