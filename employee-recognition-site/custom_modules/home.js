module.exports = function(){
    var express = require('express');
    var router = express.Router();

    router.get('/', function (req, res) {
	//Display a homepage with a link to start the process
	var context = {};
	if (req.isAuthenticated()) {
	    context.login = false;
	    context.jsscripts = ["logoutUser.js"];
	    if (req.user.type == 'user') {
		context.isUser = true;
		context.isAdmin = false;
		context.jsscripts.push("gotoAccount.js");
		context.jsscripts.push("gotoAwards.js");
	    }
	    else {
		context.isUser = false;
		context.isAdmin = true;
	    }
	}
	else {
	    context.login = true;
	}
	res.status(200).render('homepage', context);
    });
    
    return router;
}();
