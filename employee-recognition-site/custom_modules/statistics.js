module.exports = function(){
    var express = require('express');
    var router  = express.Router();
    const rp    = require('request-promise');
    
    function getAwardsBy(){
        var optUsers = {
            uri: 'https://cs467maia-backend.appspot.com/users',
            json: true
        };
        
        return rp(optUsers).then(function (users) {
            var type = [];
            var vals = [];
            var ret  = [];
            var awardby = 0;
                            
            //users.user_ids.forEach(function(user){
            //    type.push(user.first_name + ' ' + user.last_name);
                
            var options = {
                uri: 'https://cs467maia-backend.appspot.com/awards',
                json: true
            }; 
            console.log(options);
            return rp(options).then(function(awards){
                users.user_ids.forEach(function(user){
                    
                    type.push(user.first_name + ' ' + user.last_name)

                    awardby = 0;
                    awards.award_ids.forEach(function(award){
                        if (award.authorizing_user_id == user.user_id){
                           awardby++;
                        }
                    });
                    console.log(awardby);
                    vals.push(awardby);
                });
                
                ret  = [type,vals];
                console.log(ret);

                return ret;

            })
            .catch(function (err){
                vals.push(0);  
            }); 
        });         
    }
    
    function getRecvBy(){
        var optUsers = {
            uri: 'https://cs467maia-backend.appspot.com/users',
            json: true
        };
        
        return rp(optUsers).then(function (users) {
            var type = [];
            var vals = [];
            var ret  = [];
            var awardtocnt = 0;
                            
            var optRecvby = {
                uri: 'https://cs467maia-backend.appspot.com/awards',
                json: true
            }; 

            return rp(optRecvby).then(function(awards){
                users.user_ids.forEach(function(user){
                    type.push(user.first_name + ' ' + user.last_name);
                    
                    awardtocnt = 0;
                    awards.award_ids.forEach(function(award){
                        if (award.receiving_user_id == user.user_id){
                            awardtocnt++;
                        }
                    });
                    vals.push(awardtocnt);
                });
                
                ret = [type,vals];
                console.log(ret);
                
                return ret;
            })
            .catch(function(err){
                vals.push(0);
            });
        });        
    }
    
    function getAwardsBytype(){
        var options = {
            uri: 'https://cs467maia-backend.appspot.com/awards',
            json: true
        };
        console.log(options);
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
            
            console.log("Week:" + week + " Month: " + month);
            console.log(ret);
            
            return ret;
        });        
    }
    
    router.get('/', function(req,res){
        var context = {};
        //context.jsscripts = ["showOverview.js", "showAssignBy.js", "showByReceipt.js","gotoHome.js"];
        context.jsscripts = ["gotohome.js", "statsOverview.js", "statsAssignBy.js", "statsRecvBy.js"];
        context.needQuery = true;
        res.status(200).render('statspage',context);        
    });
    
    router.post('/Overview', function(req,res){
        console.log(req.body);
        
        getAwardsBytype(req).then(function(typeStat){
            console.log('overview: ' + typeStat);
            res.send(typeStat);
        });
    });
    
    router.post('/AwardedBy', function(req,res){
        console.log(req.body);
        
        getAwardsBy(req).then(function (byStat){
            console.log('Overview1: ' + byStat);
            res.send(byStat);
        });
    });
    
    router.post('/RecvBy', function(req,res){
        getRecvBy(req).then(function (toStat){
            console.log('TO: ' + toStat);
            res.send(toStat);
        });
    });
    
   return router;
}();