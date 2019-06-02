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

    router.get('/', function (req, res) {
        var context = {};
        if (req.isAuthenticated()) {
            
            if (req.body.employee && req.body.employee != ''){
                getuser(req.body.employee).then(function(user){
                    context.email = user.email_address;
                });
            }
            context.isView = false;
            context.update = false;
            context.jsscripts = ["saveUserInfo.js", "gotoEmployees.js"];
            res.status(200).render('newuserpage', context);
            
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
			context.signature = "test.jpg";
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
	    
	    var d = new Date,
		timestamp = [d.getFullYear(),
			     d.getMonth()+1,
			     d.getDate()].join('-')+' '+
		[d.getHours(),
		 d.getMinutes(),
		 d.getSeconds()].join(':');

	        var userBody = {
                first_name: req.body.first_name,
                last_name: req.body.last_name,
                created_timestamp: timestamp,
                email_address: req.body.email_address,
                password: req.body.password,
                signature_path: "turtle.jpg"
            };
	
            var options = {
                method: "POST",
                uri: "https://cs467maia-backend.appspot.com/users",
                body: userBody,
                json: true,
                resolveWithFullResponse: true
            };
	    
            rp(options)
            .then(function (saveReturn){
                if (saveReturn.statusCode == 200 || saveReturn.statusCode == 204){
                res.redirect(303, '/employees');
                }
                else if (saveReturn.statusCode >= 400){
                res.status(500).send("Malformed request. Contact your administrator.");
                }
            })
            .catch(function (err) {
                console.log("Something broke");
                        res.status(500).send("API Error.");
            });
        }
        else
        {
            res.status(500).render('500');
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
	/*if (req.isAuthenticated()){
	    
            var userBody = {
		first_name: req.body.first_name,
		last_name: req.body.last_name,
		created_timestamp: req.body.created_timestamp,
		email_address: req.body.email_address,
		password: req.body.password,
		signature_path: "turtle.jpg",
		user_id: req.body.user_id
            };
	    
            var options = {
		method: "PUT",
		uri: "https://cs467maia-backend.appspot.com/users/" + req.body.user_id,
		body: userBody,
		json: true,
		resolveWithFullResponse: true
            };
	    
            rp(options)
		.then(function (saveReturn){
                    if (saveReturn.statusCode == 200) {
			res.redirect(303, '/employees');
                    }
                    else if (saveReturn.statusCode >= 400){
			res.status(500).send("Malformed request. Contact your administrator.");
                    }
		})
		.catch(function (err) {
                    console.log("Something broke");
                    res.status(500).send("API Error.");
		});
        }
        else
        {
            res.status(500).render('500');
        }*/
    });
    
    router.delete("/", function(req,res){
        if (req.isAuthenticated()){
	        var options = {
                method: "DELETE",
                uri: "https://cs467maia-backend.appspot.com/users/" + req.body.userId,
                body: "",
                json: true,
                resolveWithFullResponse: true
            };
	    
            rp(options)
            .then(function (saveReturn){
                if (saveReturn.statusCode == 200 || saveReturn.statusCode == 204){
                res.redirect(303, '/employees');
                }
                else if (saveReturn.statusCode >= 400){
                res.status(500).send("Malformed request. Contact your administrator.");
                }
            })
            .catch(function (err) {
                console.log("Something broke");
                        res.status(500).send("API Error.");
            });
        }
        else
        {
            res.status(500).render('500');
        }
    });
    return router;
}();

// https://stackoverflow.com/questions/31729585/how-can-we-get-radio-button-values-from-form-using-body-parser-on-an-expressjs-s
