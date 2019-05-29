module.exports = function(){
    var express = require('express');
    var router = express.Router();
    const rp = require('request-promise');

    //Keep on this function, handle the null return
    router.getUsersExcept = function getUsersExcept(userID){
        var options = {
	    uri: 'https://cs467maia-backend.appspot.com/users',
	    json: true, // Automatically parses the JSON string in the response
	    resolveWithFullResponse: true
	};

	return rp(options)
	    .then(function (users) {
		if (users.statusCode == 200) {
		    var i;
		    var usersExcept = [];
		    for (i = 0; i < users.body.user_ids.length; i++) {
			if (users.body.user_ids[i].user_id != userID) {
			    usersExcept.push(users.body.user_ids[i]);
			}
		    }
		    return usersExcept;
		}
		else {
		    return null;
		}
	    })
	    .catch(function (err) {
		return null;
	    });
    }
    
    
    router.getAwards = function getAwards(userID){
        var options = {
	    uri: 'https://cs467maia-backend.appspot.com/awards/authorize/' + userID,
	    json: true, // Automatically parses the JSON string in the response
	    resolveWithFullResponse: true
	};

	return rp(options)
	    .then(function (awards) {
		if (awards.statusCode == 200) {
		    return awards.body.award_ids;
		}
		else {
		    return null;
		}
	    })
	    .catch(function (err) {
		console.log(err);
		return null;
	    });
    }

    router.getAwardedUsers = function getAwardedUsers(awards) {
	var options = {
	    uri: 'https://cs467maia-backend.appspot.com/users',
	    json: true, // Automatically parses the JSON string in the response
	    resolveWithFullResponse: true
	};
	
	return rp(options)
	    .then(function (users) {
		if (users.statusCode == 200) {
		    var i, j;
		    for (i = 0; i < awards.length; i ++) {
			for (j = 0; j < users.body.user_ids.length; j++) {
			    if (users.body.user_ids[j].user_id == awards[i].receiving_user_id) {
				awards[i].recipient_name = users.body.user_ids[j].first_name + ' ' + users.body.user_ids[j].last_name;
			    }
			}
		    }
		    return awards;
		}
		else {
		    return null;
		}
	    })
	    .catch(function (err) {
		return null;
	    });
    }

    router.createAward = function createAward (awardType, receivingUser, authorizingUser, awarddate, timepicker, meridianpicker) {
	/*var d = new Date,
		timestamp = [d.getFullYear(),
			     d.getMonth()+1,
			     d.getDate()].join('-')+' '+
		[d.getHours(),
		 d.getMinutes(),
		 d.getSeconds()].join(':');*/

	var timestamp = awarddate + " " + timepicker;
	
	var newAward = {
	    authorizing_user_id: authorizingUser,
	    receiving_user_id: receivingUser,
	    type: awardType,
	    awarded_datetime: timestamp
	};
	
	var options = {
	    method: 'POST',
	    uri: 'https://cs467maia-backend.appspot.com/awards/no-email',
	    json: true,
	    body: newAward,
	    resolveWithFullResponse: true
	}

	return rp(options)
	    .then(function (saveReturn) {
		if (saveReturn.statusCode == 200) {
		    return true;
		}
		else {
		    return false;
		}
	    })
	    .catch(function (saveReturn) {
		return false;
	    });
    }

    router.deleteAward = function deleteAward (awardID) {
	var options = {
            method: "DELETE",
            uri: "https://cs467maia-backend.appspot.com/awards/" + awardID,
            json: true,
            resolveWithFullResponse: true
	};
	
	return rp(options)
	    .then(function (deleteReturn){
		return deleteReturn.statusCode;
	    })
	    .catch(function (err) {
                return 500;
	    });
    }

    router.get('/', function (req, res) {
	res.redirect('/awards/manage');
    });

    //Page for awards. Calls getAwards for asynchronous functionality
    router.get('/:pageOption', function (req, res) {
	var context = {};
	if (req.isAuthenticated()) {
	    if (req.user.type == 'user') {
		context.jsscripts = ["logoutUser.js", "gotoAccount.js", "gotoAwards.js", "gotoHome.js"];
		if (req.params.pageOption == 'manage') {
		    router.getAwards(req.user.user_id).then(function (awards) {
			//handle null return from getAwards
			if (awards != null) {
			    return router.getAwardedUsers(awards);
			}
			else {
			    return null;
			}
		    })
			.then(function (namedAwards) {
			    if (namedAwards != null) {
				if (namedAwards.length != 0) {
				    context.someAwards = true;
				}
				else {
				    context.someAwards = false;
				}
				context.awards = namedAwards;
				context.authorizer = req.user.user_id;
				context.create = false;
				context.error = false;
				context.createError = false;
				context.jsscripts.push("deleteAwards.js");
				res.status(200).render('awardspage', context);
			    }
			    else {
				context.create = false;
				context.error = true;
				context.createError = false;
				res.status(200).render('awardspage', context);
			    }
			});
		}
		else if (req.params.pageOption == 'create') {
		    router.getUsersExcept(req.user.user_id)
			.then(function (users) {
			    if (users != null) {
				if (users.length != 0) {
				    context.someUsers = true;
				}
				else {
				    context.someUsers = false;
				}
				context.users = users;
				context.create = true;
				context.error = false;
				context.createError = false;
				res.status(200).render('awardspage', context);
			    }
			    else {
				context.create = true;
				context.error = true;
				context.createError = false;
				res.status(200).render('awardspage', context);
			    }
			}).
			catch(function (err) {
			    context.create = true;
			    context.error = true;
			    context.createError = false;
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
	if (req.isAuthenticated()) {
	    if (req.user.type == 'user') {
		router.createAward(req.body.typepicker, req.body.employee, req.user.user_id, req.body.awarddate, req.body.timepicker, req.body.meridianpicker)
		    .then(function (createReturn) {
			if (createReturn) {
			    res.redirect(303, '/awards');
			}
			else {
			    var context = {};
			    context.jsscripts = ["logoutUser.js", "gotoAccount.js", "gotoAwards.js", "deleteAwards.js"];
			    router.getUsersExcept(req.user.user_id)
				.then(function (users) {
				    if (users != null) {
					if (users.length != 0) {
					    context.someUsers = true;
					}
					else {
					    context.someUsers = false;
					}
					context.users = users;
					context.create = true;
					context.createError = true;
					context.error = false;
					res.status(200).render('awardspage', context);
				    }
				    else {
					context.create = true;
					context.error = true;
					context.createError = true;
					res.status(200).render('awardspage', context);
				    }
				})
				.catch(function (err) {
				    context.create = true;
				    context.error = true;
				    context.createError = true;
				    res.status(200).render('awardspage', context);
				});
			}
		    });
	    }
	    else if (req.user.type == 'admin'){
		res.status(403).send("Error 403, not allowed to create award");
	    }
	    else {
		res.status(500).render('500');
	    }
	}
	else {
	    res.status(401).send("Error 401, need to be authenticated");
	}
    });
    
    //Route to delete an award. AJAX handles this because HTML doesn't do delete requests
    router.delete('/:id', function(req, res){
        if (req.isAuthenticated()){
	    if (req.user.type == 'user') {
		router.deleteAward(req.params.id)
		    .then(function (deleteReturn) {
			if (deleteReturn == 200 || deleteReturn == 204){
			    res.redirect(303, '/awards');
			}
			else if (deleteReturn >= 400){
			    res.status(500).send("Malformed request. Contact your administrator.");
			}
		    })
		    .catch(function (err) {
                        res.status(500).send("API Error.");
		    });
	    }
	    else if (req.user.type == 'admin'){
		res.status(403).send("Error 403, not allowed to delete award");
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
