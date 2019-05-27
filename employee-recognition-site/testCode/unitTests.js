var awr = require('./../custom_modules/awards.js');
var acc = require('./../custom_modules/account.js');

var rp = require('request-promise');

function getUser(userID) {
    
    //Compose the PUT request to update the user
    var options = {
	method: 'GET',
	uri: 'https://cs467maia-backend.appspot.com/users/' + userID,
	json: true,
	resolveWithFullResponse: true
    };
    
    return rp(options)
	.then(function (user) {
	    return user.body;
	})
	.catch(function (err) {
	    return err;
	});
}

function printLine (heading) {
    console.log(heading);
}

function printResult(result, expected, testKind) {
    console.log(testKind);
    if (result == expected) {
	console.log("TEST PASSED\n");
    }
    else {
	console.log("TEST FAILED\n");
    }
}

var initialUser, awardID;

getUser(1)
    .then((userData) => {
	printLine("*********TESTING ACCOUNT.JS METHODS*********\n");
	initialUser = userData;
	return acc.updateUser('TestFirst', 'TestLast', 'testpath.jpg', 'testmail@unit.com', 1)
    })
    .then((updateResult) => {
	printResult(updateResult, 200, 'Checking user update status code');
	printResult('TestFirst' == initialUser.first_name, false, "Checking first name changed");
	printResult('TestLast' == initialUser.last_name, false, "Checking last name changed");
	printResult('testpath.jpg' == initialUser.signature_path, false, "Checking signature path changed");
	printResult('testmail@unit.com' == initialUser.email_address, false, "Checking email changed");
	printLine("\nChecking with invalid user id");
	return acc.updateUser('TestFirst', 'TestLast', 'testpath.jpg', 'testmail@unit.com', -1);
    })
    .then((updateResult2) => {
	printResult(updateResult2, 500, 'Checking update failed');
	printLine("\nChecking with invalid values");
	return acc.updateUser('', 'TestLast', 'testpath.jpg', 'testmail@unit.com', 1);
    })
    .then((updateResult3) => {
	printResult(updateResult3, 500, 'Checking update with no first name failed');
	return acc.updateUser('TestFirst', '', 'testpath.jpg', 'testmail@unit.com', 1);
    })
    .then((updateResult4) => {
	printResult(updateResult4, 500, 'Checking update with no last name failed');
	return acc.updateUser('TestFirst', 'TestLast', '', 'testmail@unit.com', 1);
    })
    .then((updateResult5) => {
	printResult(updateResult5, 500, 'Checking update with no sig path failed');
	return acc.updateUser('TestFirst', 'TestLast', 'testpath.jpg', '', 1);
    })
    .then((updateResult6) => {
	printResult(updateResult6, 500, 'Checking update with no email failed');
	printLine('Resetting user');
	return acc.updateUser(initialUser.first_name, initialUser.last_name, initialUser.signature_path, initialUser.email_address, 1);
    })
    .then((updateResult7) => {
	printLine("*********TESTING AWARD.JS METHODS*********");
	return awr.getUsersExcept(1);
    })
    .then((awardResults) => {
	var i;
	var userInList = false;
	for (i = 0; i < awardResults.length; i++) {
	    if (awardResults[i].user_id == 1) {
		userInList = true;
		break;
	    }
	}
	printResult(userInList, false, "Checking if user excepted from list");
	return awr.getUsersExcept(-1);
    })
    .then((awardResults2) => {
	//printResult(awardResults2, null, "Checking with invalid user id");
	return awr.createAward("week", 117, 116);
    })
    .then((awardResults3) => {
	printResult(awardResults3, true, "Checking awarding one week award");
	return awr.createAward("week", 117, 116);
    })
    .then((awardResults4) => {
	printResult(awardResults4, false, "Checking awarding another week award, should fail");
	return awr.createAward("test", 117, 1);
    })
    .then((awardResults5) => {
	printResult(awardResults5, false, "Checking awarding false award, should fail");
	return awr.getAwards(116);
    })
    .then((awardsFromTest) => {
	printResult(awardsFromTest > 0, true, "Checking there is more than one award");
	printResult(awardsFromTest[0].authorizing_user_id, 116, "Checking award authorized by user");
	printResult(awardsFromTest[0].receiving_user_id, 117, "Checking award received by other");
	printResult(awardsFromTest[0].type, "week", "Checking award is of correct type");
	awardID = awardsFromTest[0].award_id;
	return awr.getAwardedUsers(awardsFromTest);
    })
    .then((namedAwards) => {
	printResult(namedAwards[0].recipient_name, "Mark Twain", "Checking award is named correctly");
	return awr.getAwards(-1);
    })
    .then((noAwards) => {
	printResult(noAwards, null, "Checking invalid user id returns no awards");
	return awr.getAwardedUsers(null);
    })
    .then((noUsers) => {
	printResult(noUsers, null, "Checking invalid awards returns no names");
	return awr.deleteAward(awardID);
    })
    .then((statusCode) => {
	printResult(statusCode, 200, "Checking successful delete of new award")
	return awr.deleteAward(awardID);
    })
    .then((blehStatus) => {
	printResult(blehStatus, 500, "Checking bad award id for delete returns error");
    });
