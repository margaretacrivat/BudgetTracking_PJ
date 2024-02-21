var salaryRealizedInput = document.getElementById('salaryRealized');
var vacationReimbursedAmountInput = document.getElementById('vacationReimbursedAmount');
var grossSalaryAmountInput = document.getElementById('grossSalaryAmount');

salaryRealizedInput.addEventListener('input', updateGrossSalaryAmount);
vacationReimbursedAmountInput.addEventListener('input', updateGrossSalaryAmount);

workDaysInput.addEventListener('input', updateGrossSalaryAmount);
vacationLeaveDaysInput.addEventListener('input', updateGrossSalaryAmount);

function updateGrossSalaryAmount() {
    var salary_realized = parseFloat(salaryRealizedInput.value);
    var vacation_reimbursed_amount = parseFloat(vacationReimbursedAmountInput.value);

    console.log("Salary Realized:", salary_realized);
    console.log("Vacation Days Reimbursed Amount:", vacation_reimbursed_amount);

    if (!isNaN(salary_realized)) {
        var gross_salary_amount = salary_realized + vacation_reimbursed_amount;
    console.log("Calculated total amount:", gross_salary_amount);

        var grossSalaryAmountString = gross_salary_amount.toFixed(2);
        grossSalaryAmountInput.value = grossSalaryAmountString;
    } else {
        grossSalaryAmountInput.value = '0.00';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    updateGrossSalaryAmount();
});

document.querySelector('.add-workforce-form').addEventListener('submit', function(event) {
    updateGrossSalaryAmount();
});
