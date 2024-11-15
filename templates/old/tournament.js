const participants = ['Team A', 'Team B', 'Team C', 'Team D', 'Team E', 'Team F', 'Team G'];

function createBracket(participants) {
    const bracketContainer = document.getElementById('bracket');
    const rounds = Math.ceil(Math.log2(participants.length)); // Calculate number of rounds needed

    // Create rounds dynamically
    for (let round = 0; round < rounds; round++) {
        const roundDiv = document.createElement('div');
        roundDiv.className = 'round';
        const roundTitle = document.createElement('h2');
        roundTitle.textContent = `Round ${round + 1}`;
        roundDiv.appendChild(roundTitle);

        const matchesDiv = document.createElement('div');
        matchesDiv.className = 'matches';

        const matches = Math.ceil(participants.length / Math.pow(2, round + 1)); // Calculate number of matches in the round

        for (let match = 0; match < matches; match++) {
            const matchDiv = document.createElement('div');
            matchDiv.className = 'match';

            const team1 = document.createElement('div');
            team1.className = 'team';
            team1.textContent = participants[match * 2] || ''; // Get the first team for this match THIS NEEDS TO BE ADJUSTED
            team1.onclick = () => selectWinner(team1.textContent, match);

            const team2 = document.createElement('div');
            team2.className = 'team';
            team2.textContent = participants[match * 2 + 1] || ''; // Get the second team for this match
            team2.onclick = () => selectWinner(team2.textContent, match);

            matchDiv.appendChild(team1);
            matchDiv.appendChild(team2);
            matchesDiv.appendChild(matchDiv);
        }

        roundDiv.appendChild(matchesDiv);
        bracketContainer.appendChild(roundDiv);
    }
}

createBracket(participants);