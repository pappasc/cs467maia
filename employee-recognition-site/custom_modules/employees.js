module.exports = function(){
    var     express = require('express');
    var     router  = express.Router();
    const   rp      = require('request-promise');

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
		return null;
	    });
    }
    
    //Admin page to select users or 
    router.get('/', function (req, res) {
	if(req.isAuthenticated()) {
	    var context = {};
            if (req.user.type == 'admin')
            {
		context.jsscripts = ["logoutUser.js", "gotoNewAccount.js", "gotoUserAccount.js", "gotoAdmin.js", "deleteUserInfo.js", "gotoHome.js"];
		getUsers().then(function(users){
                    if (users != null) {
			if (users.length != 0) {
			    context.someUsers = true;
			    context.users = users;
			}
			else {
			    context.someUsers = false;
			}
			res.status(200).render('employees', context);
		    }
		    else {
			context.someUsers = false;
			res.status(200).render('employees', context);
		    }
		});
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
    
    return router;
}();
