import sqlite3
import json
from models import Location


LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]


def get_all_locations():
    """Get all locations"""
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address
        FROM location a
        """)

        # Initialize an empty list to hold all location representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # location class above.
            location = Location(row['id'], row['name'],
                                row['address'])

            locations.append(location.__dict__)

    return locations

def get_single_location(id):
    """Get single location"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address
        FROM location a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an location instance from the current row
        location = Location(data['id'], data['name'],
                            data['address'])

        return location.__dict__



#def get_all_locations():
#    """the squiggles really bugged me"""
#    return LOCATIONS

#def get_single_location(id):
#    """the squiggles really bugged me"""
#    requested_location = None

#    for location in LOCATIONS:
#        if location["id"] == id:
#            requested_location = location

#    return requested_location


def create_location(location):
    """This function is in charge of adding a new location to the list!"""
    # Get the id value of the last location in the list
    max_id = LOCATIONS[-1]["id"]
    new_id = max_id + 1
    location["id"] = new_id
    LOCATIONS.append(location)
    return location


def delete_location(id):
    """This function deletes locations obvi"""
    location_index = -1
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index
    if location_index >= 0:
        LOCATIONS.pop(location_index)


# def update_location(id, new_location):
#     """PUT/replace things!"""
#     for index, location in enumerate(LOCATIONS):
#         if location["id"] == id:
#             LOCATIONS[index] = new_location
#             break


def update_location(id, new_location):
    """Update locations"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE location
            SET
                id = ?,
                name = ?,
                address = ?
        WHERE id = ?
        """, (new_location['id'], new_location['name'], new_location['address']
            ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True