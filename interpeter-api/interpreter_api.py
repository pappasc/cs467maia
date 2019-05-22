import json
import os
import logging
from flask import Flask, request, Response
from latex import build_pdf

interpreter_api = Flask(__name__)

@interpreter_api.route('/test', methods=['GET'])
def test(): 
	return 'hello, it is me'

@interpreter_api.route('/pdf', methods=['POST'])
def pdf():	
	try: 
		logging.info('interpreter_api.pdf(): request made was {}'.format(request.data))
		data = json.loads(request.data)

		# Print image to {signature_path}.jpg file
		logging.info('interpeter_api.pdf(): writing signature .jpg file to disk')
		bytes_jpg = data['jpg_data']
		signature_path = data['signature_path']
		image = file('{}'.format(data['signature_path']), 'wb')
		image.write(bytes_jpg)
		logging.info('interpeter_api.pdf(): success')

		# Build PDF using image
		logging.info('interpeter_api.pdf(): building PDF using image & tex data')
		pdf = build_pdf(data['tex_data'])

		# TODO: Delete image
		#image = delete('award_{}.jpg'.format(data['award_id']))
		
		# Return bytes of pdf if successful
		return Response(bytes(pdf), status=200, mimetype='application/pdf') 
	except Exception as e: 
		logging.exception(e) 
		return Response(None, status=400, mimetype='application/pdf')

if __name__ == '__main__': 
	interpreter_api.run(host='0.0.0.0', port=8080)

# [1] https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server re: pdb
# [2] https://guides.lib.wayne.edu/latex/compiling 																re: bypassing latex lib
# [3] https://stackoverflow.com/questions/2559076/how-do-i-redirect-output-to-a-variable-in-shell 				re: redirecting file to var
# [4] https://stackoverflow.com/questions/2152114/google-app-engine-to-run-executable-files 					re: can't run binary files
# [5] https://pypi.org/project/latex/
# [6] https://stackoverflow.com/questions/38431066/runtime-error-in-build-pdf-module-of-latex-python            re: host to get latex binaries
# [7] https://github.com/mbr/latex/blob/master/latex/build.py                                                   re: specifying texinputs in build_pdf()
# [8] https://tex.stackexchange.com/questions/265688/how-can-i-add-the-latex-on-python-path 					re: adding to path
# [9] https://stackoverflow.com/questions/5971312/how-to-set-environment-variables-in-python 					re: effectively adding to os var
# [10] https://pythonhow.com/how-a-flask-app-works/ re: use of main
# [11] https://codefresh.io/docker-tutorial/hello-whale-getting-started-docker-flask/ 							re: flask & docker - use of host 0.0.0.0
# [12] https://stackoverflow.com/questions/13223855/what-is-the-http-content-type-to-use-for-a-blob-of-bytes	re: mimetype for binary
# [13] https://cloud.google.com/appengine/docs/standard/python/mail/mail-with-headers-attachments				re: mimetype for pdf
# [14] https://stackoverflow.com/questions/17693231/how-save-image-to-disk										re: writing image to disk