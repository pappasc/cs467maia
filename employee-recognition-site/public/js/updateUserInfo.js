function updateUserInfo(userId){
    var userInfo = {};

    userInfo.email_address  = document.getElementById("UserName").value;
    userInfo.first_name     = document.getElementById("FName").value;
    userInfo.last_name      = document.getElementById("LName").value;
    userInfo.password       = document.getElementById("Pword").value; 
    userInfo.signature_path = document.getElementById("SigPath").value;
    userInfo.created_timestamp = "2018-05-06 09:10:00";
    userInfo.user_id = userId;

    $.ajax({
        url: '/newaccount',
        type: 'PUT',
        data: userInfo,
        success: redirectHandler
    });
};

function redirectHandler(){
    location.assign(location.origin + "/employees");
}
