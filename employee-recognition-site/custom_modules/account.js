module.exports = function(){
    var express = require('express');
    var rp = require('request-promise');
    var router = express.Router();

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

    
    
    function getuser(id){
        var options = {
          uri: 'https://maia-backend.appspot.com/users/'+ id,
          json: true,
        };

        return rp(options).then(function (users){
            return users.user_ids;
        });
    }

    function saveInfo(){
        var userInfo = {
            first_name: req.body.first_name,
            last_name:  req.body.last_name,
            email_address: req.body.email_address,
            signature_path: req.body.signature_path,
            password: req.body.password,
            created_timestamp: req.body.created_timestamp
        };

        var options = {
            method: 'POST',
            uri: 'https://maia-backend.appspot.com/users',
            body: userInfo,
            json: true,
            resolveWithFullResponse: true
        };

        return rp(options).then(function(saveReturn){
            if (saveReturn.statusCode == 200 || saveReturn.statusCode == 204){
                res.redirect(saveReturn.statusCode,'/employees');
            }
            else if (saveReturn.statusCode == 400){
                res.status(400).send("Malformed request. Contact administrator.")
            }
            else{
                res.status(500).send("API Error");
            }
        })
        .catch(function(err){
            res.status(500).render('500');
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
		context.jsscripts = ["logoutUser.js", "gotoAwards.js", "updateUser.js"];
		res.status(200).render('userpage', context);
	    }
	    else if (req.user.type == 'admin'){
		res.status(403).send("Error 403, not allowed to view this page");
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
       res.status(404).render('404');
       /*if (req.isAuthenticated()){
            var userBody = {
                first_name: req.body.first_name,
                last_name: req.body.last_name,
                created_timestamp: req.body.created_timestamp,
                email_address: req.body.email_address,
                password: req.body.password
            }

            var options = {
                method: "POST",
                uri: "https://maia-backend.appspot.com/users",
                body: userBody,
                json: true,
                resolveWithFullResponse: true
            };

            rp(option).then(function (saveReturn){
                if (saveReturn.statusCode == 200 || saveReturn.statusCode == 204){
                    res.redirect('/employees');
                }
                else if (saveReturn.statusCode >= 400){
                    res.status(500).send("Malformed request. Contact your administrator.");
                }
            })
            .catch(function (err) {
                res.status(500).send("API Error.");
            });
            
        }
        else
        {
            res.status(500).render('500');
        }
        */
    });

    router.put('/', function (req, res) {
	if (req.isAuthenticated ()){

	    //Right now, PUT request requires passwords in the body. We'll get the password
	    //for the user first then send the new info
	    getUserPword(req.user.user_id)
		.then(function (userPword) {
		    //Compose the body for the update request
		    if (userPword != null) {
			var userBody = {
			    first_name: req.body.first_name,
			    last_name: req.body.last_name,
			    user_id: req.user.user_id,
			    signature_path: req.user.signature_path,
			    created_timestamp: req.user.created_timestamp,
			    email_address: req.user.email_address,
			    password: userPword
			};
			return userBody;
		    }
		    else {
			//Throw an error if there's an issue getting the password
			throw 'password error';
		    }
		})
		.then(function (userBody) {
		    //Compose the PUT request to update the user
		    var options = {
			method: 'PUT',
			uri: 'https://maia-backend.appspot.com/users/' + req.user.user_id,
			body: userBody,
			json: true,
			resolveWithFullResponse: true
		    };

		    //Make the request, check the status codes to render the correct
		    //page based on the response
		    return rp(options)
			.then(function (updateReturn) {
			    if (updateReturn.statusCode == 200) {
				//Send a 303 status code so the browser handles the reload
				//after the Ajax request with a GET request
				res.redirect(303, '/account');
			    }
			    else if (updateReturn.statusCode == 400) {
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
