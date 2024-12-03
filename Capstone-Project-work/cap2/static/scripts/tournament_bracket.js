
//what if tournament spans multiple days? added start date end date instead of just date

document.addEventListener('DOMContentLoaded', function () { //Listener for select menu changes
    const tournamentId = 1;  // This is the ID you're searching for
    
    const selectElement = document.getElementById('tournament-select');
    selectElement.addEventListener('change', function () {
        const selectedTournamentId = selectElement.value;
        // If a tournament is selected (i.e., the value is not empty)
        if (selectedTournamentId) {
            console.log('Selected Tournament ID:', selectedTournamentId);

            fetch(`/api/get_matches?tournament_id=${selectedTournamentId}`) //Note: must use backticks here for inserting variable
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    createBracket(data);
                })
                .catch(error => console.error('Error fetching tournament data:', error));
        } else {
            console.log('No tournament selected');
            hideResetBtn();
            createBracket([]);
        }
    });
});

document.getElementById("create-bracket-btn").addEventListener('click', function () {
    const selectElement = document.getElementById('tournament-select');
    const tournamentId = selectElement.value;
    const selectedTournament = tournaments.find(t => t.id == tournamentId);
    console.log(selectedTournament.type);
    if (tournamentId) {
        const tournamentType = selectedTournament.type.toLowerCase().replace(/ /g, '_');
        const url = `/create_${tournamentType}_bracket?tournament_id=${tournamentId}`;
        fetch(url, {
            method: 'POST',
        })
            .then(response => response.json()) // Assuming the server returns JSON
            .then(data => {
                console.log(data);
                // Handle the response here if needed
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        alert("Please select a tournament first.");
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const selectEle = document.getElementById('tournament-select');
    selectEle.value = new URLSearchParams(window.location.search).get('tournament_id') || '';
    selectEle.dispatchEvent(new Event('change')); //Trigger all the above logic onload (basically hide one of the buttons and print placeholder text/show matches)
});

function hideResetBtn() {
    document.getElementById('reset-btn').style.display = 'none';
    document.getElementById('create-bracket-btn').style.display = '';
}
function hideStartBtn() {
    document.getElementById('create-bracket-btn').style.display = 'none';
    document.getElementById('reset-btn').style.display = '';
}


function createBracket(data) {        //Helper function to populate bracket upon select menu change
    const bracketContainer = document.getElementById('bracket');
    bracketContainer.innerHTML = '';
    if (data.length == 0) {
        bracketContainer.textContent = 'No matches generated.';
        hideResetBtn();
        return;
    }
    else {
        hideStartBtn();
    }

    const createTeamDiv = (name, members, score, team_id) => {
        const teamDiv = document.createElement('div');
        teamDiv.className = 'team';
        teamDiv.textContent = name ? `*${name}` : (members.length ? members.join(', ') : 'TBD');
        
        const scoreSpan = document.createElement('span');
        scoreSpan.className = 'score';
        scoreSpan.textContent = score ? ` | ${score}` : name || members.length ? " | 0" : "";
        teamDiv.appendChild(scoreSpan);
        teamDiv.dataset.teamId = team_id;
        return teamDiv;
    };

    // Group matches by round number
    const rounds = {};
    data.forEach(match => {
        const round = match.round_number;
        if (!rounds[round]) {
            rounds[round] = [];
        }
        rounds[round].push(match);
    });

    // Create rounds dynamically
    for (const round in rounds) {
        const roundDiv = document.createElement('div');
        roundDiv.className = 'round';
        const roundTitle = document.createElement('h2');
        roundTitle.textContent = `Round ${round}`;
        roundDiv.appendChild(roundTitle);

        const matchesDiv = document.createElement('div');
        matchesDiv.className = 'matches';

        rounds[round].forEach(match => {
            const matchDiv = document.createElement('div');
            matchDiv.className = 'match';
            matchDiv.dataset.teamAId = match.team_a_id;
            matchDiv.dataset.teamBId = match.team_b_id;
            matchDiv.dataset.matchId = match.match_id;
            matchDiv.dataset.matchRound = match.round_number;
            // Display team IDs or names for each match
            const team1 = createTeamDiv(match.team_a_name, match.team_a_members, match.player_a_score, match.team_a_id); //THIS IS VERY IMPORTANT FUNCTION CALL
            const team2 = createTeamDiv(match.team_b_name, match.team_b_members, match.player_b_score, match.team_b_id);

            matchDiv.appendChild(team1);
            matchDiv.appendChild(team2);
            matchesDiv.appendChild(matchDiv);
        });

        roundDiv.appendChild(matchesDiv);
        bracketContainer.appendChild(roundDiv);


    }
    


    const matches = document.querySelectorAll('.match');
    const dialog = document.getElementById('scoreDialog');
    const closeDialogButton = document.getElementById('closeDialog');
    const scoreForm = document.getElementById('scoreForm');
    const score1Input = document.getElementById('score1');
    const score2Input = document.getElementById('score2');
    const winner1Radio = document.getElementById('winner1');
    const winner2Radio = document.getElementById('winner2');
    const teamADisplay = document.getElementById('teamA'); // Display team A name
    const teamBDisplay = document.getElementById('teamB'); // Display team B name
    let currentMatch = null;  // Store the current match details
    // Add a click event listener to each element
    matches.forEach((match) => {
        match.addEventListener('click', (event) => {
            // Do something when a match is clicked
            console.log('Match clicked:', match);
            dialog.style.display = 'block';
            // You can also access the clicked element with `event.target`
            console.log('Clicked element:', event.target);
            scoreForm.dataset.matchId = match.dataset.matchId;
            scoreForm.dataset.teamAId = match.dataset.teamAId;
            scoreForm.dataset.teamBId = match.dataset.teamBId;
            scoreForm.dataset.matchRound = match.dataset.matchRound;
            // Example: Change the background color on click
            match.style.backgroundColor = 'lightblue';
        });
    });
    closeDialogButton.addEventListener('click', () => {
        dialog.style.display = 'none';
        scoreForm.reset();
        winner1Radio.checked = false;
        winner2Radio.checked = false;
    });

    scoreForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const score1 = parseInt(score1Input.value, 10);
        const score2 = parseInt(score2Input.value, 10);
        const send_data = {
            match_id: scoreForm.dataset.matchId,
            match_round: scoreForm.dataset.matchRound,
            team_a_id: scoreForm.dataset.teamAId,
            team_b_id: scoreForm.dataset.teamBId
        };
        console.log(send_data);
        //console.log(scoreForm.dataset.matchId);
        const winner = winner1Radio.checked ? 1 : (winner2Radio.checked ? 2 : null);
        const tournamentId = document.getElementById('tournament-select').value;
        var winner_id;
        if (score1 && score2 && winner !== null) {
            if (winner == 1) {
                winner_id = send_data['team_a_id']
            }
            else {
                winner_id = send_data['team_b_id']
            }
            send_data.winner_id = winner_id;
            send_data.score_a = score1;
            send_data.score_b = score2;
            console.log(`Score 1: ${score1}, Score 2: ${score2}, Winner: Team ${winner}`);
            const url = `/select_winner?tournament_id=${tournamentId}`;
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Tell the server we're sending JSON data
                },
                body: JSON.stringify(send_data), // Convert data object to JSON string
                })
                .then(response => {
                    if (response.ok) {
                        //window.location.href = response.url;
                    } else {
                        console.error('Error with select_winner call');
                    }
                }) // Parse the JSON response from the server
                .then(data => {
                    console.log('Success:', data); // Handle success
                })
                .catch((error) => {
                    console.error('Error:', error); // Handle any errors
                });
            dialog.style.display = 'none';
        } else {
            alert('Please fill in all fields.');
        }
        scoreForm.reset();
        winner1Radio.checked = false;
        winner2Radio.checked = false;
    });
}
