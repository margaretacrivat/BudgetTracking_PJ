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






