module.exports = function(){
    var express = require('express');
    var router = express.Router();
    var rp = require('request-promise');

    function getUser(id){
        var options = {
          uri: 'https://maia-backend.appspot.com/users/'+ id,
          json: true,
        };

        return rp(options).then(function (user){
            return user;
        });
    }

    function getUserPword(user_id) {
	var options = {
	    uri: 'https://maia-backend.appspot.com/users/' + user_id + '/login',
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
			    console.log(pword);
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
	        var userBody = {
                first_name: req.body.first_name,
                last_name: req.body.last_name,
                created_timestamp: req.body.created_timestamp,
                email_address: req.body.email_address,
                password: req.body.password,
                signature_path: "turtle.jpg"
            };
	
            var options = {
                method: "POST",
                uri: "https://maia-backend.appspot.com/users",
                body: userBody,
                json: true,
                resolveWithFullResponse: true
            };
	    
            rp(options)
            .then(function (saveReturn){
                console.log("Entered");
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
	if (req.isAuthenticated()){
	    
            var userBody = {
		first_name: req.body.first_name,
		last_name: req.body.last_name,
		created_timestamp: req.body.created_timestamp,
		email_address: req.body.email_address,
		password: req.body.password,
		signature_path: "turtle.jpg"
            };
	    
            var options = {
		method: "PUT",
		uri: "https://maia-backend.appspot.com/users",
		body: userBody,
		json: true,
		resolveWithFullResponse: true
            };
	    
            rp(options)
		.then(function (saveReturn){
                    console.log("Entered");
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
        }
    });
    
    router.delete("/", function(req,res){
        if (req.isAuthenticated()){
	        var options = {
                method: "DELETE",
                uri: "https://maia-backend.appspot.com/users/" + req.body.user_id,
                body: "",
                json: true,
                resolveWithFullResponse: true
            };
	    
            rp(options)
            .then(function (saveReturn){
                console.log("Entered");
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
