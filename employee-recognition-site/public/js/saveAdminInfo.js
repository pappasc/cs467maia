function saveAdmin(){
    var adminInfo ={};
    
    adminInfo.email_address = document.getElementById("Username").value;
    adminInfo.first_name    = document.getElementById("FName").value;
    adminInfo.last_name     = document.getElementById("LName").value;
    adminInfo.password      = document.getElementById("Password").value;
    
    $.ajax({
        url: '/admin',
        type: 'POST',
        data: adminInfo,
        success: redirectHandle
    });
};

function redirectHandle(){
    location.assign(location.origin + "/admins");
}