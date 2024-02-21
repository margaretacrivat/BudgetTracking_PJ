var budgetPerDayInput = document.getElementById('budgetPerDay');
var daysNoInput = document.getElementById('daysNo');
var totalBudgetInput = document.getElementById('totalBudget');

budgetPerDayInput.addEventListener('input', updateTotalBudget);
daysNoInput.addEventListener('input', updateTotalBudget);

function updateTotalBudget() {
    var budget_per_day = parseFloat(budgetPerDayInput.value);
    var days_no = parseInt(daysNoInput.value);

    console.log("Budget per day:", budget_per_day);
    console.log("Days no:", days_no);

    if (!isNaN(budget_per_day) && !isNaN(days_no)) {
        var total_budget = budget_per_day * days_no;
        console.log("Calculated total budget:", total_budget);

        var budgetString = total_budget.toFixed(2);

        totalBudgetInput.value = budgetString;

    } else {
        daysNoInput.value = '';
        totalBudgetInput.value = '0.00';
    }
}

document.querySelector('.add-displacement-form').addEventListener('submit', function (event) {
    updateTotalBudget();
});
