module.exports = function(){
    var express = require('express');
    var router = express.Router();
    var rp = require('request-promise');

    function saveAdmin(req){
        var options = {
            method: 'POST',
            uri: 'https://maia-backend.appspot.com/admins',
            headers = {'content-Type': 'application/json'},
            body: JSON.stringify( {
                "first_name": "Patrick",
                "last_name": "DeLeon",
                "password": "encryptme",
                "email_address": "deleonp@oregonstate.edu",
                "created_timestamp":"2018-05-06 09:10:00"
            }),
            json: true
        };

        return rp(options).then( function(admin){
            return admin.admin_id;
        });
    }    

    router.get('/', function (req, res) {
        var context = {};

        if (req.isAuthenicated()){
            saveAdmin(req)
            .then(function (admin){
                res.status(204).redirect('/employees');
            })
            .catch(function(err){
                context.isView = false;
                context.jsscripts = ["logoutUser.js"];
		        res.status(500).render('userpage', context);
            });
        }
    });

}