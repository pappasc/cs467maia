module.exports = function(){
    var express = require('express');
    var router = express.Router();

    const awards = [
	    { "award_id": 1, "authorizing_user_id": 2, "receiving_user_id": 3, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" },
	    { "award_id": 2, "authorizing_user_id": 1, "receiving_user_id": 2, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" },
	    { "award_id": 3, "authorizing_user_id": 1, "receiving_user_id": 3, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" },
	    { "award_id": 4, "authorizing_user_id": 2, "receiving_user_id": 3, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" },
	    { "award_id": 5, "authorizing_user_id": 2, "receiving_user_id": 1, "type": "month", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" },
	    { "award_id": 6, "authorizing_user_id": 3, "receiving_user_id": 1, "type": "week", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" },
	    { "award_id": 7, "authorizing_user_id": 3, "receiving_user_id": 1, "type": "month", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" },
	    { "award_id": 8, "authorizing_user_id": 2, "receiving_user_id": 1, "type": "month", distributed: "true", "awarded_datetime": "2019-04-18 12:00:00" }
    ];

    router.get('/:id', function (req,res){
	var i;
	var award = null;
	for (i = 0; i < awards.length; i++) {
	    if (awards[i].award_id == req.params.id) {
		award = awards[i];
		break;
	    }
	}
	if (award != null) {
	    res.status(200).json(award);
	}
	else {
	    res.status(400).json({ "errors": [ { "field": "award_id", "message": "award_id does not exist" } ] });
	}
    });

    router.get('/authorize/:id', function(req, res){
        var userAwards = [];
	var i;
	for (i = 0; i < awards.length; i++) {
	    if (awards[i].authorizing_user_id == req.params.id) {
		userAwards.push(awards[i]);
	    }
	}
	var sendAwards = {};
	sendAwards.award_ids = userAwards;
	res.status(200).json(sendAwards);
    });

    return router;
}();
