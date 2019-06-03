function gotoUserAccount(){
    var chosenUser = getRadioValue();
    if (chosenUser > -1) {
	location.assign(location.origin + "/newaccount/" + chosenUser);
    }
    else {
	var errorHandle = document.getElementById("errorHolder");
	while (errorHandle.firstChild) {
	    errorHandle.removeChild(errorHandle.firstChild);
	}
	var errorHolder = "Select a user to update first";
	var errorString = document.createTextNode(errorHolder);
	errorHandle.appendChild(errorString);
    }
}

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
