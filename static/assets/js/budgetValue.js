document.querySelectorAll('.budget-input').forEach(function (input) {
    if (input.value.trim() === '0' || input.value.trim() === '') {
        input.value = '0.00';
    } else {
        // Dacă valoarea inițială nu este 0 sau goală, asigurați-vă că are două zecimale
        var floatValue = parseFloat(input.value).toFixed(2);
        input.value = floatValue;
    }

    input.addEventListener('input', function (event) {
        var value = event.target.value.trim().replace(/[^\d.]/g, '').replace(/^0+/, '');
        var cursorPosition = event.target.selectionStart;

        // Check if the value is empty
        if (value === '') {
            // event.target.value = value;
            event.target.value = '0.00';
            event.target.setSelectionRange(0, 0);
            return;
        }

        // If the user pressed the "." key
        if (event.data === '.') {
            // Move the cursor after the decimal point
            cursorPosition = value.indexOf('.') + 1;

            // If the cursor is at the beginning, set it after the "."
            if (cursorPosition === 0) {
                cursorPosition = value.indexOf('.') + 1;
            }
        }

        // Ensure that decimal part has two digit
        if (value.includes('.')) {
            var parts = value.split('.');
            var decimalPart = parts[1].substring(0, 2);
            value = parts[0] + '.' + decimalPart;
            // Keep cursor unchanged if after decimal point
            if (cursorPosition > parts[0].length) {
                cursorPosition = event.target.selectionStart;
            }
        } else {
            // No decimal point entered yet, append '.00'
            value += '.00';
            // Move cursor to integer part if after decimal point
            if (cursorPosition > value.length - 3) {
                cursorPosition = value.length - 3;
            }
        }

        // Update the input value and cursor position
        event.target.value = value;
        event.target.setSelectionRange(cursorPosition, cursorPosition);
    });

    input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            // Prevent the default action of the Enter key
            event.preventDefault();

            // Set the cursor position after the "."
            var value = event.target.value;
            var cursorPosition = value.indexOf('.') + 1;

            // Update the cursor position
            event.target.setSelectionRange(cursorPosition, cursorPosition);
        }
    });
});