var salaryPerHourInput = document.getElementById('salaryPerHour');
var workDaysInput = document.getElementById('workDays');
var salaryRealizedInput = document.getElementById('salaryRealized');
var vacationLeaveDaysInput = document.getElementById('vacationLeaveDays');
var vacationReimbursedAmountInput = document.getElementById('vacationReimbursedAmount');


salaryPerHourInput.addEventListener('input', updateSalaryRealized);
workDaysInput.addEventListener('input', updateSalaryRealized);
vacationLeaveDaysInput.addEventListener('input', updateVacationReimbursedAmount);

function updateSalaryRealized() {
    var salary_per_hour = parseFloat(salaryPerHourInput.value);
    var work_days = parseInt(workDaysInput.value);

    console.log("Salary per hour:", salary_per_hour);
    console.log("Work Days:", work_days);

    if (!isNaN(salary_per_hour) && !isNaN(work_days)) {
        var salary_realized = salary_per_hour * work_days;
        console.log("Calculated salary realized:", salary_realized);

        var salaryRealizedString = salary_realized.toFixed(2);
        salaryRealizedInput.value = salaryRealizedString;
    } else {
        workDaysInput.value = '';
        salaryRealizedInput.value = '0.00';
    }
}

document.querySelector('.add-workforce-form').addEventListener('submit', function (event) {
    updateSalaryRealized();
});

function updateVacationReimbursedAmount() {
    var salary_per_hour = parseFloat(salaryPerHourInput.value);
    var vacation_leave_days = parseInt(vacationLeaveDaysInput.value);

    console.log("Salary per hour:", salary_per_hour);
    console.log("Vacation Leave Days:", vacation_leave_days);

    if (!isNaN(salary_per_hour) && !isNaN(vacation_leave_days)) {
        var vacation_reimbursed_amount = salary_per_hour * vacation_leave_days;
        console.log("Calculated vacation reimbursed amount:", vacation_reimbursed_amount);

        var vacationReimbursedAmountString = vacation_reimbursed_amount.toFixed(2);
        vacationReimbursedAmountInput.value = vacationReimbursedAmountString;
    } else {
        vacationLeaveDaysInput.value = '';
        vacationReimbursedAmountInput.value = '0.00';
    }
}

document.querySelector('.add-workforce-form').addEventListener('submit', function (event) {
    updateVacationReimbursedAmount();
});

