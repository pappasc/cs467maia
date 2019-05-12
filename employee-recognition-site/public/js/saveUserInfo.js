function saveUserInfo(){
    var userInfo = {};

    userInfo.email_address = document.getElementById("UserName").value;
    userInfo.first_name     = document.getElementById("FName").value;
    userInfo.last_name      = document.getElementById("LName").value;
    userInfo.password       = document.getElementById("pword").value;
    userInfo.created_timestamp = "2019-04-15 08:52:00";

    $.ajax({
        url: '/newaccount',
        type: 'POST',
        data: userInfo,
        success: redirectHandler
    });
};

function redirectHandler(){
    location.assign(location.origin + "/employees");
}