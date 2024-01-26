
// Current monthBalanceChart

const showMonthBalanceChart = (data) => {
    const labels = ['Income', 'Balance'];
    const values = Object.values(data.current_month_data);

    const datasets = [{
        label: labels[0],
        data: [values[0], 0], // Add a 0 for the Balance value
        backgroundColor: ['#36a2eb'], // Color for Income
    }, {
        label: labels[1],
        data: [0, values[1]], // Add a 0 for the Income value
        backgroundColor: ['#ff6384'], // Color for Balance
    }];

    const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        // title: {
        //     display: true,
        //     text: 'Current Month Balance',
        //     font: {
        //         size: 15,
        //     }
        // },
        legend: {
            display: true,
            position: 'top',
            align: 'center',
            labels: {
                boxWidth: 35,
                font: {
                    size: 12,
                },
            },
        },
    },
    scales: {
        x: {
            stacked: true, // Ensure the bars are stacked
        },
        y: {
            stacked: true, // Ensure the bars are stacked
        },
    },
    layout: {
        padding: {
            left: 10,
            right: 10,
            top: 10,
            bottom: 10,
        },
    },
    scales: {
        x: {
            stacked: true,
        },
        y: {
            stacked: true,
        },
    },
};

    const monthCumulative = document.getElementById("monthBalanceChart");

    const monthsDataConfig = {
        labels: labels,
        datasets: datasets,
    };

    new Chart(monthCumulative, {
        type: 'bar',
        data: monthsDataConfig,
        options: chartOptions,
    });
};

const getMonthBalance = () => {
    fetch('/personalbudget/current_month_balance_stats')
        .then(res => res.json())
        .then(data => {
            console.log('data', data)
            showMonthBalanceChart(data);
        });
};

window.addEventListener('load', getMonthBalance);



// Current yearBalanceChart

const showYearBalanceChart = (data) => {
    const labels = ['Income', 'Balance'];
    const values = Object.values(data.current_year_data);

    const datasets = [{
        label: labels[0],
        data: [values[0], 0], // Add a 0 for the Balance value
        backgroundColor: ['#488320'], // Color for Income
    }, {
        label: labels[1],
        data: [0, values[1]], // Add a 0 for the Income value
        backgroundColor: ['#f6c446'], // Color for Balance
    }];

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false, // Disable the aspect ratio to allow the chart to fill the container
        plugins: {
            // title: {
            //     display: true,
            //     text: 'Current Year Balance',
            //     font: {
            //         size: 15,
            //     }
            // },
            legend: {
                display: true,
                position: 'top',
                labels: {
                    boxWidth: 35,// Increase legend box width
                    font: {
                        size: 12, // Increase legend font size
                    },
                },
            },
        },
        scales: {
            x: {
                stacked: true, // Ensure the bars are stacked
            },
            y: {
                stacked: true, // Ensure the bars are stacked
            },
        },
        layout: {
            padding: {
                left: 10,
                right: 10,
                top: 10,
                bottom: 10,
            },
        },
        scales: {
            x: {
                stacked: true,
            },
            y: {
                stacked: true,
            },
        },
    };

    const yearCumulative = document.getElementById("yearBalanceChart");

    const yearDataConfig = {
        labels: labels,
        datasets: datasets,
    };

    new Chart(yearCumulative, {
        type: 'bar',
        data: yearDataConfig,
        options: chartOptions,
    });
};

const getYearBalance = () => {
    fetch('/personalbudget/current_year_balance_stats')
        .then(res => res.json())
        .then(data => {
            console.log('data', data)
            showYearBalanceChart(data);
        });
};

window.addEventListener('load', getYearBalance);

