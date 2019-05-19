function updateAdmin(adminId){
    var adminInfo ={};
    
    adminInfo.email_address = document.getElementById("Username").value;
    adminInfo.first_name    = document.getElementById("FName").value;
    adminInfo.last_name     = document.getElementById("LName").value;
    adminInfo.password      = document.getElementById("Password").value;
    adminInfo.adminId      = adminId;
    
    $.ajax({
        url: '/admin',
        type: 'PUT',
        data: adminInfo,
        success: redirectHandle
    });
};

function redirectHandle(){
    location.assign(location.origin + "/admins");
}