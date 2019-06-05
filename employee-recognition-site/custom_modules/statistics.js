module.exports = function(){
    var express = require('express');
    var router  = express.Router();
    const rp    = require('request-promise');
    
    //Determine the number of awards by Authorizers
    function getAwardsBy(){
        var optUsers = {
            uri: 'https://cs467maia-backend.appspot.com/users',
            json: true
        };
        
        //Get All users
        return rp(optUsers).then(function (users) {
            var type = [];
            var vals = [];
            var wks  = [];
            var mos  = [];
            var ret  = [];
            var week = 0;
            var month = 0;
            var awardby = 0;
                            
            var options = {
                uri: 'https://cs467maia-backend.appspot.com/awards',
                json: true
            }; 
            //console.log(options);
            
            //Get all awards
            return rp(options).then(function(awards){
                users.user_ids.forEach(function(user){
                    type.push(user.first_name + ' ' + user.last_name)

                    awardby = 0;
                    week    = 0;
                    month   = 0;
                    //Find all awards a specific user gave
                    awards.award_ids.forEach(function(award){
                        if (award.authorizing_user_id == user.user_id){
                           awardby++;
                            if (award.type == "week"){
                                week++;
                            }
                            else{
                                month++;   
                            }
                        }
                    });
                    //Push counts
                    //console.log(awardby);
                    vals.push(awardby);
                    wks.push(week);
                    mos.push(month);
                });
                //Package arrays
                ret  = [type,vals,wks,mos];
                //console.log(ret);
                return ret;
            })
            .catch(function (err){
                vals.push(0);  
            }); 
        });         
    }
    
    //Determine the number of awards by Receiver
    function getRecvBy(){
        var optUsers = {
            uri: 'https://cs467maia-backend.appspot.com/users',
            json: true
        };
        //Get All users
        return rp(optUsers).then(function (users) {
            var type = [];
            var vals = [];
            var wks  = [];
            var mos  = [];
            var ret  = [];
            var week = 0;
            var month = 0;
            var awardtocnt = 0;
                            
            var optRecvby = {
                uri: 'https://cs467maia-backend.appspot.com/awards',
                json: true
            }; 
            
            //Get all awards
            return rp(optRecvby).then(function(awards){
                users.user_ids.forEach(function(user){
                    type.push(user.first_name + ' ' + user.last_name);
                    
                    //initialize counts
                    awardtocnt  = 0;
                    week        = 0;
                    month       = 0;
                    //Find all awards a specific user received
                    awards.award_ids.forEach(function(award){
                        if (award.receiving_user_id == user.user_id){
                            awardtocnt++;
                            if (award.type == "week"){
                                week++;
                            }
                            else{
                                month++;   
                            }
                        }
                    });
                    //Push counts
                    vals.push(awardtocnt);
                    wks.push(week);
                    mos.push(month);
                });
                //Package arrays
                ret  = [type,vals,wks,mos];
                //console.log(ret);
                
                return ret;
            })
            .catch(function(err){
                vals.push(0);
            });
        });        
    }
    
    //Retrieve all Awards and sort by type
    function getAwardsBytype(){
        var options = {
            uri: 'https://cs467maia-backend.appspot.com/awards',
            json: true
        };
        //console.log(options);
        return rp(options).then(function (awards) {
            var type = [];
            var vals = [];
            var ret  = [];
            var week = 0;
            var month = 0;
            
                
            awards.award_ids.forEach(function(award){
                if (award.type == "week"){
                    week++;   
                }
                else{
                    month++;   
                }
                    
            }); 
            
            type = ["Week","Month"];
            vals = [week,month];
            ret  = [type,vals];
            
            //console.log(ret);
            
            return ret;
        });        
    }
    
    //No Stat Types selected
    router.get('/', function(req,res){
        if (req.isAuthenticated()){
            if (req.user.type == 'admin'){
                var context = {};
                context.jsscripts = ["gotoHome.js", "statsOverview.js", "statsAssignBy.js", "statsRecvBy.js"];
                context.needQuery = true;
                res.status(200).render('statspage',context);
            }
            else if (req.user.type == 'user'){
                res.status(403).send("Error 403 - Not authorized to view this page");   
            }
            else{
                res.status(500).render('500');  
            }
        }
        else{
            res.status(401).send("Error 401, need to be authenticated");
        }
    });
    
    //General award data by Type
    router.post('/Overview', function(req,res){
        if (req.isAuthenticated()){
            if (req.user.type == 'admin'){
                getAwardsBytype(req).then(function(typeStat){
                    //console.log('overview: ' + typeStat);
                    res.send(typeStat);
                });
            }
            else if (req.user.type == 'user'){
                res.status(403).send("Error 403 - Not authorized to view this page");   
            }
            else{
                res.status(500).render('500');  
            }
        }
        else{
            res.status(401).send("Error 401, need to be authenticated");
        }
    });
    
    //Data by person giving awards
    router.post('/AwardedBy', function(req,res){
        if (req.isAuthenticated()){
            if (req.user.type == 'admin'){
                getAwardsBy(req).then(function (byStat){
                    //console.log('Overview1: ' + byStat);
                    res.send(byStat);
                });
            }
            else if (req.user.type == 'user'){
                res.status(403).send("Error 403 - Not authorized to view this page");   
            }
            else{
                res.status(500).render('500');  
            }
        }
        else{
            res.status(401).send("Error 401, need to be authenticated");
        }
    });
    
    //Data by person recieving awards
    router.post('/RecvBy', function(req,res){
        if (req.isAuthenticated()){
            if (req.user.type == 'admin'){
                getRecvBy(req).then(function (toStat){
                    //console.log('TO: ' + toStat);
                    res.send(toStat);
                });
            }
            else if (req.user.type == 'user'){
                res.status(403).send("Error 403 - Not authorized to view this page");   
            }
            else{
                res.status(500).render('500');  
            }
        }
        else{
            res.status(401).send("Error 401, need to be authenticated");
        }
    });
    
   return router;
}();