# interp_steps.py
# step definitions for interpreter.feature, testing interpreter-api directly
from behave import given, when, then, step
import requests
import json
import logging
import datetime

# global-level variables
url = 'http://54.203.128.106:80/'
logging.basicConfig(filename='IntegrationTest-Interpreter-{}.log'.format(datetime.datetime.now()), level=logging.INFO)

@when('I make an AWS {request_type} /image/test.jpg request')
def make_image_request(self, request_type):
    """Makes a GET, POST, or DELETE request to /image/test.jpg on AWS instance

    Arguments: 
        self
        request_type: POST, GET, DELETE
    """
    if request_type == 'POST':
        file = open('test_sig.jpg', 'r')
        image = file.read()
        self.r = requests.post('{}/{}'.format(url, '/image/test.jpg'), data=image, headers={'Content-Type': 'image/jpeg'})
    elif request_type == 'GET': 
        self.r = requests.get('{}/{}'.format(url, '/image/test.jpg'))
    elif request_type == 'DELETE': 
        self.r = requests.delete('{}/{}'.format(url, '/image/test.jpg'))

@when('I make an AWS POST /pdf request')
def make_pdf_request(self):
    """Makes a POST request to /pdf

    Arguments: self
    """
    file = open('test.tex', 'r')
    tex = file.read()
    self.r = requests.post('{}/{}'.format(url, '/pdf'), data=tex, headers={'Content-Type': 'application/octet-stream'})

@when('I make a bad AWS POST /pdf request')
def make_bad_pdf_request(self): 
    """Makes a bad POST request to /pdf

    Arguments: self
    """
    file = open('test_sig.jpg', 'r')
    tex = file.read()
    self.r = requests.post('{}/{}'.format(url, '/pdf'), data=tex, headers={'Content-Type': 'application/octet-stream'})

@then('the result is {value}')
def check_result(self, value):
    """Checks result is expected

    Arguments: 
        self
        value: the thing we're looking for -- success, failure, a pdf, or none
    """
    if value == 'success' or value == 'failure': 
        assert self.r.json()['result'] == value, 'result: {}'.format(self.r.json())
    elif value == 'a PDF': 
        assert b'\x25\x50\x44\x46' in bytearray(self.r.content), 'result was not a PDF'
    elif value == 'empty':
        assert self.r.content is '', 'result was not empty: {}'.format(self.r.content)

# [1] https://stackoverflow.com/questions/6186980/determine-if-a-byte-is-a-pdf-file re: byte string to use to determine if a file is PDF
# [2] https://realpython.com/python-requests/                                       re: using result.content
# [3] https://www.geeksforgeeks.org/python-bytearray-function/                      re: Dealing with bytes