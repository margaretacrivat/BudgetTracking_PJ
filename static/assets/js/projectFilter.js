document.getElementById('projectSelect').addEventListener('change', function () {
    // Obtain the value of the selected projects
    var selectedProjectName = this.value;

    // Select all rows from the table
    var rows = document.querySelectorAll('#projectTable > tbody > tr');

    // Verify if the option "Select Project" has been selected
    if (selectedProjectName === "") {
        // If it is selected, display all rows from the table
        rows.forEach(function (row) {
            row.style.display = ''; // Display row
        });
    } else {
        // Otherwise, iterate through all rows and display only those which coresponds to the selected projects name
        rows.forEach(function (row) {
            var projectNameCell = row.querySelector('td:nth-child(2)'); // Cell which contain the name of the projects
            if (projectNameCell.textContent === selectedProjectName || selectedProjectName === "All Projects") {
                row.style.display = ''; //Display the row if the name of the projects coresponds
            } else {
                row.style.display = 'none'; // Hide the row if the name of the projects coresponds
            }
        });
    }
});

document.getElementById('projectTypeSelect').addEventListener('change', function () {
    // Obțineți valoarea proiectului selectat
    var selectedProjectType = this.value;
    var rows = document.querySelectorAll('#projectTable > tbody > tr');

    if (selectedProjectType === "") {
        rows.forEach(function (row) {
            row.style.display = '';
        });
    } else {
        // Altfel, iterați prin toate rândurile și afișați doar cele care corespund tipului proiectului selectat
        rows.forEach(function (row) {
            var projectTypeCell = row.querySelector('td:nth-child(8)'); //
            if (projectTypeCell.textContent === selectedProjectType) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }
});


