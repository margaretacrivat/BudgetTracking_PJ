const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
tableOutput.style.display = 'none';
const tbody = document.querySelector(".table-body")

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value.trim().toLowerCase();
    const rows = document.querySelectorAll('tbody tr');

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        let found = false;

        cells.forEach(cell => {
            if (cell.textContent.trim().toLowerCase().includes(searchValue)) {
                found = true;
            }
        });

        if (found) {
            row.style.display = 'table-row';
        } else {
            row.style.display = 'none';
        }
    });
});

// const searchField = document.querySelector("#searchField");
// const tableOutput = document.querySelector(".table-output");
// const allTableRows = document.querySelectorAll('tbody tr'); // Select all table rows
// tableOutput.style.display = 'none';
//
// // Function to perform search
// function performSearch() {
//     const searchTerm = searchField.value.trim().toLowerCase(); // Get search term
//
//     allTableRows.forEach(row => {
//         const fields = row.querySelectorAll('td, th'); // Get all cells in the row
//         let found = false;
//
//         fields.forEach(field => {
//             if (field.textContent.trim().toLowerCase().includes(searchTerm)) {
//                 found = true;
//             }
//         });
//
//         if (found) {
//             row.style.display = ''; // Show the row if found
//         } else {
//             row.style.display = 'none'; // Hide the row if not found
//         }
//     });
// }
//
// // Event listener for keyup event on search field
// searchField.addEventListener('keyup', performSearch);



