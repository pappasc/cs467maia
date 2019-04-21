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
const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;

var genUser = {
    username: 'regUser',
    password: 'wordpass',
    id: '456'
};

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(session({
    genid: (req) => {
	return uuid()
    },
    secret: 'groupmaia',
    resave: false,
    saveUninitialized: true
}))

passport.use(new LocalStrategy(
    { usernameField: 'username' },
    (username, password, done) => {
	if(username === genUser.username && password === genUser.password) {
	    console.log('Local strategy returned true')
	    return done(null, genUser)
	}
    }
));

passport.serializeUser((user, done) => {
  console.log('Inside serializeUser callback')
  done(null, user.id);
});

passport.deserializeUser((id, done) => {
    console.log('Inside deserializer');
    console.log(id);
    var user;
    if (id == genUser.id) {
	user = genUser;
    }
    else {
	user = false;
    }
    done(null, user);
});

app.use(passport.initialize());
app.use(passport.session());

//Using handlebars for rendering pages
const handlebars = require('express-handlebars').create({defaultLayout:'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');

app.get('/', function (req, res) {
    //Redirect straight to home
    res.redirect('/home');
});

app.get('/home', function (req, res) {
    //Display a homepage with a link to start the process
    var context = {};
    context.login = "";
    if (req.query.login == "success") {
	context.login = "Login succeeded";
    }
    else if (req.query.login == "failure") {
	context.login = "Login failed";
    }
    else {
	context.login = req.user;
	console.log(req.user);
    }
    res.render('homepage', context);
});

app.post('/login', function(req, res, next) {
    console.log('Inside POST /login callback');
    passport.authenticate('local', (err, user, info) => {
	console.log('Inside passport.authenticate() callback');
	console.log(`req.session.passport: ${JSON.stringify(req.session.passport)}`);
	console.log(`req.user: ${JSON.stringify(req.user)}`);
	req.login(user, (err) => {
	    console.log('Inside req.login() callback');
	    console.log(`req.session.passport: ${JSON.stringify(req.session.passport)}`);
	    console.log(`req.user: ${JSON.stringify(req.user)}`);
	    return res.redirect('/home');
	})
    })(req, res, next);
});

const PORT = process.env.PORT || 8080;

app.listen(process.env.PORT || 8080, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

module.exports = app;
