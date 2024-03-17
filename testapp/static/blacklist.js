function openForm() {
    event.preventDefault(); 
    document.getElementById("formModal").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}

function closeForm() {
    document.getElementById("formModal").style.display = "none";
    document.getElementById("overlay").style.display = "none";
} 
function openModal() {
    event.preventDefault(); 
    document.getElementById("changes").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}

function closeModal() {
    document.getElementById("changes").style.display = "none";
    document.getElementById("overlay").style.display = "none";
} 