
//what if tournament spans multiple days? added start date end date instead of just date
document.addEventListener('DOMContentLoaded', () => {
    
});

document.addEventListener('DOMContentLoaded', function () {
    // Get the tournament select dropdown element by ID
    const selectElement = document.getElementById('tournament-select');

    // Add an event listener for the 'change' event on the dropdown
    selectElement.addEventListener('change', function () {
        // Get the selected value (the tournament ID)
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
        }
    });
});



function createBracket(data) {
    const bracketContainer = document.getElementById('bracket');
    bracketContainer.innerHTML = ''; // Clear previous content
    const createTeamDiv = (name, members) => {
        const teamDiv = document.createElement('div');
        teamDiv.className = 'team';
        teamDiv.textContent = name ? `Team: ${name}` : (members.length ? members.join(', ') : 'TBD');
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

            // Display team IDs or names for each match
            const team1 = createTeamDiv(match.team_a_name, match.team_a_members);
            const team2 = createTeamDiv(match.team_b_name, match.team_b_members);

            matchDiv.appendChild(team1);
            matchDiv.appendChild(team2);
            matchesDiv.appendChild(matchDiv);
        });

        roundDiv.appendChild(matchesDiv);
        bracketContainer.appendChild(roundDiv);
    }
}
