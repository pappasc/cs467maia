module.exports = function(){
    var express = require('express');
    var router = express.Router();

    router.get('/', function (req, res) {
	var context = {};
	if (req.isAuthenticated()) {
	    context.login = false;
	    if (req.user.type == 'user') {
            context.email = req.user.email_address;
            context.firstName = req.user.first_name;
            context.lastName = req.user.last_name;
            context.signature = req.user.signature_path;
            context.jsscripts = ["logoutUser.js", "gotoAwards.js"];
            res.status(200).render('userpage', context);
        }
	    else if (req.user.type == 'admin'){
            res.status(200).render('userpage', context);
            //res.status(403).send("Error 403, not allowed to view this page");
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
