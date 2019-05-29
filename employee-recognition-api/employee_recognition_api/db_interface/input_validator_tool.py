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
        
        if request_type == 'POST':
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

    def check_users_exist(self, authorizing_user_id, receiving_user_id):
        """Check that the users involved in award exist

        Arguments:
            authorizing_user_id:    int. ID of authorizing user
            receiving_user_id:      int. ID of receiving user

        Returns:
            True if both users exist
            error dictionary if a user does not exist
                will either return error re: authorizing_user_id or 
                error re: receiving_user_id. Won't return both errors at this time.
        """
        # Query database to determine if user ids exist, and continue if so; otherwise, return errors
        logging.info('awards_api: checking if user_ids {} and {} exist'.format(receiving_user_id, authorizing_user_id))
        query = QueryTool(connection_data)
        result1 = query.get_by_id('users', {
            'user_id': authorizing_user_id 
        })    
        result2 = query.get_by_id('users', {
            'user_id': receiving_user_id
        })
        
        # Check authorizing user_id, if result had errors then return those errors
        try: 
            if result1['errors'] is not None:
                status_code = 400
                logging.info('awards_api.check_users_exist(): {}'.format(result1))
                result = result1
        # If authorizing_user_id result did not have errors, check receiving_user_id 
        except KeyError:
            try: 
                if result2['errors'] is not None: 
                    logging.info('awards_api.check_users_exist(): returning {}'.format(result2))
                    result = result2
            except KeyError:
                logging.info('awards_api: user_ids found')
                result = True

        query.disconnect()
        return result 

    def check_award_does_not_exist(self, type_string, awarded_datetime):
        """Check the employee of the month/week awards do not 
            already exist in the time period associated with our award
            Example: 
                - If award of type 'month' is awarded on '2019-05-01 0:00:00'
                    then checks that no other 'month' awards exist in May 2019.
                - If award of type 'week' is awarded on '2019-05-01 0:00:00'
                    then checks that no other 'week' awards exist from Mon, April 29 2019
                    to Sun, May 5, 2019.
        Arguments: 
            type_string:        string. 'month', 'year'
            awarded_datetime:   string. 'YYYY-mm-DD HH:MM:SS'

        Returns:
            True if no awards are found in the time period

        """
        query = QueryTool(connection_data)
        # Check if more awards are acceptable during time period 
        result = True # default is to accept the award

        # Employee of the Month
        if type_string == 'month': 
            # Identify date range for month to compare against
            month = datetime.datetime.strptime(awarded_datetime, '%Y-%m-%d %H:%M:%S').month
            year = datetime.datetime.strptime(awarded_datetime, '%Y-%m-%d %H:%M:%S').year

            # Find existing awards during month range identified. If found, return errors and do not continue
            greater = str(datetime.datetime(year, month, 1, 0, 0, 0, 0))
            
            # Handle December differently (can't just add 1 to 12)
            if month == 12: 
                lesser_month = 1
            else: 
                lesser_month = month + 1 
            lesser = str(datetime.datetime(year, lesser_month, 1, 0, 0, 0))
            
            blob = { 
                'awarded_datetime': {
                    'greater': greater, 
                    'lesser': lesser 
                }, 
                'type': 'month'
            }
            existing_awards = query.get_awards_by_filter('awarded_datetime', blob, True)
            logging.info('awards_api.check_award_does_not_exist(): existing_awards: {}'.format(existing_awards))

            # If awards found, return an error dictionary. Otherwise continue.
            if len(existing_awards['award_ids']) != 0:
                logging.info('awards_api.check_award_does_not_exist(): Awards found during time period')
                result = {'errors': [{'field': 'type', 'message': 'too many awards of month type in time period'}]}
            else: 
                logging.info('awards_api.check_award_does_not_exist(): No awards found during time period')

        # Employee of the Week
        elif type_string == 'week':
            # Determine what day of the week our day is 
            # 1 2 3 4 5 6 7
            # M T W T F S S
            parsed_datetime = datetime.datetime.strptime(awarded_datetime, '%Y-%m-%d %H:%M:%S')
            weekday_number = parsed_datetime.isoweekday()
            year = parsed_datetime.year
            month = parsed_datetime.month
            day = parsed_datetime.day 
            logging.info('awards_api.check_award_does_not_exist(): weekday_number is {}'.format(weekday_number))

            # Get the beginning and end of week based on this


            beg_of_week = datetime.datetime(year, month, day, 0, 0, 0) - datetime.timedelta(days=weekday_number - 1)
            end_of_week = datetime.datetime(year, month, day, 0, 0, 0) + datetime.timedelta(days=8 - weekday_number)
            logging.info('awards_api.check_award_does_not_exist(): beginning of week: {}'.format(beg_of_week))
            logging.info('awards_api.check_award_does_not_exist(): end of week: {}'.format(end_of_week))

            # Query database for awards that exist in this week time period
            greater = str(beg_of_week)
            lesser = str(end_of_week)
            blob = { 
                'awarded_datetime': {
                    'greater': greater, 
                    'lesser': lesser 
                }, 
                'type': 'week'
            }
            logging.info('blob: {}'.format(blob))
            existing_awards = query.get_awards_by_filter('awarded_datetime', blob, True)
            logging.info('awards_api.check_award_does_not_exist(): existing_awards: {}'.format(existing_awards))
            
            # If awards found, return error dictionary. Otherwise continue.
            if len(existing_awards['award_ids']) != 0:
                logging.info('awards_api.check_award_does_not_exist(): Awards found during time period')
                result = {'errors': [{'field': 'type', 'message': 'too many awards of week type in time period'}]}
            else: 
                logging.info('awards_api.check_award_does_not_exist(): No awards found during time period')

        query.disconnect()
        return result

# [1] https://stackabuse.com/converting-strings-to-datetime-in-python/                                        re: parsing timestamp/datetime
# [2] https://stackoverflow.com/questions/8056496/python-get-unicode-string-size                             re: len()
# [3] https://www.afternerd.com/blog/python-string-contains/                                                re: contains string
# [4] https://stackoverflow.com/questions/41862525/valueerror-time-data-does-not-match-format-y-m-d-hms-f     re: use of ValueError as an exception to catch for time validation
# [5] https://docs.python.org/2/library/datetime.html                                                           re: datetime obj
# [6] https://stackoverflow.com/questions/19480028/attributeerror-datetime-module-has-no-attribute-strptime     re: use of strptime
# [7] https://stackoverflow.com/questions/2600775/how-to-get-week-number-in-python                              re: isocalendar
# [8] https://stackoverflow.com/questions/6871016/adding-5-days-to-a-date-in-python?rq=1                        re: using timedelta
# [9] https://stackoverflow.com/questions/19216334/python-give-start-and-end-of-week-data-from-a-given-date     re: ideas on how to accomplish getting first and last day of a week