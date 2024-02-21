function confirmDelete(personId) {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "block";

    document.getElementById("confirmDeleteBtn").setAttribute("data-person-id", personId);
}

function closeModal() {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "none";
}

function deletePerson() {
    var personId = document.getElementById("confirmDeleteBtn").getAttribute("data-person-id");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/projectbudget/delete-person/" + personId + "/", true);
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Set CSRF token in request headers
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest"); // Set AJAX header
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                window.location.reload();
            } else {
                console.error("Error deleting person:", xhr.statusText);
            }
            closeModal();
        }
    };
    xhr.send();
}




