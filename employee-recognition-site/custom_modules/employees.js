module.exports = function(){
    var     express = require('express');
    var     router  = express.Router();
    const   rp      = require('request-promise');
    
    function getUsers(req){
        var options = {
          uri: 'https://cs467maia-backend.appspot.com/users', //'https://cs467maia.appspot.com/users',
          json: true,
        };

        return rp(options).then(function (users){
            return users.user_ids;
        });
    }
    
    
    //Admin page to select users or 
    router.get('/', function (req, res) {
		var context = {};
        if (req.user.type == 'admin')
        {
            getUsers(req).then(function(users){
                context.jsscripts = ["logoutUser.js", "gotoNewAccount.js", "gotoUserAccount.js", "gotoAdmin.js", "deleteUserInfo.js", "gotoHome.js"];
                context.users = users;
                res.status(200).render('employees',context);
            });
        }
        else
        {
		    res.status(401).send("Error 401, admins only");
        }
    });
    
    return router;
}();
