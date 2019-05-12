module.exports = function(){
    var express = require('express');
    var router = express.Router();

    function getuser(id){
        var options = {
          uri: 'https://maia-backend.appspot.com/users/'+ id,
          json: true,
        };

        return rp(options).then(function (users){
            return users.user_ids;
        });
    }

    function saveInfo(){
        var userInfo = {
            first_name: req.body.first_name,
            last_name:  req.body.last_name,
            email_address: req.body.email_address,
            signature_path: req.body.signature_path,
            password: req.body.password,
            created_timestamp: req.body.created_timestamp
        };

        var options = {
            method: 'POST',
            uri: 'https://maia-backend.appspot.com/users',
            body: userInfo,
            json: true,
            resolveWithFullResponse: true
        };

        return rp(options).then(function(saveReturn){
            if (saveReturn.statusCode == 200 || saveReturn.statusCode == 204){
                res.redirect(saveReturn.statusCode,'/employees');
            }
            else if (saveReturn.statusCode == 400){
                res.status(400).send("Malformed request. Contact administrator.")
            }
            else{
                res.status(500).send("API Error");
            }
        })
        .catch(function(err){
            res.status(500).render('500');
        });        
    }
    
    router.post('/', function(req,res){
       res.status(404).render('404');
       /*if (req.isAuthenticated()){
            var userBody = {
                first_name: req.body.first_name,
                last_name: req.body.last_name,
                created_timestamp: req.body.created_timestamp,
                email_address: req.body.email_address,
                password: req.body.password
            }

            var options = {
                method: "POST",
                uri: "https://maia-backend.appspot.com/users",
                body: userBody,
                json: true,
                resolveWithFullResponse: true
            };

            rp(option).then(function (saveReturn){
                if (saveReturn.statusCode == 200 || saveReturn.statusCode == 204){
                    res.redirect('/employees');
                }
                else if (saveReturn.statusCode >= 400){
                    res.status(500).send("Malformed request. Contact your administrator.");
                }
            })
            .catch(function (err) {
                res.status(500).send("API Error.");
            });
            
        }
        else
        {
            res.status(500).render('500');
        }
        */
    });
    
    return router;
}();

// https://stackoverflow.com/questions/31729585/how-can-we-get-radio-button-values-from-form-using-body-parser-on-an-expressjs-s