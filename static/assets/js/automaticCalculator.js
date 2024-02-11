var costInput = document.getElementById('cost');
var qtyInput = document.getElementById('qty');
var amountInput = document.getElementById('amount');

// Add events to actualize amount based on changing values of cost and qty
costInput.addEventListener('input', updateAmount);
qtyInput.addEventListener('input', updateAmount);

// Function to actualize amount field
function updateAmount() {
    var cost = parseFloat(costInput.value);
    var qty = parseInt(qtyInput.value);

    // Verify if cost and qty are valid numbers
    if (!isNaN(cost) && !isNaN(qty)) {
        // Calculate amount
        var amount = cost * qty;

        // Actualize amount field
        // amountInput.value = parseFloat(amount.toFixed(2)); // show tithes

        // Convert amount to string with two decimal places
        var amountString = amount.toFixed(2);

        // Actualize amount field
        amountInput.value = amountString;

    } else {
        // If cost is not a valid number, erase the field qty
        qtyInput.value = '';
        // If cost or qty are not valid numbers, set amount value to empty
        amountInput.value = '0.00';
    }
}

window.addEventListener('DOMContentLoaded', function() {
    updateAmount();
});
