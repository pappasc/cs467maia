function deleteAdminInfo(thisAdminID){
    var adminInfo = {};

    adminInfo.adminId = getRadioValue();

    if (adminInfo.adminId > -1 && adminInfo.adminId != thisAdminID) {
	$.ajax({
            url: '/admin',
            type: 'DELETE',
            data: adminInfo,
            success: redirectHandler
	});
    }
    else if (adminInfo.adminId == thisAdminID) {
	var errorHandle = document.getElementById("errorHolder");
	while (errorHandle.firstChild) {
	    errorHandle.removeChild(errorHandle.firstChild);
	}
	var errorHolder = "You cannot delete yourself";
	var errorString = document.createTextNode(errorHolder);
	errorHandle.appendChild(errorString);
    }
    else {
	var errorHandle = document.getElementById("errorHolder");
	while (errorHandle.firstChild) {
	    errorHandle.removeChild(errorHandle.firstChild);
	}
	var errorHolder = "Select an admin to remove first";
	var errorString = document.createTextNode(errorHolder);
	errorHandle.appendChild(errorString);
    }
};

function getRadioValue()
{
    var elements = document.getElementsByName("admin");
    var retVal = -1;
    for (var i = 0, l = elements.length; i < l; i++)
    {
        if (elements[i].checked)
        {
            retVal = elements[i].value;
        }
    }
    return retVal;
}

function redirectHandler(){
    location.assign(location.origin + "/admins");
}
