import datetime
import json
import logging
import os 
from query_tool import QueryTool
import unittest
import os 

# Instructions to Run: 
# wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
# chmod +x cloud_sql_proxy
# ./cloud_sql_proxy --instances=maia-backend:us-west1:employee-recognition-db=tcp:3306 
# python test_query_tool.py 

class TestQueryTool(unittest.TestCase): 

	@classmethod
	def setUpClass(cls): 
		"""Sets up class for unit tests, creating query variable & 
		test data for later use

		Arguments: cls 
		"""
		# Make connection to cloud sql proxy 
		logging.basicConfig(filename='unittest-{}.log'.format(datetime.datetime.now()), level=logging.DEBUG)
		connection_data = { 
			'username': 'api_user', 
			'password': 'tj348$', 
			'database': 'maia',
			'connection_name': '127.0.0.1' 
		}
		logging.debug('Connecting to database')
		cls.query = QueryTool(connection_data)

		# Define test data 
		logging.debug('Defining test data')
		cls.static_test_data = {'users': [], 'admins': [], 'awards': []}
		cls.static_test_data['users'].append({
			'user_id': 1,  
			'first_name': 'Natasha', 
			'last_name': 'Kvavle', 
			'email_address': 'kvavlen@oregonstate.edu', 
			'password': 'encryptme', 
			'created_timestamp': '2019-04-15 08:52:00', 
			'signature_path': 'kvavlen_sig.jpg'
		})
		cls.static_test_data['users'].append({
			'first_name': 'Patrick', 
			'last_name': 'DeLeon', 
			'user_id': 2, 
			'signature_path': 'deleonp_sig.jpg', 
			'created_timestamp': '2019-04-15 08:52:00', 
			'password': 'encryptme', 
			'email_address': 'deleonp@oregonstate.edu'
		})
		cls.static_test_data['admins'].append({
			'admin_id': 1,
			'first_name': 'Conner',
			'last_name': 'Pappas',  
			'created_timestamp': '2019-04-15 08:52:00', 
			'password': 'encryptme', 
			'email_address': 'pappasc@oregonstate.edu'
		})
		cls.static_test_data['awards'].append({
			'award_id': 1,
			'authorizing_user_id': 1,
			'receiving_user_id': 2, 
			'type': 'week', 
			'distributed': False, 
			'awarded_datetime': '2019-04-27 10:00:00'
		})

		# Test data used for insertions, updates, deletions
		cls.dyn_test_data = {'users': [], 'admins': [], 'awards': []}
		cls.dyn_test_data['users'].append({
			'first_name': 'Jill',
			'last_name': 'Jones', 
			'signature_path': 'jonesj_sig.jpg', 
			'created_timestamp': '2019-04-27 10:00:00', 
			'password': 'encryptme', 
			'email_address': 'jonsj@oregonstate.edu'
		})
		cls.dyn_test_data['users'].append({
			'first_name': 'Jill',
			'last_name': 'Jones', 
			'signature_path': 'jonesj_sig2.jpg', 
			'created_timestamp': '2019-04-27 10:00:00', 
			'password': 'encryptme2', 
			'email_address': 'jonesj@oregonstate.edu'
		})
		cls.dyn_test_data['admins'].append({
			'first_name': 'Bat',
			'last_name': 'Man', 
			'signature_path': 'BatMan.jpg', 
			'created_timestamp': '2019-04-27 10:00:00', 
			'password': 'encryptme', 
			'email_address': 'nanananananananananananananananabatman@oregonstate.edu'
		})
		cls.dyn_test_data['admins'].append({
			'first_name': 'Bat',
			'last_name': 'WoMan', 
			'signature_path': 'BatWoMan.jpg', 
			'created_timestamp': '2019-04-27 10:00:00', 
			'password': 'encryptme', 
			'email_address': 'nanananananananananananananananabatwoman@oregonstate.edu'
		})
		cls.dyn_test_data['awards'].append({
			'authorizing_user_id': 2,
			'receiving_user_id': 1,
			'type': 'month', 
			'distributed': False,
			'awarded_datetime': '2018-04-30 00:00:00'
		})

	@classmethod
	def tearDownClass(cls): 
		"""Tears down class for unit tests, deconnecting from database

		Arguments: cls
		"""
		logging.debug('Disconnecting from database')
		cls.query.disconnect()

	# Helper functions
	def helper_test_json(self, result): 
		"""Tests if result is valid JSON format

		Arguments: 
			self 
			result - JSON object
		"""
		# Try to load JSON from result variable
		# A ValueError indicates invalid JSON format
		logging.debug('Checking: Valid JSON')
		try: 
			json.loads(result)
			json_bool = True
		except ValueError:
			json_bool = False 

		self.assertTrue(json_bool, msg='Result was not in valid json: {}'.format(result))

	def test_get(self): 
		"""Tests get() function

		Arguments: self
		"""
		logging.debug('Test: get()')
		entities = ['user', 'admin', 'award']
		for entity in entities: 
			logging.debug('Table: {}s table'.format(entity))
			result = self.query.get('{}s'.format(entity))

			# Test: Result is valid JSON	
			self.helper_test_json(result)

			# Test: Result contains test data
			parsed_result = json.loads(result)
			logging.debug('Function Result: {}'.format(parsed_result))

			logging.debug('Checking: Result contains static test data')	
			for entry in self.static_test_data['{}s'.format(entity)]:
				self.assertIn(entry, parsed_result['{}_ids'.format(entity)], msg='Result does not contain test data: {}'.format(parsed_result['{}_ids'.format(entity)]))
			
			# Test: Result does not contain test data that has not yet been inserted
			logging.debug('Checking: Result does not contain dynamic test data')
			self.assertNotIn(self.dyn_test_data['{}s'.format(entity)][0], parsed_result['{}_ids'.format(entity)], msg='Result contains test data we did not expect: {}'.format(parsed_result['{}_ids'.format(entity)]))
		
	def test_get_by_id(self):
		"""Tests get_by_id() function

		Arguments: self
		"""
		logging.debug('Test: get_by_id()')
		entities = ['user', 'admin', 'award']

		for entity in entities: 
			logging.debug('Table: {}s table'.format(entity))

			result = self.query.get_by_id('{}s'.format(entity), {'{}_id'.format(entity): 1})

			# Test: Result is valid JSON	
			self.helper_test_json(result)

			# Test: Result equal to test data 
			parsed_result = json.loads(result)
			logging.debug('Function Result: {}'.format(parsed_result))

			logging.debug('Checking: Result equals static test data')
			self.assertEquals(self.static_test_data['{}s'.format(entity)][0], parsed_result, msg='Result is not equal to test data: {}'.format(parsed_result))

	def test_get_awards_by_filter(self): 
		"""Tests get_awards_by_filter() function 

		Arguments: self
		"""
		logging.debug('Test: get_awards_by_filter()')
		filters = ['authorizing_user_id', 'receiving_user_id', 'type', 'awarded_datetime', 'distributed']
		filters_test_data = {
			'authorizing_user_id': 1, 
			'receiving_user_id': 2, 
			'type': 'week',
			'awarded_datetime': '2018-04-01 00:00:00', 
			'distributed': False
		}

		for column in filters:
			logging.debug('Filter: {}'.format(column))
			result = self.query.get_awards_by_filter(column, filters_test_data)

			# Test: Result is valid JSON
			self.helper_test_json(result)
			parsed_result = json.loads(result)

			logging.debug('Function Result: {}'.format(parsed_result))

			# Test: Result includes our static test data 
			logging.debug('Checking: Result equals static test data')
			self.assertIn(self.static_test_data['awards'][0], parsed_result['award_ids'], msg='Result does not include test data: {}'.format(parsed_result))
		
	def test_get_login_by_id(self):
		"""Tests get_login_by_id() function

		Arguments: self
		"""
		logging.debug('Test: get_awards_by_id()')
		entities = ['user', 'admin']

		for entity in entities: 
			logging.debug('Table: {}s'.format(entity))
			result = self.query.get_login_by_id('{}s'.format(entity), {'{}_id'.format(entity): 1}) 

			# Test: Result is valid JSON	
			self.helper_test_json(result)
			parsed_result = json.loads(result)
			logging.debug('Function Result: {}'.format(parsed_result))

			# Test: Result is a password
			logging.debug('Checking: Result is a password')
			self.assertEquals(parsed_result.keys(), ['password'], msg='Result is not a password: {}'.format(parsed_result))
		
			# Test: Result is equal to test data 
			logging.debug('Checking: Result equals static test data')
			self.assertEquals(parsed_result['password'], self.static_test_data['{}s'.format(entity)][0]['password'], msg='Result is not equal to test data: {}'.format(parsed_result))

	def test_post(self):
		"""Tests post() function

		Arguments: self
		"""
		logging.debug('Test: post()')
		entities = ['user', 'admin']

		for entity in entities: 
			logging.debug('Table: {}s'.format(entity))
			result = self.query.post('{}s'.format(entity), self.dyn_test_data['{}s'.format(entity)][0])

			# Test: Result is valid JSON	
			self.helper_test_json(result)	
			parsed_result = json.loads(result)
			logging.debug('Function Result: {}'.format(parsed_result))

			# Test: Result is a user_id
			logging.debug('Checking: Result is a {}_id'.format(entity))
			self.assertEquals(parsed_result.keys(), ['{}_id'.format(entity)], msg='Result is not a {}_id: {}'.format(entity, parsed_result))

			# Clean up test
			self.query.delete_by_id('{}s'.format(entity), {'{}_id'.format(entity): int(parsed_result['{}_id'.format(entity)]) })

	def test_put_by_id(self):
		"""Tests put_by_id() function

		Arguments: self
		"""
		logging.debug('Test: put_by_id()')
		entities = ['user', 'admin']

		for entity in entities: 
			logging.debug('Table: {}s'.format(entity))
			# Set up test
			# INSERT dynamic test data and capture user_id
			result = self.query.post('{}s'.format(entity), self.dyn_test_data['{}s'.format(entity)][0])
			parsed_result = json.loads(result)

			id = int(parsed_result['{}_id'.format(entity)])

			# Add user_id to dynamic test data for UPDATE command
			self.dyn_test_data['{}s'.format(entity)][1]['{}_id'.format(entity)] = id

			# Make UPDATE query
			result = self.query.put_by_id('{}s'.format(entity), self.dyn_test_data['{}s'.format(entity)][1])
			
			# Test: Result is valid JSON	
			self.helper_test_json(result)	
			parsed_result = json.loads(result)
			logging.debug('Function Result: {}'.format(parsed_result))

			# Test: Result is an id 
			logging.debug('Checking: Result is a {}_id'.format(entity))
			self.assertEquals(parsed_result.keys(), ['{}_id'.format(entity)], msg='Result is not a {}_id: {}'.format(entity, parsed_result))

			# Test: Result is the correct id
			logging.debug('Checking: Result is correct {}_id'.format(entity))
			self.assertEquals(int(parsed_result['{}_id'.format(entity)]), id, msg='Result is not the correct user_id: {}'.format(parsed_result))

			# Clean up
			self.query.delete_by_id('{}s'.format(entity), {'{}_id'.format(entity): int(parsed_result['{}_id'.format(entity)])})

	def test_delete_by_id(self): 
		"""
		Tests delete_by_id() function

		Arguments: self
		"""
		logging.debug('Test: delete_by_id()')
		entities = ['user', 'admin', 'award']

		for entity in entities:
			logging.debug('Table: {}s'.format(entity))
			# Set up
			# INSERT dynamic test data and capture user_id
			post_result = self.query.post('{}s'.format(entity), self.dyn_test_data['{}s'.format(entity)][0])
			parsed_post_result = json.loads(post_result)

			# DELETE inserted test data 
			delete_result = self.query.delete_by_id('{}s'.format(entity), {'{}_id'.format(entity): int(parsed_post_result['{}_id'.format(entity)])})
			
			# Test: Result is valid JSON	
			self.helper_test_json(delete_result)	
			parsed_delete_result = json.loads(delete_result)
			logging.debug('Function Result: {}'.format(parsed_delete_result))

			# Test: DELETE result is a user_id
			logging.debug('Checking: DELETE result is a {}_id'.format(entity))
			self.assertEquals(parsed_delete_result.keys(), ['{}_id'.format(entity)], msg='Result is not a {}_id: {}'.format(entity, parsed_delete_result))

			# Test: DELETE result is a None user_id
			logging.debug('Checking: DELET result is a {}_id of None'.format(entity))
			self.assertEquals(parsed_delete_result['{}_id'.format(entity)], None, msg='Result is not None: {}'.format(parsed_delete_result))

			# Test: GET result is an error
			logging.debug('Checking: GET result is an error'.format(entity))
			get_result = self.query.get_by_id('{}s'.format(entity), {'{}_id'.format(entity): int(parsed_post_result['{}_id'.format(entity)])})
			parsed_get_result = json.loads(get_result)
			self.assertEquals(parsed_get_result.keys(), ['errors'], msg='Result of verification get query shows no errors: {}'.format(parsed_get_result))
		
if __name__ == '__main__': 
	unittest.main()

# References: 
# [1] https://cloud.google.com/sql/docs/mysql/sql-proxy re: proxy
# [2] https://cloud.google.com/sql/docs/mysql/connect-external-app#proxy
# [3] https://www.google.com/search?client=firefox-b-1-d&q=setting+up+cloudsql+proxy#kpvalbx=1
