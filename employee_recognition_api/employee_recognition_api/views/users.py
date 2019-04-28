from flask import Flask 

app = Flask(__name__)

# TODO: Does not work yet
@app.route('/')
def test():
	connection_data = { 
		'username': 'api_user', 
		'password': 'tj348$', 
		'database': 'maia',
		'connection_name': '127.0.0.1' 
	}
	
	query = QueryTool(connection_data)
	result = query.get('users')
	print('{}'.format(result))

	query.disconnect()

# references 
# [1] http://flask.pocoo.org/docs/1.0/quickstart/