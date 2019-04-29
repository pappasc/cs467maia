import json 
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

        # Setup initial connection to database
        self.db = sqlalchemy.create_engine('mysql+pymysql://{}:{}@{}/{}'.format(connxn_data['username'], connxn_data['password'], connxn_data['connection_name'], connxn_data['database']))
        self.connxn = self.db.connect()
        
        
    def disconnect(self): 
        """Disconnect from database

        Arguments: self

        Returns: void
        """
        self.connxn.close()
    
    def build_json_select(self, result, key=None): 
        """Transforms database result into JSON for SELECT queries

        Arguments:
            self 
            result:         ResultProxy object. Result from database query
            key:            string. Highest level key of query response 

        Returns: JSON parsed result, ready for use in employee-recognition-api
        """
        if result.returns_rows is not None and key is not None:
            iterations = 0
            result_dict = { '{}'.format(key): [] }
            row = result.fetchone()
            while row is not None: 
                result_sub_dict = { }
                for column in row.keys(): 
                    result_sub_dict[column] = '{}'.format(row[column]) 
                    
                    # Ensure returning int for ids
                    if 'id' in str(column): 
                        result_sub_dict[column] = int(result_sub_dict[column])     
                    elif 'distributed' == str(column):
                        # Python bools are opposite of MySQL?
                        result_sub_dict[column] = not bool(result_sub_dict[column])

                iterations += 1

                if iterations >= 1 and key is not None: 
                    result_dict[key].append(result_sub_dict)
                else: 
                    result_dict[column] = result_sub_dict[column]

                row = result.fetchone()

        elif result.returns_rows is not None and key is None: 
            result_dict = {} 
            row = result.fetchone()

            if row is not None: 
                for column in row.keys():
                    result_dict[column] = '{}'.format(row[column])

                    if 'id' in str(column): 
                        result_dict[column] = int(result_dict[column])
                    elif 'distributed' == str(column):
                        result_dict[column] = not bool(result_dict[column])

            else:  
                result_dict =  {
                    'errors': { 
                        'field': '_id',
                        'message': '_id does not exist' 
                    }
                }  
                
        result.close() 
        return json.dumps(result_dict)

    def build_json_insert(self, key, result):
        """Transforms database result into JSON for INSERT queries

        Arguments:
            self 
            result:         ResultProxy obj. Result from database query
            key:            string. 'user_id', 'admin_id', or 'award_id' 

        Returns: JSON parsed result, ready for use in employee-recognition-api
        """
        # Note: Does not tell if NOT inserted, this is verified in another way
        
        # Get the row id last touched and return in JSON with key provided
        id = result.lastrowid 
        result_dict = { 
            '{}'.format(key): '{}'.format(id)
        }
        return json.dumps(result_dict)

    def build_json_delete(self, key, result): 
        """Transforms database result into JSON for DELETE queries

        Arguments:
            self 
            result:         ResultProxy obj. Result from database query
            key:            string. 'user_id', 'admin_id', or 'award_id' 

        Returns: JSON parsed result, ready for use in employee-recognition-api
        """

        # If 1 row was modified, then return a JSON object with null value
        if result.rowcount == 1: 
            result_dict = { 
                '{}'.format(key): None 
            }

        # If 0 rows were modified, then return an error JSON object
        elif result.rowcount == 0: 
            result_dict = { 
                'errors': { 
                    'field': '{}'.format(key), 
                    'message': '{} does not exist'.format(key)  
                }
            }

        # We won't have a case where rowcount > 1, as only deleting 
        # using primary keys
        else: 
            result_dict = { 
                'errors': { 
                    'field': '{}'.format(key),
                    'message': 'Something is borked. More than one entry was deleted.'
                }
            }

        return json.dumps(result_dict)

    def get(self, table):
        """Select all users, admins, or awards information (excluding login information) 

        Arguments: 
            self
            table: string. 'users', 'admins', or 'awards'

        Returns: JSON parsed result of select query 
        """
        if table == 'users': 
            query = sqlalchemy.text('select * from users;')
            key = 'user_ids'
        elif table == 'admins': 
            query = sqlalchemy.text('select * from admins;')
            key = 'admin_ids'
        elif table == 'awards': 
            query = sqlalchemy.text('select * from awards;')
            key = 'award_ids'
        
        result = self.connxn.execute(query) 
        return self.build_json_select(result, key) 

    def get_by_id(self, table, data):
        """Select users, admins, or awards information (excluding login information) based on id 

        Arguments: 
            self
            table: string. 'users', 'admins', or 'awards'
            data: dictionary. Contains one of the following keys:
                data['user_id']: int
                data['admin_id']: int
                data['award_id']: int
        
        Returns: JSON parsed result of select query 
        """
        if table == 'users':
            query = sqlalchemy.text('select * from users where user_id = :id;')
            key = 'user_id'
        elif table == 'admins': 
            query = sqlalchemy.text('select * from admins where admin_id = :id;')
            key = 'admin_id'
        elif table == 'awards': 
            query = sqlalchemy.text('select * from awards where award_id = :id;')
            key = 'award_id'

        result = self.connxn.execute(query, id = data[key])     
        return self.build_json_select(result) 

    def get_login_by_id(self, table, data): 
        """Select user or admin login information based on id 

        Arguments: 
            self
            table: string. 'users' or 'admin'
            data: dictionary. Contains one of the following keys:
                data['user_id']: int 
                data['admin_id]: int

        Returns: JSON parsed result of select query 
        """
        if table == 'users': 
            query = sqlalchemy.text('select password from users where user_id = :id;')
            key = 'user_id'
        elif table == 'admins': 
            query = sqlalchemy.text('select password from admins where admin_id = :id;')
            key = 'admin_id'

        result = self.connxn.execute(query, id = data[key])
        return self.build_json_select(result) 

    def get_awards_by_filter(self, filter, data): 
        """Select awards information based on filter

        Arguments: 
            self
            filter: string. 'authorizing_user_id', 'receiving_user_id', 'type', 'awarded_datetime', or 'distributed'
            data: dictionary. Contains one key matching filter.
                data['authorizing_user_id']: int 
                data['receiving_user_id]: int
                data['type']: string
                data['awarded_datetime']: string
                data['distributed']: string

        Returns: JSON parsed result of select query 
        """

        if filter == 'authorizing_user_id': 
            query = sqlalchemy.text('select * from awards where authorizing_user_id = :key;')
            result = self.connxn.execute(query, key = int(data[filter]))
        elif filter == 'receiving_user_id': 
            query = sqlalchemy.text('select * from awards where receiving_user_id = :key;')
            result = self.connxn.execute(query, key = int(data[filter]))
        elif filter == 'type': 
            query = sqlalchemy.text('select * from awards where type = :key;')
            result = self.connxn.execute(query, key = data[filter])
        elif filter == 'awarded_datetime': 
            query = sqlalchemy.text('select * from awards where awarded_datetime >= :key;')
            result = self.connxn.execute(query, key = data[filter])
        elif filter == 'distributed': 
            query = sqlalchemy.text('select * from awards where distributed = :key;')
            result = self.connxn.execute(query, key = bool(data[filter]))
        
        return self.build_json_select(result, 'award_ids') 

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

        Returns: JSON parsed result of insertion query 
        """
        if table == 'users':
            query = sqlalchemy.text('insert into users (first_name, last_name, email_address, password, created_timestamp, signature_path) values (:first_name, :last_name, :email_address, :password, :created_timestamp, :signature_path)')
            result = self.connxn.execute(query, first_name = data['first_name'], last_name = data['last_name'], email_address = data['email_address'], password = data['password'], created_timestamp = data['created_timestamp'], signature_path = data['signature_path'])
            key = 'user_id'

        elif table == 'admins': 
            query = sqlalchemy.text('insert into admins (first_name, last_name, email_address, password, created_timestamp) values (:first_name, :last_name, :email_address, :password, :created_timestamp)')
            result = self.connxn.execute(query, first_name = data['first_name'], last_name = data['last_name'], email_address = data['email_address'], password = data['password'], created_timestamp = data['created_timestamp'])
            key = 'admin_id'

        elif table == 'awards': 
            query = sqlalchemy.text('insert into awards (authorizing_user_id, receiving_user_id, type, distributed, awarded_datetime) values (:authorizing_user_id, :receiving_user_id, :type, :distributed, :awarded_datetime)')
            result = self.connxn.execute(query, authorizing_user_id = data['authorizing_user_id'], receiving_user_id = data['receiving_user_id'], distributed = data['distributed'], awarded_datetime = data['awarded_datetime'], type = data['type'])
            key = 'award_id'
        
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

        Returns: JSON parsed result of update query 
        """
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

        # TODO: Find a way to check success without doing a secondary select command
        result = self.connxn.execute(verify_query, id=int(data[key]))
        return self.build_json_select(result)

    def delete_by_id(self, table, data):
        """Delete from users, admins, or awards table based on user_id 

        Arguments: 
            self
            table: string. 'users', 'admins', or 'awards'
            data: dictionary. Contains one of the following keys
                data['user_id']: int
                data['admin_id]: int
                data['award_id]: int
        
        Returns: JSON parsed result of delete query 
        """
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

        result = self.connxn.execute(query, id = int(data[key]))
        return self.build_json_delete(key, result)
        
# References:
# [1] https://cloud.google.com/sql/docs/mysql/connect-app-engine re: create_engine()
# [2] https://flask-sqlalchemy.palletsprojects.com/en/2.x/
# [3] https://cloud.google.com/sql/docs/mysql/manage-connections re: sanitizing inputs with execute()
# [4] https://docs.sqlalchemy.org/en/13/core/connections.html re: execute(), close(), parsing result variable
# [5] https://www.tutorialspoint.com/sql/sql-update-query.htm re: update sql
# [6] https://www.tutorialspoint.com/sql/sql-insert-query.htm re: insert sql
# [7] https://docs.python-guide.org/scenarios/json/ re: building json strings
# [8] https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/cloud-sql/mysql/sqlalchemy/main.py re: how to import sqlalchemy, string URL for connection
# [9] https://stackoverflow.com/questions/27766794/switching-from-sqlite-to-mysql-with-flask-sqlalchemy 
# [10] https://docs.sqlalchemy.org/en/13/core/pooling.html#pool-disconnects re: engine.dispose()
# [11] https://cloud.google.com/sql/docs/mysql/connect-external-app#python re: connection via sqlalchemy & tcp to localhost
# [12] https://kite.com/python/docs/sqlalchemy.engine.result.ResultProxy re: parsing result
# [13] https://stackoverflow.com/questions/40854861/typeerror-instancemethod-object-is-not-iterable-python re: use of .keys() rather than .keys for iteration
# [14] https://docs.python.org/2/library/json.html re: use of json.dumps <--> python dict
# [15] https://docs.python.org/2/tutorial/datastructures.html re: use of append
# [16] https://stackoverflow.com/questions/19288842/programmingerror-1064-you-have-an-error-in-your-sql-syntax-check-the-manual re: use of single quotations
# [17] https://kite.com/python/docs/sqlalchemy.text re: sanitizing input, use of text()
# [18] https://kite.com/python/docs/sqlalchemy.engine.result.RowProxy re: parsing RowProxy
# [19] https://docs.sqlalchemy.org/en/13/core/tutorial.html re: how to write textual SQL 
# [20] https://stackoverflow.com/questions/7030831/how-do-i-get-the-opposite-negation-of-a-boolean-in-python re: use of not bool