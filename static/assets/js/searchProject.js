const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = 'none';
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body")

searchField.addEventListener('keyup',(e)=> {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = 'none';
        tbody.innerHTML = "";
        console.log("/searchValue", searchValue);

        fetch("/projectbudget/search-project/", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                appTable.style.display = 'none';
                tableOutput.style.display = 'block';

                // console.log("data.length", data.length)

                if(data.length === 0) {
                    noResults.style.display = "block";
                    tableOutput.style.display = 'none';
                } else {
                    noResults.style.display = "none";
                    data.forEach((item) => {
                        tbody.innerHTML += `
                        <tr>
                        <td>${item.project_title}</td>
                        <td>${item.project}</td>
                        <td>${item.project_stages}</td>
                        <td>${item.project_manager}</td>
                        <td>${item.funder}</td>
                        <td>${item.contract}</td>
                        <td>${item.project_type}</td>
                        <td>${item.budget}</td>                                
                        <td>${item.start_date}</td>                                
                        <td>${item.end_date}</td>                                
                        </tr>`;
                    });
                }
            });
    } else {
        appTable.style.display = 'block';
        paginationContainer.style.display = 'block';
        tableOutput.style.display = 'none';
    }
});






