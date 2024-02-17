function confirmDelete(displacementId) {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "block";

    document.getElementById("confirmDeleteBtn").setAttribute("data-displacement-id", displacementId);
}

function closeModal() {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "none";
}

function deleteDisplacement() {
    var displacementId = document.getElementById("confirmDeleteBtn").getAttribute("data-displacement-id");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/projectbudget/delete-displacement/" + displacementId + "/", true);
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Set CSRF token in request headers
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest"); // Set AJAX header
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                window.location.reload();
            } else {
                console.error("Error deleting displacement:", xhr.statusText);
            }
            closeModal();
        }
    };
    xhr.send();
}




