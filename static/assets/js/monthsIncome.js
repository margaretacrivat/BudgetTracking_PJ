// monthsIncomeChart

const showMonthsIncomeChart = (data) => {

    let labels = []
    const monthsdata = []
    let keys = null;

    for (let i = 0; i < data.cumulative_income_data.length; i++) {
        const element = data.cumulative_income_data[i]
        labels.push(Object.keys(element)[0])
        const vals = Object.values(element)[0]
        keys = Object.keys(vals)
        monthsdata.push(Object.values(vals))
    }

    const getMonthRep = (dateObj) => {
        const strDate = new Date(dateObj).toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
        return strDate.split(' ').join('');
        // const values = [splitted[1] + " " + splitted[3]]
        // return values
    }

    var monthCumulative = document.getElementById("monthsIncomeChart");
    var datasets = [];

    for (let i = 0; i < labels.length; i++) {
        const dataset = {
            label: getMonthRep(labels[i]),
            data: monthsdata[i],
            options: {
                plugins: {
                    lineTension: 0,
                    fill: false,
                    borderColor: getRandomColor(),
                }
            }
        };
        datasets.push(dataset);
    }

    var monthsData = {
        labels: keys,
        datasets: datasets,
    };

    var chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
                // title: {
                //     display: true,
                //     text: 'Source Cumulative Comparison (Last 3 months)',
                //     font: {
                //         size: 15,
                //     }
                // },
            legend: {
                display: true,
                position: 'top',
                labels: {
                    boxWidth: 35,
                    font: {
                        size: 12,
                    },
                },
            },
        },
    };

    var lineChart = new Chart(monthCumulative, {
        type: 'line',
        data: monthsData,
        options: chartOptions
    })
};

const getCumulativeIncome = () => {
    console.log('income_source');
    fetch('/personalbudget/last_3months_income_source_stats')
        .then(res => res.json()).then(data => {
        console.log('data', data)
        showMonthsIncomeChart(data);
    });
}

window.addEventListener('load', getCumulativeIncome)

// Function to generate random colors for the datasets
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
