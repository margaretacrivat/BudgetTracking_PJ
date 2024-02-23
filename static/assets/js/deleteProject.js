function confirmDelete(projectId) {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "block";

    // Set projectId for deletion
    document.getElementById("confirmDeleteBtn").setAttribute("data-projects-id", projectId);
}

function closeModal() {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "none";
}

function deleteProject() {
    var projectId = document.getElementById("confirmDeleteBtn").getAttribute("data-projects-id");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/projectbudget/delete-project/" + projectId + "/", true);
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Set CSRF token in request headers
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                window.location.reload();
            } else {
                console.error("Error deleting projects:", xhr.statusText);
            }
            closeModal();
        }
    };
    xhr.send();
}





