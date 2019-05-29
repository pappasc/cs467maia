module.exports = function(){
    var     express = require('express');
    var     router  = express.Router();
    const   rp      = require('request-promise');
    
    function getAdmins(req){
        var options = {
          uri: 'https://cs467maia-backend.appspot.com/admins', 
          json: true,
        };

        return rp(options).then(function (admins){
            return admins.admin_ids;
        });
    }
    
    
    //Admin page to select users or 
    router.get('/', function (req, res) {
		var context = {};
        if (req.user.type == 'admin')
        {
            getAdmins(req).then(function(admins){
                context.jsscripts = ["logoutUser.js", "gotoAdmin.js", "gotoAdminAccount.js", "gotoHome.js", "deleteAdminInfo.js"];
                context.admins = admins;
                res.status(200).render('admins',context);
            });
        }
        else
        {
		    res.status(401).send("Error 401, admins only");
        }
    });
    
    return router;
}();