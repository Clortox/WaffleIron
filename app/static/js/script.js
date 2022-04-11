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
	document.getElementById("file-upload-submit").submit()
}


function dropdown() {
	document.getElementById("course-list").classList.toggle("show");
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
		field.disabled = false;
	}
	else {
		field.classList.add('hide');
		field.disabled = true;
	}
}


function wordCounter(self) {
	var spaces = self.value.match(/\S+/g);
	var words = spaces ? spaces.length : 0;

	self.nextElementSibling.innerHTML = "Words: " + words
}