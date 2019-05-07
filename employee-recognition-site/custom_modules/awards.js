module.exports = function(){
    var express = require('express');
    var router = express.Router();
    const rp = require('request-promise');

    function getUsersExcept(req){
        var options = {
	    uri: 'https://cs467maia.appspot.com/users',
	    json: true, // Automatically parses the JSON string in the response
	};

	return rp(options).then(function (users) {
	    var i;
	    var usersExcept = [];
	    for (i = 0; i < users.user_ids.length; i++) {
		if (users.user_ids[i].user_id != req.user.user_id) {
		    usersExcept.push(users.user_ids[i]);
		}
	    }
	    return usersExcept;
	});
    }
    
    //Get the known attacks from the database for display
    function getAwards(req){
        var options = {
	    uri: 'https://cs467maia.appspot.com/awardProxy/authorize/' + req.user.user_id,
	    json: true, // Automatically parses the JSON string in the response
	};

	return rp(options).then(function (awards) {
	    return awards.award_ids;
	});
    }

    function getAwardedUsers(awards) {
	var options = {
	    uri: 'https://cs467maia.appspot.com/users',
	    json: true, // Automatically parses the JSON string in the response
	};
	
	return rp(options).then(function (users) {
	    var i, j;
	    for (i = 0; i < awards.length; i ++) {
		for (j = 0; j < users.user_ids.length; j++) {
		    if (users.user_ids[j].user_id == awards[i].receiving_user_id) {
			awards[i].recipient_name = users.user_ids[j].first_name + ' ' + users.user_ids[j].last_name;
		    }
		}
	    }
	    return awards;
	});
    }

    //Page for awards. Calls getAwards for asynchronous functionality
    router.get('/:pageOption', function (req, res) {
	var context = {};
	if (req.isAuthenticated()) {
	    if (req.user.type == 'user') {
		context.jsscripts = ["logoutUser.js", "deleteAwards.js", "awardContextSwitch.js", "gotoAccount.js", "gotoAwards.js"];
		if (req.params.pageOption == 'manage') {
		    getAwards(req).then(function (awards) {
			return getAwardedUsers(awards);
		    }).then(function (namedAwards) {
			context.awards = namedAwards;
			context.authorizer = req.user.user_id;
			context.create = false;
			res.status(200).render('awardspage', context);
		    });
		}
		else if (req.params.pageOption == 'create') {
		    getUsersExcept(req).then(function (users) {
			context.users = users;
			context.create = true;
			res.status(200).render('awardspage', context);
		    });
		}
		else {
		    res.status(404).render('404');
		}
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

    router.post('/', function (req,res) {

    });
    
    //Route to delete an award. AJAX handles this because HTML doesn't do delete requests
    router.delete('/:id', function(req, res){
        
    });

    return router;
}();
