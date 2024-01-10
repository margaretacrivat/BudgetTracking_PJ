const renderexpensesCategoryChart = (data, labels) => {
    var ctx = document.getElementById('expensesCategoryChart').getContext('2d');
    var expensesCategoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Expense Categories',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                ],
                borderWidth: 1,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribution Per Category (Last 3 months)',
                    font: {
                        size: 15,
                    }
                },
            },
        },
    });
};

const getCategoryData = () => {
    console.log('expenses_per_category_last3months');
    fetch('/personalbudget/expenses-category-chart')
        .then((res) => res.json())
        .then((results) => {
            console.log('results', results);
            const category_data = results.expense_category_data;
            const [labels, data] = [Object.keys(category_data),
                Object.values(category_data),
            ];

            renderexpensesCategoryChart(data, labels);
        });
};


// document.onload = getCategoryData();

window.addEventListener('load',getCategoryData);




