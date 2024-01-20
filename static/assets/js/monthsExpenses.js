// monthsExpensesChart

const showMonthsExpensesChart = (data) => {

    let labels = []
    const monthsdata = []
    let keys = null;

    for (let i = 0; i < data.cumulative_expense_data.length; i++) {
        const element = data.cumulative_expense_data[i]
        labels.push(Object.keys(element)[0])
        const vals = Object.values(element)[0]
        keys = Object.keys(vals)
        monthsdata.push(Object.values(vals))
    }

    const getMonthRep = (dateObj) => {
        const strDate = new Date(dateObj).toDateString()
        const splitted = strDate.split(' ')
        const values = [splitted[1] + " " + splitted[3]]
        return values
    }

    var monthCumulative = document.getElementById("monthsExpensesChart");
    var dataFirst = {
        label: getMonthRep(labels[0]),
        data: monthsdata[0],
        options: {
            plugins: {
                lineTension: 0,
                fill: false,
                borderColor: 'rgb(80,151,215)'
            }
        }
    };

    var dataSecond = {
        label: getMonthRep(labels[1]),
        data: monthsdata[1],
        options: {
            plugins: {
                lineTension: 0,
                fill: false,
                borderColor: 'rgb(231,109, 132)',
            }
        }
    };

    var thirdSecond = {
        label: getMonthRep(labels[2]),
        data: monthsdata[2],
        options: {
            plugins: {
                lineTension: 0,
                fill: false,
                borderColor: '#18bc9c ',
            }
        }
    };
    var monthsData = {
        labels: keys,
        datasets: [dataFirst, dataSecond, thirdSecond]
    };

    var chartOptions = {
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Category Cumulative Comparison (Last 3 months)',
                    font: {
                        size: 15,
                    }
                },
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        boxWidth: 10,
                    },
                },
            },
        },
    };

    var lineChart = new Chart(monthCumulative, {
        type: 'line',
        data: monthsData,
        options: {
            plugins: {
               chartOptions
            }
        }
    })
};

const getCumulativeExpenses = () => {
    console.log('expenses_source');
    fetch('/personalbudget/last_3months_expense_source_stats')
        .then(res => res.json()).then(data => {
        console.log('data', data)
        showMonthsExpensesChart(data);
    });
}

window.addEventListener('load', getCumulativeExpenses)

