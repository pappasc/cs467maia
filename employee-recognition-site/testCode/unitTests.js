require('./../custom_modules/home.js');
require('./../custom_modules/awards.js');
require('./../custom_modules/account.js');
requite('./../custom_modules/authentication.js')

function checkResult(received, expected) {
    if (received == expected) {
	return true;
    }
    else {
	return false;
    }
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

//Tests for account.js methods
printLine("*********TESTING ACCOUNT.JS METHODS*********");

//Tests for awards.js methods
printLine("*********TESTING AWARD.JS METHODS*********");

//Tests for authentication.js methods
printLine("*********TESTING AUTHENTICATION.JS METHODS*********");
