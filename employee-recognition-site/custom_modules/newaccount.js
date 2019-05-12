module.exports = function(){
    var express = require('express');
    var router = express.Router();
    var rp = require('request-promise');

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
            signature_path: "test.jpg",
            password: req.body.password,
            created_timestamp: req.body.created_timestamp       
        };

        var options = {
            header: "Content-Type: application/json",
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
            
            if (req.body.employee && req.body.employee != ''){
                getuser(req.body.employee).then(function(user){
                    context.email = user.email_address;
                });
            }
            context.isView = false;
            context.jsscripts = ["saveUserInfo.js", "gotoEmployees.js"];
            res.status(200).render('newuserpage', context);
            
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
    
    return router;
}();

// https://stackoverflow.com/questions/31729585/how-can-we-get-radio-button-values-from-form-using-body-parser-on-an-expressjs-s
