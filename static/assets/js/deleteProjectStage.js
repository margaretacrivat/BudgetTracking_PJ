function confirmDelete(project_stageId) {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "block";

    document.getElementById("confirmDeleteBtn").setAttribute("data-projects-stage-id", project_stageId);
}

function closeModal() {
    var modal = document.getElementById("deleteConfirmationModal");
    modal.style.display = "none";
}

function deleteProjectStage() {
    var project_stageId = document.getElementById("confirmDeleteBtn").getAttribute("data-projects-stage-id");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/projectbudget/delete-project-stage/" + project_stageId + "/", true);
    // Fetch CSRF token from HTML
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Set CSRF token in request headers
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                window.location.reload();
            } else {
                console.error("Error deleting projects stage:", xhr.statusText);
            }
            closeModal();
        }
    };
    xhr.send();
}





