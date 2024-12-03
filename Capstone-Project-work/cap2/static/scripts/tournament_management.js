function redirectToRegister(tournamentId) {
    window.location.href = `/tournament/register?tournament_id=${tournamentId}`;
}

function redirectToBracket(tournamentId) {
    window.location.href = `/tournament/bracket?tournament_id=${tournamentId}`;
}

function toggleForm() {
    var form = document.getElementById("addTournamentForm");
    var button = document.getElementById("displayFormButton");

    // Toggle visibility of the form
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block";  // Show the form
        button.innerHTML = "Hide Form"; // Change button text to hide
        button.style.backgroundColor = "rgba(5, 5, 5, .3)";
    } else {
        form.style.display = "none";  // Hide the form
        button.innerHTML = "Add Tournament"; // Restore button text
        button.style.backgroundColor = "#4CAF50";
    }
}