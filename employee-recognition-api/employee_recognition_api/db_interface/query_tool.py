import json 
import logging
from flask_sqlalchemy import sqlalchemy

class QueryTool:
    """Connects employee-recognition-api to Google Cloud SQL database. Driver for DB interactions.

    """

    def __init__(self, connxn_data): 
        """Initialize connection (self.connxn) to Google Cloud SQL database (or proxy).

        Arguments: 
            self
            app: Flask application instance
            connxn_data: dictionary containing variables for database connection 
                connxn_data['username']: username for connection to database
                connxn_data['password']: password for connection to database
                connxn_data['database']: database name
                connxn_data['connection_name']: name of cloud sql instance 

        Returns: void
        """
        # Setup sqlalchemy connection engine for database connection 
        try: 
            # Production environment set-up
            if connxn_data['environment'] == 'prod': 
                logging.info('QueryTool.__init__(): creating engine in production')
                self.db = sqlalchemy.create_engine(
                    sqlalchemy.engine.url.URL(
                        drivername='mysql+pymysql', 
                        username=connxn_data['username'],
                        password=connxn_data['password'],
                        database=connxn_data['database'],
                        query={
                            'unix_socket': '/cloudsql/{}'.format(connxn_data['connection_name'])
                        }
                    ))
            # Development environment set-up
            elif connxn_data['environment'] == 'dev' or connxn_data['environment'] == 'local':
                logging.info('QueryTool.__init__(): creating engine in dev')
                self.db = sqlalchemy.create_engine(
                    'mysql+pymysql://{}:{}@{}/{}'.format(connxn_data['username'], connxn_data['password'], connxn_data['connection_name'], connxn_data['database'],
                ))
  
        # Log any errors encountered for trouble-shooting
        except Exception as e: 
            logging.info('QueryTool.__init__(): exception thrown on engine creation. {}'.format(e))
            raise e

        # Use engine to connect to database -- either Google Cloud SQL or Google Cloud SQL Proxy
        try: 
            logging.info('QueryTool.__init__(): connecting to db')
            self.connxn = self.db.connect()
        
        # Log any errors encountered for trouble-shooting
        except Exception as e: 
            logging.info('QueryTool.__init__(): exception thrown on db connection. {}'.format(e))
            raise e

    def disconnect(self): 
        """Disconnect from database

        Arguments: self

        Returns: void
        """
        logging.info('QueryTool.disconnect(): closing connection to db')
        self.connxn.close()


    # Note: build_json_* functions are a bit of a misnomer. They originally returned JSON objects, but now they only 
    #       return parsed dictionaries, to later be dumped to JSON.
    
    def build_json_select(self, result, key, expect_one=False): 
        """Transforms SELECT query results into parsed dictionary

        Arguments:
            self 
            result:         ResultProxy object. Result from database query
            key:            string. Highest level key of query response
            expect_one:     bool. 
                True: only one row is expected. 
                False: more than one row is expected.         

        Returns: Parsed dictionary result
            if no rows returned: { 'errors': [ ] }
            if one row expected & returned: { 'column': 'value', 'column': 'value' }
            otherwise: { 'key': [ ] }
        """
        iterations = 0
        result_dict = { '{}s'.format(key): [] }

        # Parse result of a GET function that is expected to return many rows
        if result.returns_rows is not None:
            
            # While we can retrieve rows from result, return parsed dict data
            row = result.fetchone()
            while row is not None: 
                result_sub_dict = {}
                iterations += 1

                # Iterate through each column of result to parse the data
                for column in row.keys():
                    # Ensure returning int for any *_id column
                    if 'id' in str(column): 
                        result_sub_dict[column] = int(row[column])     
                    # Ensure returning a bool for 'distributed' column
                    elif 'distributed' == str(column):
                        result_sub_dict[column] = bool(row[column])
                    # Otherwise, return the value as a string
                    else: 
                        result_sub_dict[column] = str(row[column])
                result_dict['{}s'.format(key)].append(result_sub_dict)    
                row = result.fetchone()
                
            # Return the result dictionary based on the number of rows returned
            # If no rows returned, then there was an error so return an error dict  
            if iterations == 0:
                result_dict = {
                    'errors': [{ 
                        'field': '{}'.format(key),
                        'message': '{} does not exist'.format(key)
                    }]
                }  
            # If we expected one row to be returned and we saw one row returned, use 
            # the dict format:
            # { 'column': 'data', 'column': 'data', etc. }
            elif iterations == 1 and expect_one is True:  
                result_dict = result_sub_dict

            # In all other cases, use the default dict created in the format: 
            # { 'key': [ { }, { }, { } ] }

        result.close() 
        logging.info('QueryTool.build_json_select(): returning {}'.format(result_dict))
        return result_dict


    def build_json_insert(self, key, result):
        """Transforms INSERT query result into parsed dictionary. This does
            NOT verify the data is actually inserted -- this is done in another way.

        Arguments:
            self 
            key:            string. 'user_id', 'admin_id', or 'award_id' 
            result:         ResultProxy obj. Result from database query

        Returns: Parsed dictionary result
            i.e. { 'key': 'last_id' }
        """
        # Get the row id last touched and return a dict with this information
        last_id = result.lastrowid
        result_dict = { 
            '{}'.format(key): '{}'.format(last_id)
        }
        logging.info('QueryTool.build_json_insert(): returning {}'.format(result_dict))
        return result_dict

    def build_json_delete(self, key, result): 
        """Transforms DELETE query result into parsed dictionary

        Arguments:
            self 
            result:         ResultProxy obj. Result from database query
            key:            string. 'user_id', 'admin_id', or 'award_id' 

        Returns: Parsed dictionary result
        """

        # If 1 row was modified, then return a parsed dictionary with null value
        if result.rowcount == 1: 
            result_dict = { 
                '{}'.format(key): None 
            }

        # If 0 rows were modified, then return an error dictionary 
        elif result.rowcount == 0: 
            result_dict = { 
                'errors': [ { 
                    'field': '{}'.format(key), 
                    'message': '{} does not exist'.format(key)  
                } ]
            }

        # We won't have a case where rowcount > 1, as only deleting 
        # using primary keys. So, in this case return an error dictionary.
        else: 
            result_dict = { 
                'errors': [ { 
                    'field': '{}'.format(key),
                    'message': 'Something is borked. More than one entry was deleted.'
                } ]
            }

        logging.info('QueryTool.build_json_delete(): returning: {}'.format(result_dict))
        return result_dict

    def get(self, table):
        """Select all users, admins, or awards information (excluding login information) 

        Arguments: 
            self
            table: string. 'users', 'admins', or 'awards'

        Returns: Parsed dictionary result of select query in the format { 'key': [ ] }
        """ 

        # Create SELECT query based on table
        if table == 'users': 
            query = sqlalchemy.text('select user_id, first_name, last_name, created_timestamp, email_address, signature_path from users;')
            key = 'user_id'
        elif table == 'admins': 
            query = sqlalchemy.text('select admin_id, first_name, last_name, created_timestamp, email_address from admins;')
            key = 'admin_id'
        elif table == 'awards': 
            query = sqlalchemy.text('select * from awards;')
            key = 'award_id'
        logging.info('QueryTool.get(): query is {}'.format(str(query)))

        # Execute SELECT query & return parsed dictionary result
        result = self.connxn.execute(query)
        return self.build_json_select(result, key, False)

    def get_by_id(self, table, data):
        """Select users, admins, or awards information (excluding login information) based on id 

        Arguments: 
            self
            table: string. 'users', 'admins', or 'awards'
            data: dictionary. Contains one of the following keys:
                data['user_id']: int
                data['admin_id']: int
                data['award_id']: int
        
        Returns: Parsed dictionary result of select query in the format { 'column': 'value', 'column': 'value', 'column': 'value' }
        """
        # Create SELECT query based on table
        if table == 'users':
            query = sqlalchemy.text('select user_id, first_name, last_name, email_address, created_timestamp, signature_path from users where user_id = :id;')
            key = 'user_id'
        elif table == 'admins': 
            query = sqlalchemy.text('select admin_id, first_name, last_name, email_address, created_timestamp from admins where admin_id = :id;')
            key = 'admin_id'
        elif table == 'awards': 
            query = sqlalchemy.text('select * from awards where award_id = :id;')
            key = 'award_id'
        logging.info('QueryTool.get_by_id(): query is {}'.format(str(query)))

        # Execute query & return parsed dictionary result
        result = self.connxn.execute(query, id = data[key]) 
        return self.build_json_select(result, key, True) 

    def get_login_by_id(self, table, data): 
        """Select user or admin login information based on id 

        Arguments: 
            self
            table: string. 'users' or 'admin'
            data: dictionary. Contains one of the following keys:
                data['user_id']: int 
                data['admin_id]: int

        Returns: Parsed dictionary result of select query in the form of { 'password': '{password}' } 
        """

        # Create query based on table
        if table == 'users': 
            query = sqlalchemy.text('select password from users where user_id = :id;')
            key = 'user_id'
        elif table == 'admins': 
            query = sqlalchemy.text('select password from admins where admin_id = :id;')
            key = 'admin_id'
        logging.info('QueryTool.get_login_by_id(): query is {}'.format(str(query)))

        # Execute query & return parsed dictionary result
        result = self.connxn.execute(query, id = data[key])
        return self.build_json_select(result, key, True) 

    def get_awards_by_filter(self, filter, data, between=False): 
        """Select awards information based on filter

        Arguments: 
            self
            filter: string. 'authorizing_user_id', 'receiving_user_id', 'type', 'awarded_datetime', or 'distributed'
            between: bool. Indication of if awarded_datetime is treated as a range or not.
            data: dictionary. Contains one key matching filter.
                data['authorizing_user_id']: int 
                data['receiving_user_id]: int
                data['type']: string

                if between == True: 
                    data['awarded_datetime']['lesser']: string
                    data['awarded_datetime]['greater']: string
                else: 
                    data['awarded_datetime']: string 
                data['distributed']: string

        Returns: Parsed dictionary result of select query in the form of { 'award_ids': [] }
        """
        # Create & execute SELECT query, return parsed dictionary result
        if filter == 'authorizing_user_id': 
            query = sqlalchemy.text('select * from awards where authorizing_user_id = :key;')
            result = self.connxn.execute(query, key = int(data[filter]))
        elif filter == 'receiving_user_id': 
            query = sqlalchemy.text('select * from awards where receiving_user_id = :key;')
            result = self.connxn.execute(query, key = int(data[filter]))
        elif filter == 'type': 
            query = sqlalchemy.text('select * from awards where type = :key;')
            result = self.connxn.execute(query, key = data[filter])
        elif filter == 'awarded_datetime' and between == False: 
            query = sqlalchemy.text('select * from awards where awarded_datetime >= :key;')
            result = self.connxn.execute(query, key = data[filter])
        elif filter == 'awarded_datetime' and between == True: 
            # This is only used internally to determine if too many awards for a given week/month
            query = sqlalchemy.text('select * from awards where type = :key3 and awarded_datetime >= :key1 and awarded_datetime < :key2;')
            result = self.connxn.execute(query, key1 = data[filter]['greater'], key2 = data[filter]['lesser'], key3 = data['type'])
        elif filter == 'distributed': 
            query = sqlalchemy.text('select * from awards where distributed = :key;')
            result = self.connxn.execute(query, key = bool(data[filter]))
        logging.info('QueryTool.get_awards_by_filter(): query is {}'.format(str(query)))
        return self.build_json_select(result, 'award_id', False) 

    def post(self, table, data):
        """Insert into users, admins, or awards table 

        Arguments:
            self 
            table: string. 'users', 'admins' or 'awards'
            data: dictionary. Containing query information based on the table:
                users
                data['first_name']: string
                data['last_name']: string
                data['password']: string
                data['email_address']: string
                data['created_timestamp']: string
                data['signature_path']: string

                admins
                data['first_name']: string
                data['last_name']: string
                data['password']: string
                data['email_address']: string
                data['created_timestamp']: string

                awards 
                data['authorizing_user_id']: int
                data['receiving_user_id']: int
                data['type']: string
                data['distributed']: string
                data['awarded_datetime']: string

        Returns: Parsed dictionary result of insertion query in format { 'key': int(id) }
        """
        # Create INSERT query based on table, execute & return parsed response
        if table == 'users':
            query = sqlalchemy.text('insert into users (first_name, last_name, email_address, password, created_timestamp, signature_path) values (:first_name, :last_name, :email_address, :password, :created_timestamp, :signature_path);')
            result = self.connxn.execute(query, first_name = data['first_name'], last_name = data['last_name'], email_address = data['email_address'], password = data['password'], created_timestamp = data['created_timestamp'], signature_path = data['signature_path'])
            key = 'user_id'

        elif table == 'admins': 
            query = sqlalchemy.text('insert into admins (first_name, last_name, email_address, password, created_timestamp) values (:first_name, :last_name, :email_address, :password, :created_timestamp);')
            result = self.connxn.execute(query, first_name = data['first_name'], last_name = data['last_name'], email_address = data['email_address'], password = data['password'], created_timestamp = data['created_timestamp'])
            key = 'admin_id'

        elif table == 'awards': 
            query = sqlalchemy.text('insert into awards (authorizing_user_id, receiving_user_id, type, distributed, awarded_datetime) values (:authorizing_user_id, :receiving_user_id, :type, :distributed, :awarded_datetime);')
            result = self.connxn.execute(query, authorizing_user_id = data['authorizing_user_id'], receiving_user_id = data['receiving_user_id'], distributed = data['distributed'], awarded_datetime = data['awarded_datetime'], type = data['type'])
            key = 'award_id'

        logging.info('QueryTool.post(): query is {}'.format(str(query)))
        return self.build_json_insert(key, result) 
    
    def put_by_id(self, table, data):
        """Update users or admins table based on id 

        Arguments: 
            self 
            table: string. 'users' or 'admins'
            data: dictionary. Containing query information based on the table:

                users
                data['user_id']: int
                data['first_name']: string
                data['last_name']: string
                data['password']: string
                data['email_address']: string
                data['created_timestamp']: string
                data['signature_path']: string

                admins
                data['admin_id']: int
                data['first_name']: string
                data['last_name']: string
                data['password']: string
                data['email_address']: string
                data['created_timestamp']: string

        Returns: Parsed dictionary result of update query in format { 'key': int(id) }
        """
        # Create UPDATE and SELECT query based on table, execute and return parsed dictionary result
        # SELECT query effectively verifies that the entry still exists in the table, instead of relying on 
        # request data to make the response
        if table == 'users': 
            query = sqlalchemy.text('update users set first_name = :first_name, last_name = :last_name, email_address = :email_address, password = :password, created_timestamp = :created_timestamp, signature_path = :signature_path where user_id = :user_id;')
            result = self.connxn.execute(query, first_name = data['first_name'], last_name=data['last_name'], email_address=data['email_address'], password=data['password'], created_timestamp=data['created_timestamp'], signature_path=data['signature_path'], user_id=int(data['user_id']))
            verify_query = sqlalchemy.text('select user_id from users where user_id = :id;')
            key = 'user_id'
        elif table == 'admins': 
            query = sqlalchemy.text('update admins set first_name = :first_name, last_name = :last_name, email_address = :email_address, password = :password, created_timestamp = :created_timestamp where admin_id = :admin_id;')
            result = self.connxn.execute(query, first_name = data['first_name'], last_name=data['last_name'], email_address=data['email_address'], password=data['password'], created_timestamp=data['created_timestamp'], admin_id=int(data['admin_id']))
            verify_query = sqlalchemy.text('select admin_id from admins where admin_id = :id;')
            key = 'admin_id'

        logging.info('QueryTool.put(): update query is {}'.format(str(query)))
        logging.info('QueryTool.put(): select query is {}'.format(str(verify_query)))
        result = self.connxn.execute(verify_query, id=int(data[key]))
        return self.build_json_select(result, key, True)

    def delete_by_id(self, table, data):
        """Delete from users, admins, or awards table based on user_id 

        Arguments: 
            self
            table: string. 'users', 'admins', or 'awards'
            data: dictionary. Contains one of the following keys
                data['user_id']: int
                data['admin_id]: int
                data['award_id]: int
        
        Returns: Parsed dictionary result of delete query in the format { 'key': int(id) }
        """
        # Create query based on table
        key = None
        if table == 'users': 
            query = sqlalchemy.text('delete from users where user_id = :id;')
            key = 'user_id'

        elif table == 'admins': 
            query = sqlalchemy.text('delete from admins where admin_id = :id;')
            key = 'admin_id'

        elif table == 'awards': 
            query = sqlalchemy.text('delete from awards where award_id = :id;')
            key = 'award_id'
        logging.info('QueryTool.delete_by_id(): query is {}'.format(str(query)))

        # Execute query and return parsed dictionary result
        result = self.connxn.execute(query, id = int(data[key]))
        return self.build_json_delete(key, result)
        
# References:
# [1] https://cloud.google.com/sql/docs/mysql/connect-app-engine                                                                        re: create_engine()
# [2] https://flask-sqlalchemy.palletsprojects.com/en/2.x/
# [3] https://cloud.google.com/sql/docs/mysql/manage-connections                                                                        re: sanitizing inputs with execute(), connection variables
# [4] https://docs.sqlalchemy.org/en/13/core/connections.html                                                                           re: execute(), close(), parsing result variable
# [5] https://www.tutorialspoint.com/sql/sql-update-query.htm                                                                           re: update sql
# [6] https://www.tutorialspoint.com/sql/sql-insert-query.htm                                                                           re: insert sql
# [7] https://docs.python-guide.org/scenarios/json/                                                                                     re: building json strings
# [8] https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/cloud-sql/mysql/sqlalchemy/main.py                         re: how to import sqlalchemy, string URL for connection
# [9] https://stackoverflow.com/questions/27766794/switching-from-sqlite-to-mysql-with-flask-sqlalchemy 
# [10] https://docs.sqlalchemy.org/en/13/core/pooling.html#pool-disconnects                                                             re: engine.dispose()
# [11] https://cloud.google.com/sql/docs/mysql/connect-external-app#python                                                              re: connection via sqlalchemy & tcp to localhost
# [12] https://kite.com/python/docs/sqlalchemy.engine.result.ResultProxy                                                                re: parsing result
# [13] https://stackoverflow.com/questions/40854861/typeerror-instancemethod-object-is-not-iterable-python                              re: use of .keys() rather than .keys for iteration
# [14] https://docs.python.org/2/library/json.html                                                                                      re: use of json.dumps <--> python dict
# [15] https://docs.python.org/2/tutorial/datastructures.html                                                                           re: use of append
# [16] https://stackoverflow.com/questions/19288842/programmingerror-1064-you-have-an-error-in-your-sql-syntax-check-the-manual         re: use of single quotations
# [17] https://kite.com/python/docs/sqlalchemy.text                                                                                     re: sanitizing input, use of text()
# [18] https://kite.com/python/docs/sqlalchemy.engine.result.RowProxy                                                                   re: parsing RowProxy
# [19] https://docs.sqlalchemy.org/en/13/core/tutorial.html                                                                             re: how to write textual SQL 
