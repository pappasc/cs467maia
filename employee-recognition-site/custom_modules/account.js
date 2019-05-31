module.exports = function(){
    var express = require('express');
    var rp = require('request-promise');
    var router = express.Router();

    router.updateUser = function updateUser(firstName, lastName, sigPath, emailAddr, userID) {
	var userBody = {
	    first_name: firstName,
	    last_name: lastName,
	    signature_path: sigPath,
	    email_address: emailAddr
	};
	//Compose the PUT request to update the user
	var options = {
	    method: 'PUT',
	    uri: 'https://cs467maia-backend.appspot.com/users/' + userID,
	    body: userBody,
	    json: true,
	    resolveWithFullResponse: true
	};

	var contextReturn = {};
	
	return rp(options)
	    .then(function (updateReturn) {
		if (updateReturn.statusCode == 200) {
		    contextReturn.success = true;
		    return contextReturn;
		}
		else {
		    contextReturn.success = false;
		    contextReturn.errorMessage = updateReturn.response.body.errors;
		    return contextReturn;
		}
	    })
	    .catch(function (updateReturn) {
		contextReturn.success = false;
		contextReturn.errorMessage = updateReturn.response.body.errors;
		return contextReturn;
	    });
    }

    router.get('/', function (req, res) {
	var context = {};
	if (req.isAuthenticated()) {
	    if (req.user.type == 'user') {
		context.userId = req.user.user_id;
		context.email = req.user.email_address;
		context.firstName = req.user.first_name;
		context.lastName = req.user.last_name;
		context.signature = req.user.signature_path;
		context.isView = false;
		context.jsscripts = ["logoutUser.js", "gotoAwards.js", "updateUser.js", "gotoHome.js"];
		res.status(200).render('accountpage', context);
	    }
	    else if (req.user.type == 'admin'){
		res.status(403).send("Error 403, not allowed to update user from this endpoint");
	    }
	    else {
		res.status(500).render('500');
	    }
	}
	else {
	    res.status(401).send("Error 401, need to be authenticated");
	}
    });

    router.post('/', function (req, res) {
	if (req.isAuthenticated ()){
	    if (req.user.type == 'user') {
		router.updateUser(req.body.first_name, req.body.last_name, req.user.signature_path, req.user.email_address, req.user.user_id)
		    .then(function (updateReturn) {
			if (updateReturn.success) {
			    //Send a 303 status code so the browser handles the reload
			    //after the Ajax request with a GET request
			    res.redirect(303, '/account');
			}
			else {
			    var context = {};
			    //context.isView = true;
			    //context.userId = req.user.user_id;
			    //context.email = req.user.email_address;
			    //context.firstName = req.user.first_name;
			    //context.lastName = req.user.last_name;
			    //context.signature = req.user.signature_path;
			    context.errorMessage = updateReturn.errorMessage;
			    //context.jsscripts = ["logoutUser.js", "gotoAwards.js", "updateUser.js", "gotoHome.js"];
			    //console.log(context);
			    res.status(400).send(context);
			}
		    })
		    .catch(function (err) {
			res.status(500).render('500');
		    });
	    }
	    else if (req.user.type == 'admin') {
		res.status(403).send("Error 403, not allowed to update user from this endpoint");
	    }
	    else {
		res.status(500).render('500');
	    }
	}
	else {
	    res.status(401).send("Error 401, need to be authenticated");
	}
    });
    
    return router;
}();

// https://stackoverflow.com/questions/31729585/how-can-we-get-radio-button-values-from-form-using-body-parser-on-an-expressjs-s
