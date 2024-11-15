import os
import json
import math
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from functools import wraps
from equipment import load_equipment_data, save_equipment_data, initial_data
from db_utils import *
app = Flask(__name__)
app.secret_key = '!@#$%^&*(jhdshgsd'  # Required for flash messages




##---------- WE NEED THIS FOR SETTING ENVIRONMENT----------

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_PORT = os.environ.get('MYSQL_PORT')

##-----------------------------------------------------------
'''
##DATABSE CONNECTION 
mydb= mysql.connector.connect(
    host="127.0.0.1",
    database="",  # Use your database name
    user="root",                 # Use your database username
    password='',
    port=3306
    )
'''

mydb= mysql.connector.connect(
    host="127.0.0.1",
    database="mydatabase",  # Use your database name
    user="root",                 # Use your database username
    password="root",
    port=3306
    )


##THIS IS TO CHECK THE DATABSE TABLE
def table_check(fname, lname, studentid, equip, status):
    try:
        # Establishing a database connection
        cursor = mydb.cursor()

        # Create the table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS accounts (
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            student_id INT(11) NOT NULL,
            equipment VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (student_id)
        );
        """
        cursor.execute(create_table_query) #EXECUTE THE COMMAND TO CREATE THE TABLE
        mydb.commit()

         # Check if the student already has a record with the given status (CHECKIN OR CHECKOUT)
        select_query = """
        SELECT status FROM accounts WHERE student_id = %s;
        """
        cursor.execute(select_query, (studentid,))  ##PERFORMS THE QUERY FOR FETCHING THE STATUS
        result = cursor.fetchone()  # Fetch one result

        if result:
            current_status = result[0]

            # If the current status is 'check-out', update to 'check-in'
            if current_status == 'check-out':
                update_query = """
                UPDATE accounts SET status = 'check-in' , timestamp = CURRENT_TIMESTAMP WHERE student_id = %s;
                """
                cursor.execute(update_query, (studentid,))
                mydb.commit()
                print("Status updated to check-in successfully!")
            #if the current status is 'check-in', insert into the table new record of user to checkout new equipment
            elif current_status == 'check-in':
                update_query = """
                UPDATE accounts 
                SET status = 'check-out', equipment = %s, timestamp = CURRENT_TIMESTAMP 
                WHERE student_id = %s;
                """
                cursor.execute(update_query, (equip, studentid))
                mydb.commit()
                print("Data inserted successfully!")

        else:
            # Insert data from the form if no existing record is found FROM THE TABLE QUERY
            insert_query = """
            INSERT INTO accounts (first_name, last_name, student_id, equipment, status)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (fname, lname, studentid, equip, status))
            mydb.commit()
            print("Data inserted successfully!")
        return result

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()




##THIS CHECK THE DATABASE FOR THE POROVIDED USER LOGIN
def validate_login(username, password):
    try:
        # Establishing a database connection
        cursor = mydb.cursor()
        # Example query to validate login (modify as needed)
        cursor.execute("SELECT * FROM Employees WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
# A decorator to ensure the user is logged in before accessing any routes
# A decorator to ensure the user is logged in before accessing any routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in by checking the session
        if 'logged_in' not in session or not session['logged_in']:
            flash('You must be logged in to access this page.', 'warning')
            return redirect(url_for('login'))  # Redirect to login page if not logged in
        return f(*args, **kwargs)
    return decorated_function

#THIS IS TO ROUTE THE LOGIN PAGE
## Login route handling
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate credentials
        if validate_login(username, password):
            session['logged_in'] = True  # Set session flag to indicate user is logged in
            session['username'] = username  # Optionally store the username in the session
            flash('Login successful!', 'success')
            return redirect(url_for('mainmenu'))  # Redirect to a protected page after successful login
        else:
            flash('INVALID USERNAME OR PASSWORD', 'danger')

    return render_template('login.html')  # Render the login HTML template


# Route for main menu PAGE OF CHECKIN CHECKOUT HOMEPAGE 
@app.route('/mainmenu')
@login_required  # Restrict access to this page unless the user is logged in
def mainmenu():
    return render_template('main-menu.html')

@app.route('/activity')
@login_required  # Restrict access to this page unless the user is logged in
def activity():
    try:
        # Create the cursor object
        page = int(request.args.get('page', 1))  # Get current page number from query parameters
        per_page = 20
        conn = mydb.cursor()

        # Define the query
        total_query = 'SELECT COUNT(*) FROM accounts'
        #query = 'SELECT first_name, last_name, student_id, equipment, status, timestamp FROM accounts'
        
        # Execute the query
        #conn.execute(query)
        conn.execute(total_query)
        total_rows = conn.fetchone()[0]
        
        # Fetch all rows from the executed query
        #rows = conn.fetchall()  
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (total_rows + per_page - 1) // per_page

        query = 'SELECT first_name, last_name, student_id, equipment, status, timestamp FROM accounts LIMIT %s OFFSET %s'
        conn.execute(query, (per_page, start))
        rows = conn.fetchall()
        if not rows:
            rows = []


    # Pass the result to the template


    except mysql.connector.Error as err:
        # Log the error and show an error page or message
        print(f"Database error: {err}")
        rows = []
        total_pages = 1
    finally:
        # Always close the cursor/connection if it was opened
        if conn:
            conn.close()

    # Pass the result to the temgplaxtessk
   
    #return render_template('equipment.html', rows=rows)

    return render_template('activity.html', rows=rows, page=page, total_pages=total_pages)



@app.route('/equipments')
@login_required  # Restrict access to this page unless the user is logged in
def equipments():
    # Load initial equipment data
    equipment_data = load_equipment_data()

    # If no data is loaded (e.g., file not found), initialize with initial_data
    if not equipment_data:
        equipment_data = initial_data
        save_equipment_data(equipment_data)
    return render_template('equipments.html', equipment_data=equipment_data)


'''
@app.route('/update_availability', methods=['POST'])
def update_availability():
    item_id = int(request.form['item_id'])
    availability = request.form['availability']

    # Load existing data
    equipment_data = load_equipment_data()

    # Update the item's availability
    for item in equipment_data:
        if item['id'] == item_id:
            if availability == "available":
                item['available'] = True
            else:  
                item['available'] = False
            break
    # Save the updated data
    save_equipment_data(equipment_data)

    return redirect(url_for('equipment'))
'''
def check_status(student_id):
    try:
        # Establishing a database connection
        cursor = mydb.cursor()

        # Check if the student status already has a record with the given student_id
        select_query = """
        SELECT status,timestamp FROM accounts WHERE student_id = %s;
        """
        cursor.execute(select_query, (student_id,))  # Notice the comma for a single-element tuple
        result = cursor.fetchone()  # Fetch one result

        if result:
            return result[0], result[1]  # Return the status if found
        else:
            return None  # Return None if no record is found
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    


@app.route('/checkinout', methods=['GET', 'POST'])
@login_required  # Restrict access to this page unless the user is logged in
def checkinout():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        studentid = request.form['studentid']
        equipment = request.form['equipment']
        status = request.form['status']

        result = check_status(studentid)
        if isinstance(result, tuple):
            current_status, previous_time = result
        else:
            current_status, previous_time = None, None
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if current_status == status:
            flash(f'You are currently {current_status} at {previous_time}.', 'danger')  # Using string formatting
            return redirect(url_for('checkinout'))
        else:
            # Proceed with other logic, like updating or inserting the record
            table_check(fname, lname, studentid, equipment, status)
            new_status = check_status(studentid)[0]
            flash(f'You successfully {new_status} at {current_time}', 'success')
    
    return render_template('checkinout.html')

## Logout route
@app.route('/logout')
@login_required  # Protect this route
def logout():
    session.clear()  # Clear the session data to log the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

################################
#### TOURNAMENT MANAGEMENT ####
################################

@app.route('/tournament/bracket', methods=['GET'])
@login_required
def tournament_bracket():
    tournaments = load_tournaments(mydb)
    return render_template('tournament_bracket.html', tournaments=tournaments)

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
        return render_template('tournament_register.html', tournaments=load_tournaments(mydb), students=load_tournament_students(mydb), tournament_id=request.form['tournament_id'])
    return render_template('tournament_register.html', tournaments=load_tournaments(mydb), students=load_tournament_students(mydb))

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
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8082",debug=True)








    #Control access to internal use of api points because of student data use: authentication/auth, rate limiting?
    #cursor.execute("SELECT * FROM Tournament_participants JOIN Tournaments ON Tournament_participants.tournament_id = Tournaments.tournament_id WHERE Tournaments.tournament_start <= CURRENT_DATE and Tournaments.tournament_end >= CURRENT_DATE;")
    # Assuming data is a list of tuples, convert it to a list of dictionaries
    #how to add formatting to these sql statements to add readability?
