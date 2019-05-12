function gotoUserAccount(){
    location.assign(location.origin + "/account/" + getRadioValue());
}

function getRadioValue()
{
    var elements = document.getElementsByName("employee");
    for (var i = 0, l = elements.length; i < l; i++)
    {
        if (elements[i].checked)
        {
            return elements[i].value;
        }
    }
}
