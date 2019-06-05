module.exports = function(){
    var express = require('express');
    var router = express.Router();
    var rp = require('request-promise');

    function getUser(id){
        var options = {
          uri: 'https://cs467maia-backend.appspot.com/users/'+ id,
          json: true
        };

        return rp(options).then(function (user){
            return user;
        });
    }

    function getUsers(){
        var options = {
	    uri: 'https://cs467maia-backend.appspot.com/users',
	    json: true, // Automatically parses the JSON string in the response
	    resolveWithFullResponse: true
	};

	return rp(options)
	    .then(function (users) {
		if (users.statusCode == 200) {
		    return users.body.user_ids;
		}
		else {
		    return null;
		}
	    })
	    .catch(function (err) {
		var retArry = [];
		return retArry;
	    });
    }

    function getAdmins(){
        var options = {
	    uri: 'https://cs467maia-backend.appspot.com/admins',
	    json: true, // Automatically parses the JSON string in the response
	    resolveWithFullResponse: true
	};

	return rp(options)
	    .then(function (admins) {
		if (admins.statusCode == 200) {
		    return admins.body.admin_ids;
		}
		else {
		    return null;
		}
	    })
	    .catch(function (err) {
		var retArry = [];
		return retArry;
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

	return getUsers()
	    .then(users => {
		
		if (password.length < 6 || password.length > 10) {
		    var errors = [];
		    var errorMessage = {};
		    errorMessage.field = "password";
		    errorMessage.message = "either too short or too long (6-10 characters required)";
		    errors.push(errorMessage);
		    
		    var contextReturn = {};
		    contextReturn.errorMessage = errors;
		    contextReturn.success = false;
		    return contextReturn;
		}
		
		var i;
		var emailUsed = false;
		for (i = 0; i < users.length; i++) {
		    if (emailAddr == users[i].email_address) emailUsed = true;
		}

		if (!emailUsed) {
		    return getAdmins()
			.then(admins => {
			    var i;
			    var emailUsed = false;
			    for (i = 0; i < admins.length; i++) {
				if (emailAddr == admins[i].email_address) emailUsed = true;
			    }

			    if (!emailUsed) {
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
					    contextReturn.userID = createReturn.body.user_id;
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
			    else {
				var errors = [];
				var errorMessage = {};
				errorMessage.field = "email";
				errorMessage.message = "used by admin";
				errors.push(errorMessage);
				
				var contextReturn = {};
				contextReturn.errorMessage = errors;
				contextReturn.success = false;
				return contextReturn;
			    }
			    
			});
		}
		else {
		    var errors = [];
		    var errorMessage = {};
		    errorMessage.field = "email";
		    errorMessage.message = "used by user";
		    errors.push(errorMessage);
		    
		    var contextReturn = {};
		    contextReturn.errorMessage = errors;
		    contextReturn.success = false;
		    return contextReturn;
		}
	    });
    }

    function updateUser(firstName, lastName, sigPath, emailAddr, userID) {

	return getUsers()
	    .then(users => {
		var i;
		var emailUsed = false;
		for (i = 0; i < users.length; i++) {
		    if (emailAddr == users[i].email_address && userID != users[i].user_id) emailUsed = true;
		}

		if (!emailUsed) {
		    return getAdmins()
			.then(admins => {
			    var i;
			    var emailUsed = false;
			    for (i = 0; i < admins.length; i++) {
				if (emailAddr == admins[i].email_address) emailUsed = true;
			    }

			    if (!emailUsed) {
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
			    else {
				var errors = [];
				var errorMessage = {};
				errorMessage.field = "email";
				errorMessage.message = "used by admin";
				errors.push(errorMessage);
				
				var contextReturn = {};
				contextReturn.errorMessage = errors;
				contextReturn.success = false;
				return contextReturn;
			    }
			    
			});
		}
		else {
		    var errors = [];
		    var errorMessage = {};
		    errorMessage.field = "email";
		    errorMessage.message = "used by user";
		    errors.push(errorMessage);
		    
		    var contextReturn = {};
		    contextReturn.errorMessage = errors;
		    contextReturn.success = false;
		    return contextReturn;
		}
	    });
    }

    function updateUserPass(userPass, userID) {

	return getUserPword(userID)
	    .then(userPassword => {

		if (userPass.length < 6 || userPass.length > 10) {
		    var errors = [];
		    var errorMessage = {};
		    errorMessage.field = "password";
		    errorMessage.message = "either too short or too long (6-10 characters required). Other fields may have updated";
		    errors.push(errorMessage);
		    
		    var contextReturn = {};
		    contextReturn.errorMessage = errors;
		    contextReturn.success = false;
		    return contextReturn;
		}
		
		var userPassUpdate = {
		    password: userPass
		};
		
		var options = {
		    method: "PUT",
		    uri: "https://cs467maia-backend.appspot.com/users/" + userID + "/login",
		    body: userPassUpdate,
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
		context.isView = false;
		context.update = false;
		context.currUser = false;
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
			context.currUser = true;
			getUserPword(req.params.id)
			    .then(function (pword){
				context.password = pword;
				context.isView = false;
				context.jsscripts = ["gotoEmployees.js", "updateUserInfo.js"];
				res.status(200).render('newuserpage', context);
			    })
			    .catch(function(err){
				res.status(500).render('500');
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
		createUser(req.body.first_name, req.body.last_name, req.body.email_address, req.body.password, req.body.signature_path)
		    .then(function (createReturn) {
			if (createReturn.success) {
			    res.status(200).send({"userID": createReturn.userID});
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
			    res.status(400).send("Malformed request. Contact your administrator.");
			}
			else {
			    res.status(500).render('500');
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
