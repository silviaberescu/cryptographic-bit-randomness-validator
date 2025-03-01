document.addEventListener('DOMContentLoaded', () => {
	const dropdownToggle = document.getElementById('dropdown-toggle');
	const dropdownMenu = document.getElementById('dropdown-menu');

	dropdownToggle.addEventListener('click', () => {
		dropdownMenu.classList.toggle('active'); // Toggle visibility
	});

	// Close dropdown when clicking outside
	document.addEventListener('click', (event) => {
		if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
			dropdownMenu.classList.remove('active');
		}
	});
});

document.addEventListener('DOMContentLoaded', () => {
	const testFilter = document.getElementById('test-type');
	const dateFilter = document.getElementById('date-filter');
	const filterButton = document.querySelector('.filter-btn');
	const rows = document.querySelectorAll('.history-table tbody tr');

	function filterRows() {
		const testType = testFilter.value;
		const selectedDate = dateFilter.value;
		const encodedDate = encodeURIComponent(selectedDate);
		window.location.href = `/history/filter?testType=${testType}&date=${encodedDate}`;
	}
	filterButton.addEventListener('click', filterRows);
});


let selectedTest = '';

// Handle test card selection
document.querySelectorAll('.test-card').forEach(card => {
	card.addEventListener('click', function () {
		selectedTest = this.getAttribute('id');
		console.log('Selected Test:', selectedTest);

		document.querySelectorAll('.test-card').forEach(c => c.classList.remove('selected'));
		this.classList.add('selected');

		const hiddenField = document.createElement('input');
		hiddenField.type = 'hidden';
		hiddenField.name = 'test_type';
		hiddenField.value = selectedTest;
		document.getElementById("upload-form").appendChild(hiddenField);

		updateDynamicFields(selectedTest);
	});
});

function updateDynamicFields(testType) {
	const dynamicFields = document.getElementById('dynamic-fields');
	dynamicFields.innerHTML = '';

	if (testType === 'mbit' || testType === 'serial') {
		dynamicFields.innerHTML = `<label for="parameter-m">Parameter (m):</label>
            <input type="text" id="parameter-m" name="parameter" required>`;
	} else if (testType === 'autocorrelation') {
		dynamicFields.innerHTML = `<label for="parameter-d">Parameter (d):</label>
            <input type="text" id="parameter-d" name="parameter" required>`;
	}
}

// Prevent link click from affecting card selection
document.querySelectorAll('.test-card a').forEach(link => {
	link.addEventListener('click', e => {
		e.stopPropagation();
	});
});
