function openform() {
    document.getElementById("formModal").style.display = "block";
}

function closeform() {
    document.getElementById("formModal").style.display = "none";
}
function openModal() {
    event.preventDefault(); 
    document.getElementById("formModal").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}

function closeModal() {
    document.getElementById("formModal").style.display = "none";
    document.getElementById("overlay").style.display = "none";
} 