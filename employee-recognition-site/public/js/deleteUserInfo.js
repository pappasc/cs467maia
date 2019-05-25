function deleteUserInfo(){
    var userInfo = {};

    userInfo.userId = getRadioValue();

    $.ajax({
        url: '/newaccount',
        type: 'DELETE',
        data: userInfo,
        success: redirectHandler
    });
};

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

function redirectHandler(){
    location.assign(location.origin + "/employees");
}