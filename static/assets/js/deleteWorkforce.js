function confirmDelete(workforceId) {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "block";

    document.getElementById("confirmDeleteBtn").setAttribute("data-workforce-id", workforceId);
}

function closeModal() {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "none";
}

function deleteWorkforce() {
    var workforceId = document.getElementById("confirmDeleteBtn").getAttribute("data-workforce-id");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/projectbudget/delete-workforce/" + workforceId + "/", true);
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Set CSRF token in request headers
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest"); // Set AJAX header
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                window.location.reload();
            } else {
                console.error("Error deleting workforce:", xhr.statusText);
            }
            closeModal();
        }
    };
    xhr.send();
}




