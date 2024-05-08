const renderProjectsBudgetChart = (data, labels) => {
    var ctx = document.getElementById('projectsBudgetChart').getContext('2d');

    // Generate an array of random colors for each category
    const backgroundColors = [];
    const borderColors = [];
    for (let i = 0; i < labels.length; i++) {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        backgroundColors.push('rgba(' + r + ', ' + g + ', ' + b + ', 0.2)');
        borderColors.push('rgba(' + r + ', ' + g + ', ' + b + ', 1)'); // Use the same color but fully opaque for border
    }

    var projectsBudgetChart = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [{
                label: 'Projects / Budget',
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

const getBudgetData = () => {
    console.log('projects_budget_stats_this_year');
    fetch('/projectbudget/projects-budget-stats')
        .then((res) => res.json())
        .then((results) => {
            console.log('results', results);
            const budget_data = results.project_budget_data;
            const [labels, data] = [Object.keys(budget_data),
                Object.values(budget_data),
            ];
            renderProjectsBudgetChart(data, labels);
        });
};

window.addEventListener('load', getBudgetData);


