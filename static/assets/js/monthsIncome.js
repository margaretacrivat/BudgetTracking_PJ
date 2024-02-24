const showMonthsIncomeChart = (data) => {
    let labels = [];
    const monthsdata = [];
    let keys = null;

    for (let i = 0; i < data.cumulative_income_data.length; i++) {
        const element = data.cumulative_income_data[i];
        labels.push(Object.keys(element)[0]);
        const vals = Object.values(element)[0];
        keys = Object.keys(vals);
        monthsdata.push(Object.values(vals));
    }

    const getMonthRep = (dateObj) => {
        const strDate = new Date(dateObj).toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
        return strDate.split(' ').join('');
    }

    var monthCumulative = document.getElementById("monthsIncomeChart");
    var datasets = [];

    for (let i = 0; i < labels.length; i++) {
        const dataset = {
            label: getMonthRep(labels[i]),
            data: monthsdata[i],
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
    });
};

const getCumulativeIncome = () => {
    fetch('/personalbudget/income-stats')
        .then(res => res.json()).then(data => {
            console.log('data', data)
            showMonthsIncomeChart(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

window.addEventListener('load', getCumulativeIncome);