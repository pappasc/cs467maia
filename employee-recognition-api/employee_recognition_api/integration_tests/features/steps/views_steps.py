from behave import given, when, then, step
import requests
import json
import logging
import datetime

url = 'https://cs467maia-backend.appspot.com'
logging.basicConfig(filename='IntegrationTest-Views-{}.log'.format(datetime.datetime.now()), level=logging.INFO)

@when('I make a GET {endpoint} request')
def make_get_request(self, endpoint):
    """Makes a GET request  

    Arguments: 
        self
        endpoint: string. endpoint to make a request against.
    """
    self.r = requests.get('{}/{}'.format(url, endpoint))

@when('I make a POST {endpoint} request with body {body}')
def make_post_request(self, endpoint, body):
    """Makes a POST request, saves id created

    Arguments: 
        self
        endpoint: string. endpoint to make a request against.
        body: JSON obj. body of request to make
    """
    logging.info('POST {}/{}'.format(url, endpoint))
    logging.info('Body: {}'.format(body))
    if 'users' in endpoint: 
        key = 'user_id'
    elif 'admins' in endpoint: 
        key = 'admin_id'
    elif 'awards' in endpoint: 
        key = 'award_id'

    self.r = requests.post('{}/{}'.format(url, endpoint), data=body, headers={'Content-Type': 'application/json'})

    # Save the id_created if successful POST    
    if self.r.status_code == 200: 
        self.id_created = self.r.json()[key]    
    else: 
        self.id_created = None 
    logging.info('ID Created: {}'.format(self.id_created))

@when('I make another POST {endpoint} request with body {body}')
def make_post_request_2(self, endpoint, body):
    """Makes another POST request, saves id created

    Arguments: 
        self
        endpoint: string. endpoint to make a request against.
        body: JSON obj. body of request to make
    """
    logging.debug('POST {}/{}'.format(url, endpoint))
    logging.info('Body: {}'.format(body))
    if 'users' in endpoint: 
        key = 'user_id'
    elif 'admins' in endpoint: 
        key = 'admin_id'
    elif 'awards' in endpoint: 
        key = 'award_id'
        
    self.r = requests.post('{}/{}'.format(url, endpoint), data=body, headers={'Content-Type': 'application/json'})
    
    # Save second ID created if successful
    if self.r.status_code == 200: 
        self.id_2_created = self.r.json()[key]  
    else: 
        self.id_2_created = None 
    logging.info('ID Created: {}'.format(self.id_2_created))


@when('I make a PUT {endpoint} request with body {body}')
def make_put_request(self, endpoint, body): 
    """Makes a PUT request if id created is not None

    Arguments: 
        self
        endpoint: string. endpoint to make a request against.
        body: JSON obj. body of request to make
    """
    logging.info('PUT {}/{}/{}'.format(url, endpoint, self.id_created))
    logging.info('Body: {}'.format(body))
    if self.id_created is not None: 
        self.r = requests.put('{}/{}/{}'.format(url, endpoint, self.id_created), data=body, headers={'Content-Type': 'application/json'})

@when('I make a login-only PUT {endpoint} request with body {body}')
def make_put_login_request(self, endpoint, body): 
    """Makes a PUT login request if id created is not None

    Arguments: 
        self
        endpoint: string. endpoint to make a request against.
        body: JSON obj. body of request to make
    """
    logging.info('PUT {}/{}/{}/login'.format(url, endpoint, self.id_created).strip())
    logging.info('Body: {}'.format(body))
    if self.id_created is not None: 
        self.r = requests.put('{}/{}/{}/login'.format(url, endpoint, self.id_created).strip(), data=body, headers={'Content-Type': 'application/json'})

@when('I make a DELETE {endpoint} request')
def make_delete_request(self, endpoint):
    """Makes a DELETE request.

    Arguments: 
        self
        endpoint: string. endpoint to make a request against.
    """
    logging.info('URL: {}/{}'.format(url, endpoint))
    self.r = requests.delete('{}/{}'.format(url, endpoint))

@then('I get a status code of {status_code}')
def get_status_code(self, status_code): 
    """Checks status code of response.

    Arguments: 
        self
        status_code: int. Expected status code.
    """
    logging.info('STATUS: {}'.format(self.r.status_code))
    assert int(self.r.status_code) == int(status_code), 'status_code: {}'.format(self.r.status_code)

@then('the result has keys {keys}')
def compare_keys(self, keys): 
    """Checks keys of result.

    Arguments: 
        self
        keys: comma-delimited string. Exepcted keys in response body.
    """
    keys = keys.split(',')
    assert keys == self.r.json().keys(), 'keys: {}'.format(self.r.json().keys())

@then('the result field is {field}')
def compare_fields(self, field): 
    """Check error fields of result

    Arguments: 
        self
        field: string. Expected error field in response body.
    """
    assert field == self.r.json()['errors'][0]['field'], 'field: {}'.format(self.r.json()['errors'][0]['field'])
    
@then('the result message is {message}')
def compare_msg(self, message):
    """Checks error message of result.

    Arguments: 
        self
        message: string. Exepcted error message in response body.
    """
    assert message == self.r.json()['errors'][0]['message'], 'message: {}'.format(self.r.json()['errors'][0]['message'])

@then('the result has {number} errors')
def compare_number(self, number): 
    """Checks numbers of errors in result.

    Arguments: 
        self
        number: int. Number of errors expected in errors list
    """
    assert int(number) == len(self.r.json()['errors']), 'number of errors: {}'.format(len(self.r.json()['errors']))

@then('I clean up my POST to {endpoint}')
def clean_up(self, endpoint):
    """Deletes POSTed entry, cleaning up test data.

    Arguments: 
        self
        endpoint: string. Endpoint to make request against.
    """
    if endpoint == 'users': 
        key = 'user_id'
    elif endpoint == 'admins': 
        key = 'admin_id'
    elif endpoint == 'awards': 
        key = 'award_id'
    result = requests.delete('{}/{}/{}'.format(url, endpoint, self.id_created))
    assert result.json()[key] is None, 'result: {}'.format(result.json()[key]) 
