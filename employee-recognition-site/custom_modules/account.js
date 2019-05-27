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
	
	return rp(options)
	    .then(function (updateReturn) {
		return updateReturn.statusCode;
	    })
	    .catch(function (err) {
		return 500;
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
		context.isView = true;
		context.jsscripts = ["logoutUser.js", "gotoAwards.js", "updateUser.js", "gotoHome.js"];
		res.status(200).render('userpage', context);
	    }
	    else if (req.user.type == 'admin'){
		console.log(req.body);
		getUser(req.body.user_id)
		    .then(function (userProfile) {
			context.userId = userProfile.user_id;
			context.email = userProfile.email_address;
			context.firstName = userProfile.first_name;
			context.lastName = userProfile.last_name;
			context.signature = userProfile.signature_path;
			context.isView = false;
			context.jsscripts = ["gotoEmployees.js", "saveUserInfo.js"];
			res.status(200).render('userpage', context);
		    })
		    .catch(function (err) {
			res.status(500).render('500');
		    });
	    }
	    else {
		res.status(500).render('500');
	    }
	}
	else {
	    res.status(401).send("Error 401, need to be authenticated");
	}
    });

    router.put('/', function (req, res) {
	if (req.isAuthenticated ()){
	    router.updateUser(req.body.first_name, req.body.last_name, req.user.signature_path, req.user.email_address, req.user.user_id)
		.then(function (updateReturn) {
		    if (updateReturn == 200) {
			//Send a 303 status code so the browser handles the reload
			//after the Ajax request with a GET request
			res.redirect(303, '/account');
		    }
		    else if (updateReturn == 400) {
			//Send the same error code received from the API
			res.status(400).send("Malformed request. Contact administrator");
		    }
		    else {
			res.status(500).send("API Error");
		    }
		})
		.catch(function (err) {
		    res.status(500).render('500');
		});
	}
	else {
	    res.status(401).send("Error 401, need to be authenticated");
	}
    });
    
    return router;
}();

// https://stackoverflow.com/questions/31729585/how-can-we-get-radio-button-values-from-form-using-body-parser-on-an-expressjs-s
