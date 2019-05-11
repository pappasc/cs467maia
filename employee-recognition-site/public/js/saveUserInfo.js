function saveUserInfo(){
    var express = require('express');
    var router = express.Router();
    var rp = require('request-promise');

    function saveUser(req){
        var options = {
            method: 'POST',
            uri: 'https://maia-backend.appspot.com/users',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify( {
                "first_name": req.user.first_name,
                "last_name": "DeLeon",
                "password": "encryptme",
                "email_address": "deleonp@oregonstate.edu",
                "created_timestamp":"2018-05-06 09:10:00",
                "signature_path": "kvavlen_sig.jpg"
            }),
            json: true
        };

        return rp(options).then( function(user){
            return user.user_id;
        });
    }    

    router.get('/', function (req, res) {
        var context = {};

        if (req.isAuthenicated()){
            saveUser(req)
            .then(function (users){
                res.status(204).redirect('/employees');
            })
            .catch(function(err){
                context.isView = false;
                context.jsscripts = ["logoutUser.js"];
                context.err = err;
		        res.status(500).render('userpage', context);
            });
        }
        else
        {
            res.status(401).send("Bad request")
        }
    });

    return router;

}