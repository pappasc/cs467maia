module.exports = function(){
    var     express = require('express');
    var     router  = express.Router();
    const   rp      = require('request-promise');
    
    function delUsers(req){
        var options = {
            Method: 'DELETE',
            uri: 'https://maia-backend.appspot.com/users'+ req.param.id,
            json: true,
        };

        return rp(options).then(function (users){
            return users.user_ids;
        });
    }
    
    
    //Admin page to select users or 
    router.get('/:id', function (req, res) {
		var context = {};
        delUsers(req)
        .then(function(users){
            context.jsscripts = ["logoutUser.js","gotoAccount.js","gotoAdmin.js","deleteAccount.js"];
            context.users = users;
            context.msg = "User" + req.param.id + "deleted.";
                res.status(200).render('employees',context);
            })
        .catch(function(err){
            context.msg = "User could not be deleted";
            res.status(401).send("Error 401, admins only");
        });
       
    });   
    
    return router;
}();