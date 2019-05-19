function deleteAdminInfo(){
    var adminInfo = {};

    adminInfo.adminId = getRadioValue();

    $.ajax({
        url: '/admin',
        type: 'DELETE',
        data: adminInfo,
        success: redirectHandler
    });
};

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

function redirectHandler(){
    location.assign(location.origin + "/admins");
}