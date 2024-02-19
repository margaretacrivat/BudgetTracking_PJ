var salaryPerHourInput = document.getElementById('salaryPerHour');
var workDaysInput = document.getElementById('workDays');
var amountInput = document.getElementById('amount');

// Add events to actualize amount based on changing values of salary_per_hour and days_no
salaryPerHourInput.addEventListener('input', updateAmount);
workDaysInput.addEventListener('input', updateAmount);

function updateAmount() {
    var salary_per_hour = parseFloat(salaryPerHourInput.value);
    var work_days = parseInt(workDaysInput.value);

    console.log("Salary per hour:", salary_per_hour);
    console.log("Days no:", work_days);

    if (!isNaN(salary_per_hour) && !isNaN(work_days)) {
        var amount = salary_per_hour * work_days;
    console.log("Calculated amount:", amount);

        // Actualize amount field
        // amountInput.value = parseFloat(amount.toFixed(2)); // show tithes

        // Convert amount to string with two decimal places
        var amountString = amount.toFixed(2);

        // Actualize amount field
        amountInput.value = amountString;

    } else {
        workDaysInput.value = '';
        amountInput.value = '0.00';
    }
}

document.querySelector('.add-workforce-form').addEventListener('submit', function(event) {
    updateAmount();
});
