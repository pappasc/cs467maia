function updateUserInfo(userId){
    var userInfo = {};

    userInfo.email_address  = document.getElementById("UserName").value;
    userInfo.first_name     = document.getElementById("FName").value;
    userInfo.last_name      = document.getElementById("LName").value;
    userInfo.password       = document.getElementById("Pword").value; 
    userInfo.user_id = userId;

    var checkSig = document.getElementById('sigFile').value;
    if (checkSig != "") {
	userInfo.signature_path = checkSig;
    }
    else {
	userInfo.signature_path = document.getElementById("currentSig").textContent;
    }

    $.ajax({
        url: '/newaccount',
        type: 'PUT',
        data: userInfo,
        success: sigHandler,
	error: errorHandle
    });
};

function sigHandler (res) {
    var checkSig = document.getElementById('sigFile').value;
    var sigURL = "https://cs467maia-backend.appspot.com/users/" + res.user_id + "/signature";

    if (checkSig != "") {
	var fileInput = document.getElementById('sigFile');
	var file = fileInput.files[0];
	var sigData = new FormData();
	sigData.set('sigFile', file);
	var sigReq = new XMLHttpRequest();
	sigReq.open("POST", sigURL, true);
	sigReq.onload = function(oEvent) {
	    if (sigReq.status == 200) {
		redirectHandler();
	    } else {
		console.log("Error " + sigReq.status + " occurred when trying to upload your file");
	    }
	};

	sigReq.send(sigData);
    }
    else {
	redirectHandler();
    }
}

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

//https://thoughtbot.com/blog/ridiculously-simple-ajax-uploads-with-formdata
//https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
