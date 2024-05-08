const renderProjectsTypeChart = (data, labels) => {
    var ctx = document.getElementById('projectsTypeChart').getContext('2d');

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

    var projectsTypeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Projects Type',
                barPercentage: 0.5,
                barThickness: 18,
                maxBarThickness: 16,
                minBarLength: 2,
                data: data,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
              x: {
                beginAtZero: true,
                ticks: {
                        stepSize: 1, // Display x-axis values from 1 to 1
                        precision: 1
                    }
              }
            },
        },
    });
};

const getTypeData = () => {
    console.log('projects_type_stats_this_year');
    fetch('/projectbudget/projects-type-stats')
        .then((res) => res.json())
        .then((results) => {
            console.log('results', results);
            const type_data = results.project_type_data;
            const [labels, data] = [Object.keys(type_data),
                Object.values(type_data),
            ];
            renderProjectsTypeChart(data, labels);
        });
};

window.addEventListener('load', getTypeData);