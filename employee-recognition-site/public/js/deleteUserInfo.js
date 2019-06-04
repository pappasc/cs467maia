function deleteUserInfo(){
    var userInfo = {};

    userInfo.userId = getRadioValue();

    if (userInfo.userId > -1) {
	$.ajax({
            url: '/newaccount',
            type: 'DELETE',
            data: userInfo,
            success: redirectHandler
	});
    }
    else {
	var errorHandle = document.getElementById("errorHolder");
	while (errorHandle.firstChild) {
	    errorHandle.removeChild(errorHandle.firstChild);
	}
	var errorHolder = "Select a user to remove first";
	var errorString = document.createTextNode(errorHolder);
	errorHandle.appendChild(errorString);
    }
};

function getRadioValue()
{
    var elements = document.getElementsByName("employee");
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
    location.assign(location.origin + "/employees");
}
