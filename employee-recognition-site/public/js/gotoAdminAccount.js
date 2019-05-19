function gotoAdminAccount(){
    location.assign(location.origin + "/admin/" + getRadioValue());
}

function getRadioValue()
{
    var elements = document.getElementsByName("admin");
    for (var i = 0, l = elements.length; i < l; i++)
    {
        if (elements[i].checked)
        {
            return elements[i].value;
        }
    }
}
