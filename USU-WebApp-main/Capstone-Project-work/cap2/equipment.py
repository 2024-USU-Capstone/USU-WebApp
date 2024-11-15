
# Path to the equipment data file
import json


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
    {'id': 1,'name': 'Assassins Creed IV Black Flag', 'console': 'Xbox', 'available': True},
    {'id': 2,'name': 'Battlefield 1', 'console': 'Xbox', 'available': True},
    {'id': 3,'name': 'Battlefield 4', 'console': 'Xbox', 'available': True},
    {'id': 4,'name': 'Call of Duty Ghosts', 'console': 'Xbox', 'available': False},
    {'id': 5,'name': 'Call of Duty Modern Warfare', 'console': 'Xbox', 'available': True},
    {'id': 6,'name': 'Call of Duty Vanguard', 'console': 'Xbox', 'available': True},
    {'id': 7,'name': 'Call of Duty WW1', 'console': 'Xbox', 'available': True},
    {'id': 8,'name': 'Dead Rising 3', 'console': 'Xbox', 'available': True},
    {'id': 9,'name': 'Destiny 2', 'console': 'Xbox', 'available': False},
    {'id': 10,'name': 'FIFA 22', 'console': 'Xbox', 'available': True},
    {'id': 11,'name': 'Forza Motorsport 5', 'console': 'Xbox', 'available': True},
    {'id': 12,'name': 'Halo 5', 'console': 'Xbox', 'available': False},
    {'id': 13,'name': 'Halo Reach', 'console': 'Xbox', 'available': True},
    {'id': 14,'name': 'Halo Master Chief Collection', 'console': 'Xbox', 'available': True},
    {'id': 15,'name': 'Halo Infinite', 'console': 'Xbox', 'available': True},
    {'id': 16,'name': 'Injustice 2', 'console': 'Xbox', 'available': False},
    {'id': 17,'name': 'Madden NFL 22', 'console': 'Xbox', 'available': True},
    {'id': 18,'name': 'Minecraft', 'console': 'Xbox', 'available': True},
    {'id': 19,'name': 'Mortal Kombat 11', 'console': 'Xbox', 'available': True},
    {'id': 20,'name': 'Mortal Kombat XL', 'console': 'Xbox', 'available': True},
    {'id': 21,'name': 'Naruto Shippuden: Ultimate Ninja Storm 4 ROAD TO BORUTO', 'console': 'Xbox', 'available': True},
    {'id': 22,'name': 'NBA 2K22', 'console': 'Xbox', 'available': False},
    {'id': 23,'name': 'Overwatch Origins Edition', 'console': 'Xbox', 'available': True},
    {'id': 24, 'name': 'Rocket League', 'console': 'Xbox', 'available': True},
    {'id': 25,'name': 'Tekken 7', 'console': 'Xbox', 'available': True},
    {'id': 26,'name': 'Tom Clancy\'s Rainbow 6 Siege', 'console': 'Xbox', 'available': False} ]
'''
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


'''