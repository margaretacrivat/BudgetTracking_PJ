const renderExpensesCategoryChart = (data, labels) => {
    var ctx = document.getElementById('expensesCategoryChart').getContext('2d');

    // Generate an array of random colors for each category
    const backgroundColors = [];
    const borderColors = [];
    for (let i = 0; i < labels.length; i++) {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        backgroundColors.push('rgba('+r+', '+g+', '+b+', 0.2)');
        borderColors.push('rgba('+r+', '+g+', '+b+', 1)'); // Use the same color but fully opaque for border
}

    var expensesCategoryChart = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [{
                label: 'Expenses Categories',
                data: data,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1,
            }],
        },

        options: {
            responsive: true,
            // plugins: {
            //     // legend: {
            //     //     position: 'right',
            //     //     align: 'start'
            //     // },
            //     title: {
            //         display: true,
            //         // text: 'Distribution Per Category (Last 3 months)',
            //         font: {
            //             size: 15,
            //         }
            //     },
            // },
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

            renderExpensesCategoryChart(data, labels);
        });
};


// document.onload = getCategoryData();

window.addEventListener('load',getCategoryData);

