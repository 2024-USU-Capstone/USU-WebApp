import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from functools import wraps
from equipment import load_equipment_data, save_equipment_data, initial_data

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
    database="user",  # Use your database name
    user="root",                 # Use your database username
    password='',
    port=3306
    )
'''
mydb= mysql.connector.connect(
    host=MYSQL_HOST,
    database=MYSQL_DATABASE,  # Use your database name
    user=MYSQL_USER,                 # Use your database username
    password=MYSQL_PASSWORD,
    port=MYSQL_PORT
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
        if result is not None:
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


# Route for Tournament Schedule page
@app.route('/tournament')
@login_required  # Restrict access to this page unless the user is logged in
def tournament():
    return render_template('tournament.html')

## Logout route
@app.route('/logout')
@login_required  # Protect this route
def logout():
    session.clear()  # Clear the session data to log the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


import os

if __name__ == "__main__":
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')  # Default to localhost
    port = int(os.getenv('FLASK_RUN_PORT', 8080))  # Default to port 8080
    app.run(host=host, port=port, debug=False)

