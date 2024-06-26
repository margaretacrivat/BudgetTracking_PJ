
// delete Expenses

function confirmDelete(expenseId) {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "block";

    // Set expenseId for deletion
    document.getElementById("confirmDeleteBtn").setAttribute("data-expense-id", expenseId);
}

function closeModal() {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "none";
}

function deleteExpense() {
    var expenseId = document.getElementById("confirmDeleteBtn").getAttribute("data-expense-id");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/personalbudget/delete-expense/" + expenseId + "/", true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest"); // Set AJAX header
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Handle successful deletion
                window.location.reload(); // Optionally reload the page
            } else {
                // Handle error
                console.error("Error deleting expense:", xhr.statusText);
                // Display error message to the user
            }
            closeModal(); // Close the modal regardless of the response
        }
    };
    xhr.send();
}





