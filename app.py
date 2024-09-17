import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Path to the equipment data file
EQUIPMENT_FILE = 'equipment_data.json'

def load_equipment_data():
    """Load equipment data from a JSON file."""
    try:
        with open(EQUIPMENT_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # If file does not exist, initialize with an empty list
        return []
    except json.JSONDecodeError:
        # If file is not valid JSON, initialize with an empty list
        return []

def save_equipment_data(data):
    """Save equipment data to a JSON file."""
    with open(EQUIPMENT_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Initial equipment data
initial_data = [
    # Xbox
    {'name': 'Assassins Creed IV Black Flag', 'console': 'Xbox', 'available': True},
    {'name': 'Battlefield 1', 'console': 'Xbox', 'available': True},
    {'name': 'Battlefield 4', 'console': 'Xbox', 'available': True},
    {'name': 'Call of Duty Ghosts', 'console': 'Xbox', 'available': False},
    {'name': 'Call of Duty Modern Warfare', 'console': 'Xbox', 'available': True},
    {'name': 'Call of Duty Vanguard', 'console': 'Xbox', 'available': True},
    {'name': 'Call of Duty WW1', 'console': 'Xbox', 'available': True},
    {'name': 'Dead Rising 3', 'console': 'Xbox', 'available': True},
    {'name': 'Destiny 2', 'console': 'Xbox', 'available': False},
    {'name': 'FIFA 22', 'console': 'Xbox', 'available': True},
    {'name': 'Forza Motorsport 5', 'console': 'Xbox', 'available': True},
    {'name': 'Halo 5', 'console': 'Xbox', 'available': False},
    {'name': 'Halo Reach', 'console': 'Xbox', 'available': True},
    {'name': 'Halo Master Chief Collection', 'console': 'Xbox', 'available': True},
    {'name': 'Halo Infinite', 'console': 'Xbox', 'available': True},
    {'name': 'Injustice 2', 'console': 'Xbox', 'available': False},
    {'name': 'Madden NFL 22', 'console': 'Xbox', 'available': True},
    {'name': 'Minecraft', 'console': 'Xbox', 'available': True},
    {'name': 'Mortal Kombat 11', 'console': 'Xbox', 'available': True},
    {'name': 'Mortal Kombat XL', 'console': 'Xbox', 'available': True},
    {'name': 'Naruto Shippuden: Ultimate Ninja Storm 4 ROAD TO BORUTO', 'console': 'Xbox', 'available': True},
    {'name': 'NBA 2K22', 'console': 'Xbox', 'available': False},
    {'name': 'Overwatch Origins Edition', 'console': 'Xbox', 'available': True},
    {'name': 'Rocket League', 'console': 'Xbox', 'available': True},
    {'name': 'Tekken 7', 'console': 'Xbox', 'available': True},
    {'name': 'Tom Clancy\'s Rainbow 6 Siege', 'console': 'Xbox', 'available': False},

    # PlayStation
    {'name': 'Battlefield 1', 'console': 'PlayStation', 'available': True},
    {'name': 'Battlefield 4', 'console': 'PlayStation', 'available': True},
    {'name': 'Call of Duty Ghosts', 'console': 'PlayStation', 'available': False},
    {'name': 'Call of Duty WW2', 'console': 'PlayStation', 'available': True},
    {'name': 'Call of Duty Modern Warfare', 'console': 'PlayStation', 'available': True},
    {'name': 'Destiny 2', 'console': 'PlayStation', 'available': True},
    {'name': 'Injustice 2', 'console': 'PlayStation', 'available': True},
    {'name': 'Madden 20', 'console': 'PlayStation', 'available': True},
    {'name': 'Madden 22', 'console': 'PlayStation', 'available': True},
    {'name': 'Naruto Shippuden: Ultimate Ninja Storm 4 ROAD TO BORUTO', 'console': 'PlayStation', 'available': True},
    {'name': 'Need for Speed Rivals', 'console': 'PlayStation', 'available': True},
    {'name': 'Rainbow 6 Siege', 'console': 'PlayStation', 'available': True},
    {'name': 'Street Fighter V', 'console': 'PlayStation', 'available': True},
    {'name': 'Mortal Kombat XL', 'console': 'PlayStation', 'available': True},
    {'name': 'Rocket League Collectors Edition', 'console': 'PlayStation', 'available': True},
    {'name': 'Tekken 7', 'console': 'PlayStation', 'available': False},
    {'name': 'Spider-man', 'console': 'PlayStation', 'available': True},
    {'name': 'Mortal Kombat 11', 'console': 'PlayStation', 'available': True},
    {'name': 'NBA 2K22', 'console': 'PlayStation', 'available': True},
    {'name': 'The Last of Us Remastered', 'console': 'PlayStation', 'available': False},
    {'name': 'Soulcalibur VI', 'console': 'PlayStation', 'available': True},
    {'name': 'FIFA 22', 'console': 'PlayStation', 'available': True},
    {'name': 'FIFA 24', 'console': 'PlayStation', 'available': True},
    {'name': 'Overwatch', 'console': 'PlayStation', 'available': True},
    {'name': 'God of War', 'console': 'PlayStation', 'available': True},
    {'name': 'Dead by Daylight', 'console': 'PlayStation', 'available': True},
    {'name': 'Plants vs Zombies: Garden Warfare 2', 'console': 'PlayStation', 'available': True},

    # Switch
    {'name': 'Mario Party Super Stars', 'console': 'Switch', 'available': True},
    {'name': 'Super Smash Bros Ultimate', 'console': 'Switch', 'available': True},
    {'name': 'New Super Mario Bros. U Deluxe', 'console': 'Switch', 'available': True},
    {'name': 'Mario Kart 8 Deluxe', 'console': 'Switch', 'available': True},
    {'name': 'Taiko no Tatsujin Nintendo Switch Version', 'console': 'Switch', 'available': True},
    {'name': 'Overcooked 2', 'console': 'Switch', 'available': True},
]

# Load initial equipment data
equipment_data = load_equipment_data()

# If no data is loaded (e.g., file not found), initialize with initial_data
if not equipment_data:
    equipment_data = initial_data
    save_equipment_data(equipment_data)

# Route for main menu
@app.route('/')
def main_menu():
    return render_template('main_menu.html')

# Route for Check In/Out page
@app.route('/checkinout', methods=['GET', 'POST'])
def checkinout():
    if request.method == 'POST':
        name = request.form['name']
        numberid = request.form['numberid']
        equipment_name = request.form['equipment']
        action = request.form['action']

        equipment_item = next((item for item in equipment_data if item['name'].lower() == equipment_name.lower()), None)

        if equipment_item:
            if action == 'checkin':
                if equipment_item['available']:
                    flash(f'{equipment_name} is already available.', 'error')
                else:
                    equipment_item['available'] = True
                    flash(f'{name} successfully checked in {equipment_name}. It is now available.', 'success')
            elif action == 'checkout':
                if not equipment_item['available']:
                    flash(f'{equipment_name} is already unavailable.', 'error')
                else:
                    equipment_item['available'] = False
                    flash(f'{name} successfully checked out {equipment_name}. It is now unavailable.', 'success')
            
            # Save changes to JSON file
            save_equipment_data(equipment_data)
        else:
            flash(f'Equipment {equipment_name} not found.', 'error')

        return redirect(url_for('checkinout'))

    return render_template('checkinout.html')

# Route for Equipment List page
@app.route('/equipment')
def equipment():
    return render_template('equipment.html', equipment_data=equipment_data)

# Route for Tournament Schedule page
@app.route('/tournament')
def tournament():
    return render_template('tournament.html')

if __name__ == '__main__':
    app.run(debug=True)
