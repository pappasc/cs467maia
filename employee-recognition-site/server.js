/**************************************************************************************
Author: Conner Pappas, OSUID: 931835643
Class: CS467
Description: Capstone Project
**************************************************************************************/
'use strict';

const express = require('express');
const bodyParser = require('body-parser');
const rp = require('request-promise');
const path = require('path');
const uuid = require('uuid/v4')
const session = require('express-session')
const {Datastore} = require('@google-cloud/datastore');
const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const app = express();
const DatastoreStore = require('@google-cloud/connect-datastore')(session);

//Enable requests with bodies to be in JSON format
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

//Enable sessions and instantiate store for cookies
app.use(session({
    genid: (req) => {
	return uuid();
    },
    store: new DatastoreStore({
	dataset: new Datastore({
	    kind: 'express-sessions',
	    projectId: 'cs467maia',
	    keyFilename: 'cs467maia-a21a648c06b7.json'
	})
    }),
    secret: 'groupmaia',
    resave: false,
    saveUninitialized: true
}));


//making an attempt to fix callback hell


//Enable a local strategy for logging in
//Sift through users first then admins
//Adds a "type" attribute to objects to distinguish users from admins
passport.use(new LocalStrategy((username, password, done) => {
    //logic for checking user credentials
    //make call to DB API to retreive user password and id
    
    var options1 = {
	uri: 'http://localhost:8080/users',
	json: true, // Automatically parses the JSON string in the response
	resolveWithFullResponse: true
    };
    
    return rp(options1).then(function (users) {
	if (users.statusCode == 200) {
	    var i;
	    var userObj = null;
	    for (i = 0; i < users.body.user_ids.length; i++) {
		if (username == users.body.user_ids[i].email_address) {
		    userObj = users.body.user_ids[i];
		    break;
		}
	    }
	    if (userObj != null) {
		var options2 = {
		    uri: 'http://localhost:8080/users/' + userObj.user_id + '/login',
		    json: true,
		    resolveWithFullResponse: true
		};
		
		return rp(options2).then(function(passObj) {
		    if (passObj.statusCode == 200) {
			if (passObj.body.password == password) {
			    userObj.type = 'user';
			    return done(null, userObj);
			}
			else {
			    return done(null, false);
			}
		    }
		    else {
			return done(null, false);
		    }
		});
	    }
	    else {
		var options3 = {
		    uri: 'http://localhost:8080/admins',
		    json: true, // Automatically parses the JSON string in the response
		    resolveWithFullResponse: true
		};

		return rp(options3).then(function (admins) {
		    if (admins.statusCode == 200) {
			var j;
			var adminObj = null;
			for (j = 0; j < admins.body.admin_ids.length; j++) {
			    if (username == admins.body.admin_ids[j].email_address) {
				adminObj = admins.body.admin_ids[j];
				break;
			    }
			}
			if (adminObj != null) {
			    var options4 = {
				uri: 'http://localhost:8080/admins/' + adminObj.admin_id + '/login',
				json: true,
				resolveWithFullResponse: true
			    };
			    
			    return rp(options4).then(function(passObj) {
				if (passObj.statusCode == 200) {
				    if (passObj.body.password == password) {
					adminObj.type = 'admin';
					return done(null, adminObj);
				    }
				    else {
					return done(null, false);
				    }
				}
				else {
				    return done(null, false);
				}
			    });
			}
			else {
			    return done(null, false);
			}
		    }
		    else {
			return done(null, false);
		    }
		});
	    }
	}
	else {
	    return done(null, false);
	}
    });
}));

//Store necessary info about the user on the server for later retreival
passport.serializeUser((user, done) => {
    if (user != false) {
	var userIdent = {
	    type: user.type
	};
	if (user.type == 'admin') {
	    userIdent.admin_id = user.admin_id;
	}
	else {
	    userIdent.user_id = user.user_id;
	}
	done(null, userIdent);
    }
    else {
	done(null, user);
    }
});

//Use the serialized user info to retreive user from database
passport.deserializeUser((userIdent, done) => {
    //logic for checking user id
    //should make a call to DB API to retreive id info
    var uriType;
    if (userIdent.type == 'user') {
	uriType = 'users';
    }
    else if (userIdent.type == 'admin') {
	uriType = 'admins';
    }
    else {
	done(null, false);
    }
    
    var options = {
	uri: 'http://localhost:8080/' + uriType,
	json: true // Automatically parses the JSON string in the response
    };
    
    rp(options).then(function (accounts) {
	var i;
	var accountObj = null;
	if (userIdent.type == 'user') {
	    for (i = 0; i < accounts.user_ids.length; i++) {
		if (userIdent.user_id == accounts.user_ids[i].user_id) {
		    accountObj = accounts.user_ids[i];
		    accountObj.type = 'user';
		    break;
		}
	    }

	}
	else if (userIdent.type == 'admin') {
	    for (i = 0; i < accounts.admin_ids.length; i++) {
		if (userIdent.admin_id == accounts.admin_ids[i].admin_id) {
		    accountObj = accounts.admin_ids[i];
		    accountObj.type = 'admin';
		    break;
		}
	    }
	}
	else {
	    done(null, false);
	}

	if (accountObj != null) {
	    done(null, accountObj);
	}
	
	else {
	    done(null, false);
	}
    });
});

app.use(passport.initialize());
app.use(passport.session());

//Using handlebars for rendering pages
const handlebars = require('express-handlebars').create({defaultLayout:'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');

app.use(express.static(path.join(__dirname, '/public')));

//Dummy backend for now. Will port to different module later
app.use('/users', require('./testCode/userProxyBackend.js'));
app.use('/admins', require('./testCode/adminProxyBackend.js'));

app.get('/', function (req, res) {
    //Redirect straight to home
    res.redirect('/home');
});

app.get('/home', function (req, res) {
    //Display a homepage with a link to start the process
    var context = {};
    if (req.isAuthenticated()) {
	context.login = false;
	if (req.user.type == 'user') {
	    context.isUser = true;
	    context.isAdmin = false;
	    context.name = 'User ' + req.user.first_name + ' ' + req.user.last_name;
	}
	else {
	    context.isUser = false;
	    context.isAdmin = true;
	    context.name = 'Admin ' + req.user.first_name + ' ' + req.user.last_name;
	}
    }
    else {
	context.login = true;
    }
    res.render('homepage', context);
});

app.get('/test', function (req, res) {
    res.send("Test page");
});

app.post('/login', function(req, res) {
    passport.authenticate('local', (err, user, info) => {
	req.login(user, (err) => {
	    return res.redirect('/home');
	})
    })(req, res);
});

const PORT = process.env.PORT || 8080;

app.listen(process.env.PORT || 8080, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

module.exports = app;
