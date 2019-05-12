require('./../custom_modules/home.js');
require('./../custom_modules/awards.js');
require('./../custom_modules/account.js');
require('./../custom_modules/employees.js');
require('./../custom_modules/adminAccount.js');
require('./../custom_modules/newaccount.js');

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

function printResult(result, expected) {
    if (result == expected) {
	console.log();
    }
}

//Tests for account.js methods
printLine("*********TESTING ACCOUNT.JS METHODS*********");

printResult(checkResult(getUserPword(1), 'encryptme'), true);

//Tests for awards.js methods
printLine("*********TESTING AWARD.JS METHODS*********");

//Tests for employees.js methods
printLine("*********TESTING EMPLOYEE.JS METHODS*********");

//Tests for adminAccount.js methods
printLine("*********TESTING ADMINACCOUNT.JS METHODS*********");

//Tests for newaccount.js methods
printLine("*********TESTING NEWACCOUNT.JS METHODS*********");
