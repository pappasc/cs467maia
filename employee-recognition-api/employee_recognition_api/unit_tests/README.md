# Unit Tests

## Instructions to Run
0. Ensure environment set up according to directions in employee-recognition-api/README.md -- only original test data should be in the database when running unit tests, otherwise tests will fail. This is an artifact of not having a QA/DEV database environment to test with.
1. Set ENV environmental variable to local: ```export ENV=local```
2. Create python module so that we can import local classes: ```python -m employee_recognition_api.__init__```
3. Run Google SQL Cloud Proxy: ```./cloud_sql_proxy --instances=cs467maia-backend:us-west1:employee-recognition-database=tcp:3306```
3. Run unit tests
	- Test views: ```python -m unittest.employee_recognition_api.unit_tests.views.test_views```
	- Test db_interface QueryTool: ```python -m unittest.employee_recognition_api.unit_tests.db_interface.test_query_tool```
	- Test db_interface InputValidatorTool: ```python -m unittest.employee_recognition_api.unit_tests.db_interface.test_input_validator_tool```
	- Test award_interface Builder: 
	```python -m unittest employee_recognition_api.unit_tests.award_interface.test_builder```
	- Test award_interface Distributer: 
	```python -m unittest employee_recognition_api.unit_tests.award_interface.test_distributer```

## Note
There are several classes that do not have unit tests becase it isn't feasible to test them in a local environment -- particularly, those classes that use cloudstorage or google.appengine.api libraries. 

## References 
1. https://docs.python.org/2.7/library/unittest.html
2. https://docs.python.org/2.7/library/unittest.html#unittest.TestCase.setUp
3. https://stackoverflow.com/questions/52305191/using-self-vs-cls-to-access-variable-in-unittest/52305252
4. https://testandcode.com/ re: test image