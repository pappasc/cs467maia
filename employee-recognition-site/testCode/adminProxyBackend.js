module.exports = function(){
    var express = require('express');
    var router = express.Router();

    const admins = {
	admin_ids: [
	    { "admin_id": 4, "first_name": "Admin", "last_name": "Kvavle", "email_address": "adminkvavlen@oregonstate.edu", "created_timestamp": "2019-04-15 08:52:00", "signature_path": "kvavlen_sig.jpg" },
	    { "admin_id": 5, "first_name": "Admin", "last_name": "Pappas", "email_address": "adminpappasc@oregonstate.edu", "created_timestamp": "2019-04-15 08:52:00", "signature_path": "pappasc_sig.jpg" },
	    { "admin_id": 6, "first_name": "Admin", "last_name": "Deleon", "email_address": "admindeleonp@oregonstate.edu", "created_timestamp": "2019-04-15 08:52:00", "signature_path": "deleonp_sig.jpg" }
	]
    };

    const adminIdPass = [{"admin_id": 4, "password": "cheese"}, {"admin_id": 5, "password": "doodle"}, {"admin_id": 6, "password": "gurder"}];

    router.get('/', function (req,res){
	res.status(200).json(admins);
    });

    router.get('/:id/login', function(req, res){
        var passwordToSend = {};
	var i;
	for (i = 0; i < adminIdPass.length; i++) {
	    if (req.params.id == adminIdPass[i].admin_id) {
		passwordToSend.password = adminIdPass[i].password;
		break;
	    }
	}
	res.status(200).json(passwordToSend);
    });

    return router;
}();
