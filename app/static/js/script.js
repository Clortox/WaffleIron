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
		}
}

function displayField(self, fieldName) {
	var field = document.getElementById(fieldName + "-info");
	if(self.checked) {
		field.classList.remove('hide');
	}
	else {
		field.classList.add('hide');
	}
}


function wordCounter(self) {
	var spaces = self.value.match(/\S+/g);
	var words = spaces ? spaces.length : 0;

	self.nextElementSibling.innerHTML = "Words: " + words
}