document.addEventListener('click', e => {
	const isDropdownButton = e.target.matches("[data-dropdown-button]");
	if(!isDropdownButton && e.target.closest('[data-dropdown]') != null) return;

	let currentDropdown
	if(isDropdownButton) {
		currentDropdown = e.target.closest('[data-dropdown]');
		currentDropdown.classList.toggle('active');
	}

	document.querySelectorAll("[data-dropdown].active").forEach(dropdown => {
		if(dropdown === currentDropdown) return;
		dropdown.classList.remove('active');
	});
});


function displayField(self, fieldName) {
	var field = document.getElementById(fieldName + "-info");
	if(self.checked)
		field.classList.remove('hide');
	else 
		field.classList.add('hide');
}


function counter(self) {
	var spaces = self.value.match(/\S+/g);
	var words = spaces ? spaces.length : 0;

	self.nextElementSibling.innerHTML = "Words: " + words
}