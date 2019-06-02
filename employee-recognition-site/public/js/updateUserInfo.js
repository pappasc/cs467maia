function updateUserInfo(userId){
    var userInfo = {};

    userInfo.email_address  = document.getElementById("UserName").value;
    userInfo.first_name     = document.getElementById("FName").value;
    userInfo.last_name      = document.getElementById("LName").value;
    userInfo.password       = document.getElementById("Pword").value; 
    userInfo.signature_path = document.getElementById("currentSig").textContent;
    userInfo.user_id = userId;

    $.ajax({
        url: '/newaccount',
        type: 'PUT',
        data: userInfo,
        success: redirectHandler,
	error: errorHandle
    });
};

function redirectHandler(){
    location.assign(location.origin + "/employees");
}

function errorHandle (err) {
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
