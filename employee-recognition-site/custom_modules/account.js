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

    router.get('/', function (req, res) {
        var context = {};
        if (req.isAuthenticated()) {
            
            context.login = false;
            if (req.user.type == 'user') {
                context.email = req.user.email_address;
                context.firstName = req.user.first_name;
                context.lastName = req.user.last_name;
                context.signature = req.user.signature_path;
                context.isView = true;		
                context.jsscripts = ["logoutUser.js", "gotoAwards.js"];
                res.status(200).render('userpage', context);
            }
            else if (req.user.type == 'admin'){
                if (req.body.employee && req.body.employee != '')
                {
                    getuser(req.body.employee).then(function(user){
                        context.email = user.email_address;
                    });
                }
                context.isView = false;
                context.jsscripts = ["saveUserInfo.js", "gotoEmployees.js"];
                res.status(200).render('userpage', context);
            }
            else {
            res.status(500).render('500');
            }
        }
        else {
            res.status(401).send("Error 401, need to be authenticated");
        }
    });
    /*
    router.get('/:id', function(req,res){
        var context = {};
        if (req.isAuthenticated()){
            context.jsscripts = ["gotoEmployees.js", "updateUser.js"];
            
        }
        else
        {
            res.redirect(500,'/500')
        }
    });
    */
    return router;
}();

// https://stackoverflow.com/questions/31729585/how-can-we-get-radio-button-values-from-form-using-body-parser-on-an-expressjs-s