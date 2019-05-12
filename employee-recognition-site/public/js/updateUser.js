//write function to compose put request to db through middleware to update user
function updateUser(userID){
    var updatedUserInfo = {};
    updatedUserInfo.first_name = document.getElementById("Fname").value;
    updatedUserInfo.last_name = document.getElementById("Lname").value;
    //will send PUT to middleware, middleware will make GET to server to get
    //rest of user's info for the full PUT request
    $.ajax({
        url: '/account',
        type: 'PUT',
	data: updatedUserInfo,
        success: redirectHandle
    });
};

function redirectHandle () {
    location.reload(true);
}
