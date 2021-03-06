module.exports = function(){
    var express = require('express');
    var router = express.Router();

    const users = {
	user_ids: [
	    { "user_id": 1, "first_name": "Natasha", "last_name": "Kvavle", "email_address": "kvavlen@oregonstate.edu", "created_timestamp": "2019-04-15 08:52:00", "signature_path": "kvavlen_sig.jpg" },
	    { "user_id": 2, "first_name": "Conner", "last_name": "Pappas", "email_address": "pappasc@oregonstate.edu", "created_timestamp": "2019-04-15 08:52:00", "signature_path": "pappasc_sig.jpg" },
	    { "user_id": 3, "first_name": "Patrick", "last_name": "Deleon", "email_address": "deleonp@oregonstate.edu", "created_timestamp": "2019-04-15 08:52:00", "signature_path": "deleonp_sig.jpg" }
	]
    };

    const userIdPass = [{"user_id": 1, "password": "cheese"}, {"user_id": 2, "password": "doodle"}, {"user_id": 3, "password": "gurder"}];

    router.get('/', function (req,res){
	res.status(200).json(users);
    });

    router.get('/:id/login', function(req, res){
        var passwordToSend = {};
	var i;
	for (i = 0; i < userIdPass.length; i++) {
	    if (req.params.id == userIdPass[i].user_id) {
		passwordToSend.password = userIdPass[i].password;
		break;
	    }
	}
	res.status(200).json(passwordToSend);
    });

    return router;
}();
