module.exports = function(){
    var express = require('express');
    var router = express.Router();
    var rp = require('request-promise');

    function getAdmin(id){
        var options = {
          uri: 'https://maia-backend.appspot.com/admins/'+ id,
          json: true,
        };

        return rp(options).then(function (admin){
            return admin;
        });
    }
    
    function getAdminPwd(id){
        var options = {
            uri: 'https://maia-backend.appspot.com/admins/' + id + '/login',
            json: true,
            resolveWithFullResponse: true
        };
        
        return rp(options).then(function(passObj){
            if (passObj.statusCode == 200){
                return passObj.body.password;
            }else{
                return null;
            }
        });
    }

    router.get('/', function (req, res) {
        var context = {};
        if (req.isAuthenticated()) {
            context.jsscripts = ["gotoAdmins.js","saveAdminInfo.js"];
            context.update = false;
            res.status(200).render('adminpage',context);
        }
        else {
            res.status(401).send("Error 401, need to be authenticated");
        }
    });

    router.get('/:id', function(req,res){
        var context = {};
        if (req.isAuthenticated()){
            getAdmin(req.params.id).then(function (admins){
                context.jsscripts = ["gotoAdmins.js", "updateAdminInfo.js"];
                context.adminId = admins.admin_id;
                context.email = admins.email_address;
                context.firstName = admins.first_name;
                context.lastName = admins.last_name;
                context.update = true;
                
                getAdminPwd(req.params.id).then(function(pword){
                    console.log(context);
                    console.log(pword);
                    context.password = pword;
                    res.status(200).render('adminpage',context);
                });
            })
            .catch(function(err){
                    res.status(500).render('500');
            });           
        }
                   
    });
    
    router.post('/', function(req,res){
        if (req.isAuthenticated()){
            var d = new Date,
                timestamp = [d.getFullYear(),
                         d.getMonth()+1,
                         d.getDate()].join('-')+' '+
                [d.getHours(),
                 d.getMinutes(),
                 d.getSeconds()].join(':');
            
            var adminBody = {
                first_name: req.body.first_name,
                last_name: req.body.last_name,
                created_timestamp: timestamp,
                email_address: req.body.email_address,
                password: req.body.password
            };
            
            var options ={
                method: "POST",
                uri: "https://maia-backend.appspot.com/admins",
                body: adminBody,
                json: true,
                resolveWithFullResponse: true                
            };
            
            rp(options)
            .then(function(saveReturn){
                if(saveReturn.statusCode == 200 || saveReturn.statusCode == 204){
                    res.redirect(303, '/admins');
                }
                else if(saveReturn.statusCode >= 400){
                    res.status(500).send("malformed request. Contact your administrator.");
                }
            })
            .catch(function(err){
                console.log("RP failed");
                res.status(500).send("API Error");
            });
        }
        else{
            res.status(500).render('500');        
        }
    });
    
    router.put('/', function(req,res){
        if (req.isAuthenticated()){
            var d = new Date,
                timestamp = [d.getFullYear(),
                         d.getMonth()+1,
                         d.getDate()].join('-')+' '+
                [d.getHours(),
                 d.getMinutes(),
                 d.getSeconds()].join(':');
            
            var adminBody = {
                first_name: req.body.first_name,
                last_name: req.body.last_name,
                created_timestamp: timestamp,
                email_address: req.body.email_address,
                password: req.body.password
            };
            
            console.log(adminBody);
            
            var options = {
                method: "PUT",
                uri: "https://maia-backend.appspot.com/admins/" + req.body.adminId,
                body: adminBody,
                json: true,
                resolveWithFullResponse: true
            };
            console.log(options);
            rp(options)
            .then(function(updateReturn){
                if (updateReturn.statusCode == 200){
                    res.redirect(303, '/admins');   
                }
                else if(updateReturn.statusCode >=400){
                    res.status(500).send("Malformed request. Contact your administrator.");   
                }
            })
            .catch(function(err){
                console.log("Put failed");
                res.status(500).render('500');
            });
        }
        else{
            res.status(500).render('500');        
        }
    });
    
    router.delete('/', function(req,res){
        if (req.isAuthenticated()){
            var options = {
                method: "DELETE",
                uri: "https://maia-backend.appspot.com/admins/" + req.body.adminId,
                body: "",
                json: true,
                resolveWithFullResponse: true
            };
            console.log(options);
            rp(options)
            .then(function(delReturn){
                if (delReturn.statusCode == 200 || delReturn.statusCode == 204){
                    res.redirect(303,'/admins');   
                }
                else if(delReturn.statusCode >= 400){
                    res.status(500).send("Malformed request. Contact your administrator.");   
                }
            })
            .catch(function(err){
               res.status(500).render('500'); 
            });
        }
    });
    
    return router;
}();
