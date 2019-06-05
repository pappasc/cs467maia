function gotoAdminAccount(){
    var chosenAdmin = getRadioValue();
    if (chosenAdmin > -1) {
	location.assign(location.origin + "/admin/" + chosenAdmin);
    }
    else {
	var errorHandle = document.getElementById("errorHolder");
	while (errorHandle.firstChild) {
	    errorHandle.removeChild(errorHandle.firstChild);
	}
	var errorHolder = "Select an admin to update first";
	var errorString = document.createTextNode(errorHolder);
	errorHandle.appendChild(errorString);
    }
}

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
