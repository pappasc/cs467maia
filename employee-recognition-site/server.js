/**************************************************************************************
Author: Conner Pappas, OSUID: 931835643
Class: CS467
Description: Capstone Project
**************************************************************************************/
'use strict';

const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const rp = require('request-promise');
const path = require('path');
const uuid = require('uuid/v4')
const session = require('express-session')
const FileStore = require('session-file-store')(session);
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

//Using handlebars for rendering pages
const handlebars = require('express-handlebars').create({defaultLayout:'main'});
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');

//Create session ID generator
app.use(session({
  genid: (req) => {
    return uuid() // use UUIDs for session IDs
  },
  store: new FileStore(),
  secret: 'groupmaia',
  resave: false,
  saveUninitialized: true
}))

app.get('/', function (req, res) {
    //Display a homepage with a link to start the process
    var context = {};
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
	context.login = "Login not attempted";
    }
    res.render('homepage', context);
});

app.post('/login', function(req, res) {
    //middleware for now for authentication
    var username = req.body.username;
    var password = req.body.password;
    console.log(req.body);
    if (username == "regUser" && password == "wordpass") {
	res.redirect('/home?login=success');
    }
    else {
	res.redirect('/home?login=failure');
    }
});

const PORT = process.env.PORT || 8080;

app.listen(process.env.PORT || 8080, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

module.exports = app;
