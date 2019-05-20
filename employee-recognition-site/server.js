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

//Using handlebars for rendering pages
const handlebars = require('express-handlebars').create({defaultLayout:'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');

//Enable requests with bodies to be in JSON format
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

//Set pathname for local file access
app.use(express.static(path.join(__dirname, '/public')));

//Enable sessions and instantiate store for cookies
app.use(session({
    genid: (req) => {
	return uuid();
    },
    store: new DatastoreStore({
	dataset: new Datastore({
	    kind: 'express-sessions',
	    projectId: 'cs467maia-site',
	    keyFilename: 'cs467maia-site-2c8a987d36ff.json'
	})
    }),
    secret: 'groupmaia',
    resave: false,
    saveUninitialized: true
}));

require('./custom_modules/authentication.js');

app.use(passport.initialize());
app.use(passport.session());

//Dummy backend for now. Will port to different module later
app.use('/users', require('./testCode/userProxyBackend.js'));
app.use('/admins', require('./testCode/adminProxyBackend.js'));
app.use('/awardProxy', require('./testCode/awardProxyBackend.js'));

app.get('/', function (req, res) {
    //Redirect straight to home
    res.redirect('/home');
});

app.post('/login', function(req, res) {
    passport.authenticate('local', (err, user, info) => {
	req.login(user, (err) => {
	    return res.redirect('/home');
	})
    })(req, res);
});

//Endpoint to initiate user logout
app.get('/logout', function(req, res, next) {
    if (req.session) {
	req.session.destroy(function(err) {
	    if(err) {
		return next(err);
	    }
	    else {
		return res.redirect('/home');
	    }
	});
    }
});

app.use('/home', require('./custom_modules/home.js'));
app.use('/awards', require('./custom_modules/awards.js'));
app.use('/account', require('./custom_modules/account.js'));
app.use('/employees', require('./custom_modules/employees.js'));
app.use('/admin', require('./custom_modules/adminAccount.js'));
app.use('/newaccount', require('./custom_modules/newaccount.js'));

//If the user tries navigating to a non-supplied page
app.use(function(req,res){
  res.status(404);
  res.render('404');
});

//Something went wrong
app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.render('500');
});

const PORT = process.env.PORT || 8080;

app.listen(process.env.PORT || 8080, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

module.exports = app;
