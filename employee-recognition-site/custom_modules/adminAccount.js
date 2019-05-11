module.exports = function(){
    var express = require('express');
    var router = express.Router();

    function getAdmin(id){
        var options = {
          uri: 'https://maia-backend.appspot.com/admins/'+ id,
          json: true,
        };

        return rp(options).then(function (admin){
            return admin.admin_ids;
        });
    }

    router.get('/', function (req, res) {
        var context = {};
        if (req.isAuthenticated()) {
            res.status(200).render('adminpage');
        }
        else {
            res.status(401).send("Error 401, need to be authenticated");
        }
    });

    router.get('/:id', function(req,res){
        var context = {};
        if (req.isAuthenticated()){
            getAdmin(req.params.id).then(function (admins){
                context.jsscripts = ["logoutUser.js", "gotoAwards.js"];
                context.admins = admins;
                res.status(200).render('adminpage', context);
            });           
        }
    });
    
    return router;
}();
