
// delete Project

function confirmDelete(projectId) {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "block";

    // Set expenseId for deletion
    document.getElementById("confirmDeleteBtn").setAttribute("data-project-id", projectId);
}

function closeModal() {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "none";
}

function deleteProject() {
    var projectId = document.getElementById("confirmDeleteBtn").getAttribute("data-project-id");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/projectbudget/delete-project/" + projectId + "/", true);
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Set CSRF token in request headers
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest"); // Set AJAX header
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Handle successful deletion
                window.location.reload(); // Optionally reload the page
            } else {
                // Handle error
                console.error("Error deleting project:", xhr.statusText);
                // Display error message to the user
            }
            closeModal(); // Close the modal regardless of the response
        }
    };
    xhr.send();
}





