//write function to compose put request to db through middleware to update user
function updateUser(userID){
    var updatedUserInfo = {};
    updatedUserInfo.first_name = document.getElementById("FName").value;
    updatedUserInfo.last_name = document.getElementById("LName").value;
    //will send PUT to middleware, middleware will make GET to server to get
    //rest of user's info for the full PUT request
    $.ajax({
        url: '/account',
        type: 'POST',
	data: updatedUserInfo,
        success: redirectHandle,
	error: errorHandle
    });
};

function redirectHandle () {
    location.reload(true);
}

function errorHandle (err) {
    console.log(err);
    
    var errorHandle = document.getElementById("errorHolder");
    while (errorHandle.firstChild) {
	errorHandle.removeChild(errorHandle.firstChild);
    }
    var errorHolder = "Following errors occured: ";
    var i;
    for (i = 0; i < err.responseJSON.errorMessage.length; i++) {
	errorHolder += err.responseJSON.errorMessage[i].field + " is " + err.responseJSON.errorMessage[i].message;
	if ((i+1) < err.responseJSON.errorMessage.length) errorHolder += " and ";
    }
    var errorString = document.createTextNode(errorHolder);
    errorHandle.appendChild(errorString);
}
