function sendAward(authorizer) {
    /*
    $.post("http://localhost:8080/awards", {
	
    }, function (data, status) {
	
    });*/
}

function createNewElements (users, authorizer) {
    var dispTable = document.getElementById("displayTable");
    var headerRow = document.createElement("thead");
    var headerElems = [];
    var headerText = ["~", "Name", "Email", "Created on"];
    var typeOptions = ["week", "month"];
    var i;

    //Create the header for the new table
    for (i = 0; i < 4; i++) {
	headerElems.push(document.createElement("th"));
	headerElems[i].innerHTML = headerText[i];
    }
    for (i = 0; i < headerElems.length; i++) {
	headerRow.appendChild(headerElems[i]);
    }
    dispTable.appendChild(headerRow);

    //Fill the table with the user information
    for (i = 0; i < users.length; i++) {
	var userRow = document.createElement("tr");
	var userSelect = document.createElement("td");
	var userRadio = document.createElement("INPUT");
	userRadio.setAttribute("type", "radio");
	userRadio.value = users[i].user_id;
	userRadio.name = "employee";
	userSelect.appendChild(userRadio);
	userRow.appendChild(userSelect);
	var userName = document.createElement("td");
	userName.innerHTML = users[i].first_name + " " + users[i].last_name;
	userRow.appendChild(userName);
	var userEmail = document.createElement("td");
	userEmail.innerHTML = users[i].email_address;
	userRow.appendChild(userEmail);
	var userCreate = document.createElement("td");
	userCreate.innerHTML = users[i].created_timestamp;
	userRow.appendChild(userCreate);
	dispTable.appendChild(userRow);
    }

    var awardsContainer = document.getElementById("awardsContainer");

    var typeSelect = document.createElement("SELECT");
    for (i = 0; i < typeOptions.length; i++) {
	typeSelect.appendChild(new Option(typeOptions[i], typeOptions[i]));
    }
    awardsContainer.appendChild(typeSelect);
    
    var createButton = document.createElement('input');
    createButton.setAttribute('type', 'button');
    createButton.setAttribute('onclick', 'sendAward(' + authorizer + ')');
    createButton.value = "Create Award";
    awardsContainer.appendChild(createButton);
}

function getUsers (authorizer) {
    $.ajax({
	type: 'GET',
	//dataType: 'jsonp',
	url:'https://maia-backend.appspot.com/users',
	success: function (data, status) {
	       createNewElements(data.user_ids, authorizer);
	}
    });
}

function switchContext (authorizer) {
    var myNode = document.getElementById("displayTable");
    while (myNode.firstChild) {
	myNode.removeChild(myNode.firstChild);
    }
    getUsers(authorizer);
}
