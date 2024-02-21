var totalBudgetInput = document.getElementById('totalBudget');
var otherExpensesBudgetInput = document.getElementById('otherExpensesBudget');
var totalAmountInput = document.getElementById('totalAmount');

totalBudgetInput.addEventListener('input', updateTotalAmount);
otherExpensesBudgetInput.addEventListener('input', updateTotalAmount);

budgetPerDayInput.addEventListener('input', updateTotalAmount);
daysNoInput.addEventListener('input', updateTotalAmount);

function updateTotalAmount() {
    var total_budget = parseFloat(totalBudgetInput.value);
    var other_expenses_budget = parseFloat(otherExpensesBudgetInput.value);

    console.log("Total Budget:", total_budget);
    console.log("Other Expenses Budget:", other_expenses_budget);

    if (!isNaN(total_budget) && !isNaN(other_expenses_budget)) {
        var total_amount = total_budget + other_expenses_budget;
        console.log("Calculated total amount:", total_amount);

        var totalAmountString = total_amount.toFixed(2);
        totalAmountInput.value = totalAmountString;

    } else {
        // otherExpensesBudgetInput ='';
        totalAmountInput.value = '0.00';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    updateTotalAmount();
});

document.querySelector('.add-displacement-form').addEventListener('submit', function(event) {
    updateTotalAmount();
});