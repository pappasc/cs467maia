module.exports = function(){
    var express = require('express');
    var router = express.Router();
    var rp = require('request-promise');

    function getUser(id){
        var options = {
          uri: 'https://cs467maia-backend.appspot.com/users/'+ id,
          json: true,
        };

        return rp(options).then(function (user){
            return user;
        });
    }

    function getUserPword(user_id) {
	var options = {
	    uri: 'https://cs467maia-backend.appspot.com/users/' + user_id + '/login',
	    json: true,
	    resolveWithFullResponse: true
	};
	
	return rp(options).then(function(passObj) {
	    if (passObj.statusCode == 200) {
		return passObj.body.password;
	    }
	    else {
		return null;
	    }
	});
    }

    function createUser(firstName, lastName, emailAddr, password, sigPath) {
	var d = new Date,
	    timestamp = [d.getFullYear(),
			 d.getMonth()+1,
			 d.getDate()].join('-')+' '+
	    [d.getHours(),
	     d.getMinutes(),
	     d.getSeconds()].join(':');
	
	var userBody = {
            first_name: firstName,
            last_name: lastName,
            created_timestamp: timestamp,
            email_address: emailAddr,
            password: password,
            signature_path: sigPath
        };
	
        var options = {
            method: "POST",
            uri: "https://cs467maia-backend.appspot.com/users",
            body: userBody,
            json: true,
            resolveWithFullResponse: true
        };

	var contextReturn = {};
	
	return rp(options)
	    .then(function (createReturn) {
		if (createReturn.statusCode == 200) {
		    contextReturn.success = true;
		    return contextReturn;
		}
		else {
		    contextReturn.success = false;
		    contextReturn.errorMessage = createReturn.response.body.errors;
		    return contextReturn;
		}
	    })
	    .catch(function (createReturn) {
		contextReturn.success = false;
		contextReturn.errorMessage = createReturn.response.body.errors;
		return contextReturn;
	    });
    }

    function updateUser(firstName, lastName, sigPath, emailAddr, userID) {

	var userBody = {
	    first_name: firstName,
	    last_name: lastName,
	    email_address: emailAddr,
	    signature_path: sigPath
        };
	
        var options = {
	    method: "PUT",
	    uri: "https://cs467maia-backend.appspot.com/users/" + userID,
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

    function updateUserPass(userPass, userID) {
	var userPass = {
	    password: userPass
        };

	var options = {
	    method: "PUT",
	    uri: "https://cs467maia-backend.appspot.com/users/" + userID + "/login",
	    body: userPass,
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

    function deleteUser (userID) {
	var options = {
            method: "DELETE",
            uri: "https://cs467maia-backend.appspot.com/users/" + userID,
            json: true,
            resolveWithFullResponse: true
	};
	
	return rp(options)
	    .then(function (deleteReturn){
		return deleteReturn.statusCode;
	    })
	    .catch(function (err) {
                return 500;
	    });
    }

    router.get('/', function (req, res) {
        var context = {};
        if (req.isAuthenticated()) {
            if (req.user.type == 'admin') {
		//Don't think this bit of code is needed. Adding an email attribute to the context in a promise
		//The page is likely already rendered before that happens
		/*if (req.body.employee && req.body.employee != ''){
                    getuser(req.body.employee).then(function(user){
			context.email = user.email_address;
                    });
		}*/
		context.isView = false;
		context.update = false;
		context.jsscripts = ["saveUserInfo.js", "gotoEmployees.js"];
		res.status(200).render('newuserpage', context);
	    }
	    else if (req.user.type == 'user') {
		res.status(403).send("Error 403 - Not authorized to view this page");
	    }
	    else {
		res.status(500).render('500');
	    }
        }
        else {
            res.status(401).send("Error 401, need to be authenticated");
        }
    });
    
    router.get('/:id', function (req, res) {
	var context = {};
	if (req.isAuthenticated()) {
	    if (req.user.type == 'user') {
		res.status(403).send("Error 403 - Not authorized to view this page");
	    }
	    else if (req.user.type == 'admin'){
		getUser(req.params.id)
		    .then(function (userProfile) {
			context.userId = userProfile.user_id;
			context.email = userProfile.email_address;
			context.firstName = userProfile.first_name;
			context.lastName = userProfile.last_name;
			context.signature = userProfile.signature_path;
			context.update = true;
			getUserPword(req.params.id).then(function (pword){
			    context.password = pword;
			    context.isView = false;
			    context.jsscripts = ["gotoEmployees.js", "updateUserInfo.js"];
			    res.status(200).render('newuserpage', context);
			});
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

    router.post('/', function(req,res){
	if (req.isAuthenticated()){
	    if (req.user.type == 'admin') {
		createUser(req.body.first_name, req.body.last_name, req.body.email_address, req.body.password, "temp.jpg")
		    .then(function (createReturn) {
			if (createReturn.success) {
			    res.status(303).redirect('/employees');
			}
			else {
			    var context = {};
			    context.errorMessage = createReturn.errorMessage;
			    res.status(400).send(context);
			}
		    })
		    .catch(function (err) {
			res.status(500).render('500');
		    });
	    }
	    else if (req.user.type == 'user') {
		res.status(403).send("Error 403, not allowed to update user from this endpoint");
	    }
	    else {
		res.status(500).render('500');
	    }
	    
        }
        else
        {
            res.status(401).send("Error 401, need to be authenticated");
        }
    });

    router.put('/', function(req,res){
	if (req.isAuthenticated ()){
	    if (req.user.type == 'admin') {
		updateUser(req.body.first_name, req.body.last_name, req.body.signature_path, req.body.email_address, req.body.user_id)
		    .then(function (updateReturn) {
			if (updateReturn.success) {
			    //Send a 303 status code so the browser handles the reload
			    //after the Ajax request with a GET request
			    //res.redirect(303, '/account');

			    //Update password now
			    updateUserPass(req.body.password, req.body.user_id)
				.then(function (updatePassReturn) {
				    if (updatePassReturn.success) {
					res.status(200).send({"user_id": req.body.user_id});
				    }
				    else {
					var context = {};
					context.errorMessage = updatePassReturn.errorMessage;
					res.status(400).send(context);
				    }
				});
			}
			else {
			    var context = {};
			    context.errorMessage = updateReturn.errorMessage;
			    res.status(400).send(context);
			}
		    })
		    .catch(function (err) {
			res.status(500).render('500');
		    });
	    }
	    else if (req.user.type == 'user') {
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
    
    router.delete("/", function(req,res){
        if (req.isAuthenticated()){
	    if (req.user.type == 'admin') {
		deleteUser(req.body.userId)
		    .then(function (deleteReturn) {
			if (deleteReturn == 200){
			    res.redirect(303, '/employees');
			}
			else if (deleteReturn >= 400){
			    res.status(500).send("Malformed request. Contact your administrator.");
			}
		    })
		    .catch(function (err) {
                        res.status(500).send("API Error.");
		    });
	    }
	    else if (req.user.type == 'user') {
		res.status(403).send("Error 403, not allowed to update user from this endpoint");
	    }
	    else {
		res.status(500).render('500');
	    }
        }
        else
        {
            res.status(401).send("Error 401, need to be authenticated");
        }
    });
    return router;
}();

// https://stackoverflow.com/questions/31729585/how-can-we-get-radio-button-values-from-form-using-body-parser-on-an-expressjs-s
