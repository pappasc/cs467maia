function logoutUser() {
    document.getElementById("logoutButton").onclick = function () {
        location.assign("https://cs467maia.appspot.com/logout");
    };
}
