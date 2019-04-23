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
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
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

passport.use(new LocalStrategy((username, password, done) => {
    //logic for checking user credentials
    //make call to DB API to retreive user password and id
    
    var options1 = {
	uri: 'http://localhost:8080/users',
	json: true // Automatically parses the JSON string in the response
    };
    
    return rp(options1).then(function (users) {
	var i;
	var userObj = null;
	for (i = 0; i < users.user_ids.length; i++) {
	    if (username == users.user_ids[i].email_address) {
		userObj = users.user_ids[i];
		break;
	    }
	}
	if (userObj != null) {
	    var options2 = {
		uri: 'http://localhost:8080/users/' + userObj.user_id + '/login',
		json: true
	    };
	    
	    return rp(options2).then(function(passObj) {
		if (passObj.password == password) {
		    return done(null, userObj);
		}
		else {
		    return done(null, false);
		}
	    });
	}
	else {
	    return done(null, false);
	}
    });
}));

passport.serializeUser((user, done) => {
    done(null, user.user_id);
});

passport.deserializeUser((user_id, done) => {
    //logic for checking user id
    //should make a call to DB API to retreive id info

    var options = {
	uri: 'http://localhost:8080/users',
	json: true // Automatically parses the JSON string in the response
    };
    
    rp(options).then(function (users) {
	var i;
	var userObj = false;
	for (i = 0; i < users.user_ids.length; i++) {
	    if (user_id == users.user_ids[i].user_id) {
		userObj = users.user_ids[i];
		break;
	    }
	}
	done(null, userObj);
    });
});

app.use(passport.initialize());
app.use(passport.session());

//Using handlebars for rendering pages
const handlebars = require('express-handlebars').create({defaultLayout:'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');

app.use(express.static(path.join(__dirname, '/public')));

app.use('/users', require('./testCode/dummyBackend.js'));

app.get('/', function (req, res) {
    //Redirect straight to home
    res.redirect('/home');
});

app.get('/home', function (req, res) {
    //Display a homepage with a link to start the process
    var context = {};
    context.login = "";
    if (req.isAuthenticated()) {
	context.login = req.user.first_name + req.user.last_name;
    }
    else {
	context.login = "Need to be logged in";
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
