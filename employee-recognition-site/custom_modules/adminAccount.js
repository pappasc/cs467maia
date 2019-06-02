module.exports = function(){
    var express = require('express');
    var router = express.Router();
    var rp = require('request-promise');

    function getAdmin(id){
        var options = {
          uri: 'https://cs467maia-backend.appspot.com/admins/'+ id,
          json: true
        };

        return rp(options).then(function (admin){
            return admin;
        });
    }

    function getUsers() {
	var options = {
          uri: 'https://cs467maia-backend.appspot.com/users',
          json: true
        };

        return rp(options).then(function (users){
            return users.user_ids;
        });
    }

    function getAdmins() {
	var options = {
          uri: 'https://cs467maia-backend.appspot.com/admins',
          json: true
        };

        return rp(options).then(function (admins){
            return admins.admin_ids;
        });
    }
    
    function getAdminPwd(id){
        var options = {
            uri: 'https://cs467maia-backend.appspot.com/admins/' + id + '/login',
            json: true,
            resolveWithFullResponse: true
        };
        
        return rp(options).then(function(passObj){
            if (passObj.statusCode == 200){
                return passObj.body.password;
            }else{
                return null;
            }
        });
    }

    function createAdmin(firstName, lastName, emailAddr, password) {

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
				var adminBody = {
				    first_name: firstName,
				    last_name: lastName,
				    created_timestamp: timestamp,
				    email_address: emailAddr,
				    password: password
				};
				
				var options = {
				    method: "POST",
				    uri: "https://cs467maia-backend.appspot.com/admins",
				    body: adminBody,
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

    function updateAdmin(firstName, lastName, emailAddr, adminID) {

	return getUsers()
	    .then(users => {
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
				if (emailAddr == admins[i].email_address && adminID != admins[i].admin_id) emailUsed = true;
			    }

			    if (!emailUsed) {
				var adminBody = {
				    first_name: firstName,
				    last_name: lastName,
				    email_address: emailAddr
				};
				
				var options = {
				    method: "PUT",
				    uri: "https://cs467maia-backend.appspot.com/admins/" + adminID,
				    body: adminBody,
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

    function updateAdminPass(adminPass, adminID) {

	return getAdminPwd(adminID)
	    .then(adminPassword => {

		if (adminPass.length < 6 || adminPass.length > 10) {
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
		
		var adminPassUpdate = {
		    password: adminPass
		};
		
		var options = {
		    method: "PUT",
		    uri: "https://cs467maia-backend.appspot.com/admins/" + adminID + "/login",
		    body: adminPassUpdate,
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

    router.get('/', function (req, res) {
        var context = {};
        if (req.isAuthenticated()) {
	    if (req.user.type == 'admin') {
		context.update = false;
		context.jsscripts = ["gotoAdmins.js","saveAdminInfo.js"];
		res.status(200).render('adminpage', context);
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

    router.get('/:id', function(req,res){
        var context = {};
        if (req.isAuthenticated()){
	    if (req.user.type == 'user') {
		res.status(403).send("Error 403 - Not authorized to view this page");
	    }
	    else if (req.user.type == 'admin') {
		getAdmin(req.params.id).
		    then(function (admins){
			context.jsscripts = ["gotoAdmins.js", "updateAdminInfo.js"];
			context.adminId = admins.admin_id;
			context.email = admins.email_address;
			context.firstName = admins.first_name;
			context.lastName = admins.last_name;
			context.update = true;
			
			getAdminPwd(req.params.id).
			    then(function(pword){
				context.password = pword;
				res.status(200).render('adminpage',context);
			    })
			    .catch(function(err){
				res.status(500).render('500');
			    });
		    })
		    .catch(function(err){
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
		createAdmin(req.body.first_name, req.body.last_name, req.body.email_address, req.body.password)
		    .then(function (createReturn) {
			if (createReturn.success) {
			    res.status(303).redirect('/admins');
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
		updateAdmin(req.body.first_name, req.body.last_name, req.body.email_address, req.body.admin_id)
		    .then(function (updateReturn) {
			if (updateReturn.success) {
			    //Send a 303 status code so the browser handles the reload
			    //after the Ajax request with a GET request

			    //Update password now
			    updateUserPass(req.body.password, req.body.admin_id)
				.then(function (updatePassReturn) {
				    if (updatePassReturn.success) {
					res.status(303).redirect('/admins');
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
    
    router.delete('/', function(req,res){
        if (req.isAuthenticated()){
	    if (req.user.type == 'admin'){
		var options = {
                    method: "DELETE",
                    uri: "https://cs467maia-backend.appspot.com/admins/" + req.body.adminId,
                    json: true,
                    resolveWithFullResponse: true
		};
		
		rp(options)
		    .then(function(delReturn){
			if (delReturn.statusCode == 200){
			    res.redirect(303,'/admins');   
			}
			else if(delReturn.statusCode >= 400){
			    res.status(400).send("Malformed request. Contact your administrator.");   
			}
			else {
			    res.status(500).render('500');
			}
		    })
		    .catch(function(err){
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
    
    return router;
}();
