################################
#### TOURNAMENT MANAGEMENT ####
################################

@app.route('/tournament', methods=['GET'])
@login_required
def tournament():
    tournaments = load_tournaments(mydb)
    return render_template('tournament.html', tournaments=tournaments)

@app.route('/tournament/register', methods=['GET', 'POST'])
@login_required
def tournament_register():
    if request.method == 'POST':
        register_student(mydb, {
            'fname': request.form['fname'],
            'lname': request.form['lname'],
            'studentid': request.form['studentid'],
            'tournament_id': request.form['tournament_id'],
            'team_name': request.form.get('team_name') if request.form.get('team_name') else None #Use .get on .form if value may be null

        }) 
        flash('Registration successful!', 'success')
        return redirect(url_for('tournament_management'))
    return render_template('tournament_register.html', tournaments=load_tournaments(mydb))

@app.route('/tournament/management')
@login_required
def tournament_management():
    tournaments = load_tournaments(mydb)
    return render_template('tournament_management.html', tournaments=tournaments)

@app.route('/tournament/add_tournament', methods=['POST'])
@login_required
def add_tournament():
    insert_tournament(mydb, { 
        'name': request.form['tournament_name'], 
        'date': request.form['date'], 
        'start_time': request.form['start_time'], 
        'end_time': request.form['end_time'], 
        'location': request.form['location'],
        'type': request.form['tournament_type'],
        'team_based': request.form.get('team_based') if request.form.get('team_based') else 'FALSE'
    })
    flash('Tournament added successfully!', 'success')
    return redirect(url_for('tournament_management'))

@app.route('/remove_tournament/<tournament_id>', methods=['POST'])
@login_required
def remove_tournament(tournament_id):
    delete_tournament(mydb, tournament_id)            
    flash('Tournament deleted successfully!', 'success')
    return redirect(url_for('tournament_management'))


@app.route('/create_single_elimination_bracket', methods=['POST'])
@login_required
def create_single_elimination_bracket(): 
    tournament_id = request.args.get('tournament_id')
    response1 = create_bracket_single_elim(mydb, tournament_id)
    return {"message": "Single elimination bracket created successfully.", "matches": response1, "status":200}


@app.route('/api/get_matches')
@login_required
def get_matches():
    tournament_id = request.args.get('tournament_id')
    return select_matches(mydb, tournament_id)
    