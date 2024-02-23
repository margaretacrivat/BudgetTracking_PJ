document.addEventListener('change', function (event) {
    // Check if the changed element is the projects select element
    if (event.target && event.target.id === 'projectSelect') {
        var selectedProjectName = event.target.value;

        var tableContainers = document.querySelectorAll('.table-container');

        // Iterate through each table container
        tableContainers.forEach(function (tableContainer) {
            // Select all rows from the table inside the current container
            var rows = tableContainer.querySelectorAll('tbody tr');

            // Iterate through all rows and display only those which correspond to the selected projects name
            rows.forEach(function (row) {
                var projectNameCell = row.querySelector('td:first-child'); // Cell which contains the name of the projects
                if (selectedProjectName === "" || projectNameCell.textContent === selectedProjectName || selectedProjectName === "All Projects") {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
});