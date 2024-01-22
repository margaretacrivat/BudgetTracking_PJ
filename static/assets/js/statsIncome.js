const renderIncomeSourceChart = (data, labels) => {
    var ctx = document.getElementById('incomeSourceChart').getContext('2d');
    var incomeSourceChart = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [{
                label: 'Income Sources',
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.4)',
                    'rgba(54, 162, 235, 0.4)',
                    'rgba(255, 206, 86, 0.4)',
                    'rgba(75, 192, 192, 0.4)',
                    'rgba(153, 102, 255, 0.4)',
                    'rgba(255, 159, 64, 0.4)',
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
                    text: 'Distribution Per Source (Last 3 months)',
                    font: {
                        size: 15,
                    }
                },
            },
        },
    });
};

const getSourceData = () => {
    console.log('income_per_source_last3months');
    fetch('/personalbudget/income-source-chart')
        .then((res) => res.json())
        .then((results) => {
            console.log('results', results);
            const source_data = results.income_source_data;
            const [labels, data] = [Object.keys(source_data),
                Object.values(source_data),
            ];

            renderIncomeSourceChart(data, labels);
        });
};


// document.onload = getCategoryData();

window.addEventListener('load',getSourceData);







