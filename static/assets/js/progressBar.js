document.addEventListener('DOMContentLoaded', function() {
    var remainingBudget = parseFloat(document.getElementById('budgetCard1').getAttribute('data-remaining-budget'));
    var totalIncome = parseFloat(document.getElementById('budgetCard1').getAttribute('data-total-income'));
    var remainingBudgetPercentage = (remainingBudget / totalIncome) * 100;
    var progressBar = document.querySelector('.budget-progress-bar');
    var tooltip = document.getElementById('progressTooltip');

    // Set the width of the progress bar
    progressBar.style.width = remainingBudgetPercentage + '%';

    // Add conditional styling based on remaining budget percentage
    if (remainingBudgetPercentage < 50) {
        progressBar.style.backgroundColor = 'red';
    } else if (remainingBudgetPercentage < 70) {
        progressBar.style.backgroundColor = 'orange';
    } else {
        progressBar.style.backgroundColor = 'green';  // Default color for remaining percentage >= 70
    }

    // Event listener for mouseover
    progressBar.addEventListener('mouseover', function() {
        showPercentage();  // Call the globally defined function
        tooltip.textContent = remainingBudgetPercentage.toFixed(2) + '%';
    });

    // Event listener for mouseout
    progressBar.addEventListener('mouseout', function() {
        hidePercentage();  // Call the globally defined function
    });
});

// Function to show the tooltip
function showPercentage() {
    var tooltip = document.getElementById('progressTooltip');
    tooltip.style.visibility = 'visible';
}

// Function to hide the tooltip
function hidePercentage() {
    var tooltip = document.getElementById('progressTooltip');
    tooltip.style.visibility = 'hidden';
}