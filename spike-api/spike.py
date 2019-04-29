from flask import Flask 
from google.appengine.api import urlfetch
from google.appengine.api import mail

app = Flask(__name__)

# GET /
@app.route('/', methods=['GET'])
def test():
	"""GET / endpoint

	Sends message back to user 'This it the test endpoint'

	"""
	
	return 'This is the test endpoint.'

# GET /email
@app.route('/email', methods=['GET'])
def email():
	"""GET /email endpoint
	
	Sends a test email from kvavlen@oregonstate.edu to tasha@kvavle.com [3, 4]

	"""

	try: 
		mail.send_mail(sender='kvavlen@oregonstate.edu',
						to='tasha@kvavle.com',
						subject='test',
						body='testestest')
	except Exception as e:
		print(e)

	return 'Success'

# GET /file
@app.route('/file', methods=['GET'])
def file():
	"""GET /file endpoint
	
	Saves a test file to the google cloud storage bucket for application [5-11]

	"""
	
	url = 'https://www.googleapis.com/upload/storage/v1/b/maia-backend.appspot.com/o?uploadType=media&name=signatures/test.jpg'
	headers = {
		'Content-Type': 'image/jpeg',
		'Authorization': 'Bearer ya29.Glz0BogAxpVghh5vM4fZnHYHS5pOMCA6LfB5CD-QaGmIMrfwdZu8Di7Rsq8xiTRi5vjMap7x5pk5fpcYvNf14IYUKIfVX2QK0bYAPm9795JrDbqv52EeWxX1Vn-_bw',
	}

	# convert test.jpg to bytearray [11]
	with open("test.jpg", "rb") as img:
		i = img.read() 
		payload = bytearray(i)
	
	result = urlfetch.fetch(
		url=url,
		payload=payload, 
		method=urlfetch.POST, 
		headers=headers
	)

	print(result.status_code)	

	return 'success'

# references (based code off of these resources)
# [1] http://flask.pocoo.org/docs/1.0/quickstart/
# [2] https://docs.python.org/2/tutorial/inputoutput.html
# [3] https://cloud.google.com/appengine/docs/standard/python/mail/
# [4] https://cloud.google.com/appengine/docs/standard/python/mail/sending-mail-with-mail-api 
# [5] https://cloud.google.com/storage/docs/uploading-objects 
# [6] https://docs.python.org/3/tutorial/errors.html
# [7] https://stackoverflow.com/questions/1483429/how-to-print-an-exception-in-python
# [8] https://cloud.google.com/storage/docs/json_api/v1/how-tos/simple-upload
# [9] https://cloud.google.com/appengine/docs/standard/python/issue-requests
# [10] https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app
# [11] https://stackoverflow.com/questions/22351254/python-script-to-convert-image-into-byte-array

# references (reviewed, but ultimately not used for working spike)
# failed attempts included use of libraries: webob, requests/requests-toolbelt, cloudstorage as well as command line utilities gsutil, curl
# [12] http://flask.pocoo.org/docs/1.0/patterns/fileuploads/#uploading-files
# [13] https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/storage/cloud-client/snippets.py 
# [14] https://pypi.org/project/google-cloud-storage/ 
# [15] https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python 
# [16] https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/app-engine-cloud-storage-sample#write-to-bucket
# [17] https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/functions#open
# [18] https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.ext.cloudstorage.common
# [19] https://cloud.google.com/appengine/docs/standard/python/refdocs/modules/google/appengine/ext/cloudstorage/common#set_access_token
# [20] https://github.com/GoogleCloudPlatform/appengine-gcs-client/blob/master/python/test/common_test.py re: how to import common, rather than cloudstorage
# [21] https://github.com/GoogleCloudPlatform/appengine-gcs-client/blob/master/python/src/cloudstorage/cloudstorage_api.py
# [22] https://github.com/GoogleCloudPlatform/appengine-gcs-client/blob/master/python/test/cloudstorage_test.py 
# [23] https://docs.pylonsproject.org/projects/webob/en/stable/reference.html#request
# [24] https://docs.python.org/2.7/library/stdtypes.html#file-objects
# [25] https://docs.pylonsproject.org/projects/webob/en/stable/api/request.html
# [26] https://cloud.google.com/storage/docs/gsutil/commands/cp
# [27] https://stackoverflow.com/questions/450285/executing-command-line-programs-from-within-python
# [28] https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/setting-up-cloud-storage 
# [29] https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
# [30] https://toolbelt.readthedocs.io/en/latest/adapters.html#appengineadapter
# [31] https://www.geeksforgeeks.org/working-images-python/ re: using PIL 
# [32] https://pypi.org/project/urlfetch/
# [33] https://stackoverflow.com/questions/3735553/how-do-i-read-an-image-file-using-python
# [34] https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
# [35] https://www.youbbs.org/t/596
# [36] https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27#installing_a_library
# [37] https://2.python-requests.org//en/master/user/install/#install 
# [38] https://stackoverflow.com/questions/4754152/how-do-i-remove-git-tracking-from-a-project 
# [39] https://pypi.org/project/requests-toolbelt/#files 