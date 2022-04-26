function initialCheck() {
	var checkboxes = document.querySelectorAll("input.syllabus-fields"), statuses = [], ids = [];

	Array.prototype.forEach.call(checkboxes, function(elem) {
		statuses.push(elem.checked);
		ids.push(elem.id);
	});

	let field;
	for(let i = 0; i <= statuses.length; i++)
		if(statuses[i]) {
			field = document.getElementById(ids[i] + "-info");
			field.classList.remove('hide');
			field.disabled = false;
		}
}


function openUpload() {
	document.getElementById("file-upload").click();
}


function uploaded() {
	document.getElementById("file-upload-form").submit()
}


function dropdown() {
	document.getElementById("course-list").classList.toggle("show");
}


function passwordCheck() {
	pass = document.getElementById("password").value;
	passConfirm = document.getElementById("password-confirm").value;

	console.log("pass: " + pass);
	console.log("passConfirm: " + passConfirm);

	if(pass == null) {
		pass = "";
	}
	if(passConfirm == null) {
		passConfirm = "";
	}

	var len = document.getElementById("length");
	var number = document.getElementById("number");
	var match = document.getElementById("match");
	var button = document.getElementById("submit-button");

	var matched = (pass == passConfirm);
	var propLen = ((pass.length >= 12) && (pass.length <= 36));
	var hasNum = pass.match(/\d+/g);

	if(propLen) {
		len.style.color = "green";
	}
	else {
		len.style.color = "red";
	}

	if(hasNum) {
		number.style.color = "green"
	}
	else {
		number.style.color = "red"
	}

	if(matched) {
		match.style.color = "green";
	}
	else {
		match.style.color = "red";
	}

	if(matched && propLen && hasNum) {
		button.disabled = false;
	}
	else {
		button.disabled = true;
	}
}


window.onclick = function(event) {
	if(!event.target.matches('.dropdown-button')) {
		var dropdowns = document.getElementsByClassName("course-list");

		for(let i = 0; i < dropdowns.length; i++) {
			var openDropdown = dropdowns[i];

			if(openDropdown.classList.contains('show'))
				openDropdown.classList.remove('show');
		}
	}
}


function displayField(self, fieldName) {
	var field = document.getElementById(fieldName + "-info");
	if(self.checked) {
		field.classList.remove('hide');
                //field.disabled = false;
	}
	else {
		field.classList.add('hide');
		//field.disabled = true;
	}
}


function wordCounter(self) {
	var spaces = self.value.match(/\S+/g);
	var words = spaces ? spaces.length : 0;

	self.nextElementSibling.innerHTML = "Words: " + words
}
