import logging 
import datetime
import json

class InputValidatorTool:
    """Validates inputs to the employee-recognition-api.

    """
    def __init__(self):
        """Initialize InputValidatorTool class. Performs basic logging.
        
        Arguments: self
        
        Returns: void
        """
        logging.info('InputValidatorTool.__init__(): creating InputValidatorTool instance')  

    def template_response(self, field):
        """Creates a template error response to be added to 'errors' list and 
            eventually returned to the user.

        Arguments:
            self
            field: string. Field to include in error message

        Returns: 
            message dict as follows:
                { 'field': field, 'message': 'invalid value' }
        """
        logging.info('InputValidatorTool.template_response(): creating template error response for {}'.format(field))
        return {'field': field, 'message': 'invalid value'}

    def valid_password(self, password):
        """Validates password input is between 6 and 10 characters.

        Arguments:
            self
            password: string. Password to validate.

        Returns: 
            if valid: None
            if invalid: { 'field': 'password', 'message': 'invalid value' }
        """
        logging.info('InputValidatorTool.valid_password(): validating password is between 6 and 10 chars')
        if len(password) >= 6 and len(password) <= 10: 
            return None  
        else:
            return self.template_response('password') 

    def valid_email(self, email_address):
        """Validates email input is at least one character in length.

        Arguments:
            self
            email_address: string. Email address to validate.

        Returns: 
            if valid: None
            if invalid: { 'field': 'email_address', 'message': 'invalid value' }
        """
        logging.info('InputValidatorTool.valid_email(): validating email not empty')
        if len(email_address) >= 1: 
            return None  
        else:
            return self.template_response('email_address') 

    def valid_name(self, name, name_type): 
        """Validates name input is between 1 and 256 characters.

        Arguments:
            self
            name: string. Name to validate.
            name_type: string. Input key. Should be 'first_name' or 'last_name'

        Returns: 
            if valid: None
            if invalid: { 'field': '{name_type}', 'message': 'invalid value' }
        """
        logging.info('InputValidatorTool.valid_name(): validating name is between 2 and 256 chars')
        if len(name) >= 1 and len(name) <= 256:
            return None 
        else: 
            return self.template_response(name_type)

    def valid_time(self, time_string, time_type): 
        """Validates time input is of expected datetime format as defined by strptime().

        Arguments:
            self
            time_string: string. Time to validate.
            time_type: string. Input key. Should be 'created_timestamp' or 'awarded_datetime'

        Returns: 
            if valid: None
            if invalid: { 'field': '{time_type}', 'message': 'invalid value' }
        """
        logging.info('InputValidatorTool.valid_time(): validating time is in correct format YYYY-m-dd HH:MM:SS')
        try: 
            if datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S'): 
                return None
            
        except ValueError as e:
            return self.template_response(time_type)

    def valid_signature_path(self, signature_path):
        """Validates signature_path is of expected datetime format as defined by strptime().

        Arguments:
            self
            signature_path: string. Signature path to validate.

        Returns: 
            if valid: None
            if invalid: { 'field': 'signature_path', 'message': 'invalid value' }
        """
        logging.info('InputValidatorTool.valid_signature_path(): validating signature path includes \'.jpg\'')
        if '.jpg' in signature_path:
            return None 
        else: 
            return self.template_response('signature_path')

    def valid_type(self, type_string): 
        """Validates type is either 'week' or 'month'.

        Arguments:
            self
            type_string: string. Type to validate.

        Returns: 
            if valid: None
            if invalid: { 'field': 'type', 'message': 'invalid value' }
        """
        logging.info('InputValidatorTool.valid_type(): validating type is \'week\' or \'month\'')
        if type_string == 'week' or type_string == 'month':
            return None 
        else: 
            return self.template_response('type')

    def validate_users(self, request_type, data):
        """Validates all data for users POST/PUT requests.

        Arguments:
            self
            request_type: POST or PUT
            data: dict. Data contained in POST/PUT request to /users endpoint.
                keys: first_name, last_name, created_timestamp, password, email_address, signature_path

        Returns: 
            if valid: None
            if invalid: List of errors in format {'errors': [] }
        """
        # Validate each input, appending errors (if applicable) to 'errors' dict
        logging.info('InputValidatorTool.validate_users(): validating request data in /users request')
        result = { 'errors': [] } 
        valid_fname_result = self.valid_name(data['first_name'], 'first_name')
        if valid_fname_result is not None:
            result['errors'].append(valid_fname_result)
            
        valid_lname_result = self.valid_name(data['last_name'], 'last_name')
        if valid_lname_result is not None:
            result['errors'].append(valid_lname_result)

        valid_email_result = self.valid_email(data['email_address'])
        if valid_email_result is not None:
            result['errors'].append(valid_email_result) 

        valid_sig_result = self.valid_signature_path(data['signature_path'])
        if valid_sig_result is not None:
            result['errors'].append(valid_sig_result) 

        if request_type == 'POST': 
            valid_time_result = self.valid_time(data['created_timestamp'], 'created_timestamp') 
            if valid_time_result is not None:
                result['errors'].append(valid_time_result)

            valid_pass_result = self.valid_password(data['password'])
            if valid_pass_result is not None: 
                result['errors'].append(valid_pass_result) 

        if result == {'errors':[]}:
            logging.info('validate_users(): returning None')
            return None 
        else:
            logging.info('validate_users(): returning {}'.format(result))
            return result

    def validate_login(self, data): 
        """Validates password for users/admins PUT requests.

        Arguments:
            self
            data: dict. Data contained in POST/PUT request to /admins endpoint.
                keys: password

        Returns: 
            if valid: None
            if invalid: List of errors in format {'errors': [] }
        """
        logging.info('validating request data in /login request')
        result = { 'errors': [] } 

        valid_pass_result = self.valid_password(data['password'])
        if valid_pass_result is not None: 
            result['errors'].append(valid_pass_result) 
            
        if result == {'errors': []}:
            logging.info('returning None')
            return None 
        else:
            logging.info('returning {}'.format(result))
            return result


    def validate_admins(self, request_type, data):
        """Validates all data for admins POST/PUT requests.

        Arguments:
            self
            data: dict. Data contained in POST/PUT request to /admins endpoint.
                keys: first_name, last_name, created_timestamp, password, email_address

        Returns: 
            if valid: None
            if invalid: List of errors in format {'errors': [] }
        """
        logging.info('validating request data in /admins request')
        result = { 'errors': [] } 

        # Validate each input, appending errors (if applicable) to 'errors' dict
        valid_fname_result = self.valid_name(data['first_name'], 'first_name')
        if valid_fname_result is not None:
            result['errors'].append(valid_fname_result)
        
        valid_lname_result = self.valid_name(data['last_name'], 'last_name')
        if valid_lname_result is not None:
            result['errors'].append(valid_lname_result)
        
        valid_email_result = self.valid_email(data['email_address'])
        if valid_email_result is not None:
            result['errors'].append(valid_email_result)
        
        if request_type != 'PUT':
            valid_time_result = self.valid_time(data['created_timestamp'], 'created_timestamp') 
            if valid_time_result is not None:
                result['errors'].append(valid_time_result)

            valid_pass_result = self.valid_password(data['password'])
            if valid_pass_result is not None: 
                result['errors'].append(valid_pass_result) 

        if result == {'errors': []}:
            logging.info('returning None')
            return None 
        else:
            logging.info('returning {}'.format(result))
            return result

    def validate_awards(self, data):
        """Validates all data for awards POST requests.

        Arguments:
            self
            data: dict. Data contained in POST request to /awards endpoint.
                keys: type, awarded_datetime

        Returns: 
            if valid: None
            if invalid: List of errors in format {'errors': [] }
        """
        logging.info('InputValidatorTool.validate_awards(): validating request data in /awards request')
        result = { 'errors': [] } 

        valid_time_result = self.valid_time(data['awarded_datetime'], 'awarded_datetime') 
        if valid_time_result is not None:
            result['errors'].append(valid_time_result)

        valid_type_result = self.valid_type(data['type'])
        if valid_type_result is not None: 
            result['errors'].append(valid_type_result)

        if result == {'errors': []}:
            logging.info('returning None')
            return None
        else: 
            logging.info('returning {}'.format(result))
            return result


# [1] https://stackabuse.com/converting-strings-to-datetime-in-python/                                        re: parsing timestamp/datetime
# [2] https://stackoverflow.com/questions/8056496/python-get-unicode-string-size                             re: len()
# [3] https://www.afternerd.com/blog/python-string-contains/                                                re: contains string
# [4] https://stackoverflow.com/questions/41862525/valueerror-time-data-does-not-match-format-y-m-d-hms-f     re: use of ValueError as an exception to catch for time validation