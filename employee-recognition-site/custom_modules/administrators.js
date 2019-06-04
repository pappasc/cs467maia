module.exports = function(){
    var     express = require('express');
    var     router  = express.Router();
    const   rp      = require('request-promise');
    
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
		return null;
	    });
    }
    
    router.get('/', function (req, res) {
	if(req.isAuthenticated()) {
	    var context = {};
            if (req.user.type == 'admin')
            {
		context.jsscripts = ["logoutUser.js", "gotoAdmin.js", "gotoAdminAccount.js", "gotoHome.js", "deleteAdminInfo.js"];
		getAdmins().then(function(admins){
                    if (admins != null) {
			if (admins.length != 0) {
			    context.someAdmins = true;
			    context.adminID = req.user.admin_id;
			    context.admins = admins;
			}
			else {
			    context.someAdmins = false;
			}
			res.status(200).render('admins', context);
		    }
		    else {
			context.someAdmins = false;
			res.status(200).render('admins', context);
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
