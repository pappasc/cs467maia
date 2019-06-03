function saveAdmin(){
    var adminInfo ={};
    
    adminInfo.email_address = document.getElementById("Username").value;
    adminInfo.first_name    = document.getElementById("FName").value;
    adminInfo.last_name     = document.getElementById("LName").value;
    adminInfo.password      = document.getElementById("Password").value;
    
    $.ajax({
        url: '/admin',
        type: 'POST',
        data: adminInfo,
        success: redirectHandle,
	error: errorHandle
    });
};

function redirectHandle(){
    location.assign(location.origin + "/admins");
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
