import json
import os
import logging
from flask import Flask, request, Response
from latex import build_pdf, LatexBuildError
import os 

interpreter_api = Flask(__name__)

@interpreter_api.route('/image/<signature_path>', methods=['GET', 'POST', 'DELETE'])
def image(signature_path): 
	# POST /image/<signature_path>
	# Saves an image to disk with signature_path as filename
	if request.method == 'POST':  
		logging.info('interpreter_api.image(): saving image {}'.format(signature_path))
		try: 
			image = open(signature_path, 'w')
			image.write(request.data)
			return Response(json.dumps({'result': 'success'}), status=200, mimetype='application/json')
		except IOError as e: 
			logging.exception('interpeter_api.image(): {}'.format(e))
			return Response(json.dumps({'result': 'failure'}), status=400, mimetype='application/json')
	# DELETE /image/<signature_path>
	# Deletes image with signature_path as filename
	elif request.method == 'DELETE': 
		logging.info('interpeter_api.image(): deleting image {}'.format(signature_path))
		os.remove(signature_path)
		return Response(json.dumps({'result': 'success'}), status=200, mimetype='application/json')
	# GET /image/<signature_path>
	# Simply tells us if image exists
	elif request.method == 'GET': 
		logging.info('interpeter_api.image(): retrieving image {}'.format(signature_path))
		try: 
			image = open(signature_path, 'r')
			return Response(json.dumps({'result': 'success'}), status=200, mimetype='application/json')
		except IOError as e: 
			logging.exception('interpeter_api.image(): {}'.format(e))
			return Response(json.dumps({'result': 'failure'}), status=400, mimetype='application/json')

# POST /pdf
@interpreter_api.route('/pdf', methods=['POST'])
def pdf():
	try: 
		logging.info('interpreter_api.pdf(): building pdf')
		pdf = build_pdf(request.data)
		return Response(bytes(pdf), status=200, mimetype='application/pdf')
	except LatexBuildError as e: 
		logging.exception(e) 
		return Response(None, status=400, mimetype='application/pdf')

if __name__ == '__main__': 
	# Host 0.0.0.0 because we're in a container
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
# [15] https://docs.python.org/3/tutorial/inputoutput.html 														re: printing bytes to file with file lib
# [16] https://www.dummies.com/programming/python/how-to-delete-a-file-in-python/								re: deleting file in python 
# [17] https://pythonhosted.org/latex/																			re: exception to catch