const renderIncomeSourceChart = (data, labels) => {
    var ctx = document.getElementById('incomeSourceChart').getContext('2d');

    // Generate an array of random colors for each category
    const backgroundColors = [];
    const borderColors = [];
    for (let i = 0; i < labels.length; i++) {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        backgroundColors.push('rgba('+r+', '+g+', '+b+', 0.2)');
        borderColors.push('rgba('+r+', '+g+', '+b+', 1)');
}

    var incomeSourceChart = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [{
                label: 'Income Sources',
                data: data,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
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







