# ------------
# Import / Set up

import sqlite3

conn = sqlite3.connect("user_data.db")
c = conn.cursor()

# ----------
# Queries


c.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, username TEXT, password TEXT)")

c.execute("INSERT INTO users VALUES (1, 'generic-duck', 'TG23{remember_to_vaccinate_kids}')")
c.execute("INSERT INTO users VALUES (2, 'b-dev', 'beagleboys!?AS')")
c.execute("INSERT INTO users VALUES (3, 'hogwilde', 'mayorpiggywiggy1976?')")

# Create a things table
c.execute('''CREATE TABLE IF NOT EXISTS user_information(user_id INTEGER, adress TEXT, gym_membership TEXT, library_card TEXT, flag TEXT, username TEXT)''')

# Add some example users and things to the database
c.execute("INSERT INTO user_information (user_id, adress, gym_membership, library_card, flag, username) VALUES (1, 'N/A', 'Nei', 'Nei', 'Nei', 'Generic Duck')")
c.execute("INSERT INTO user_information (user_id, adress, gym_membership, library_card, flag, username) VALUES (2, 'Grotta', 'Nei', 'Ja', 'Nei', 'B-dev')")
c.execute("INSERT INTO user_information (user_id, adress, gym_membership, library_card, flag, username) VALUES (3, 'Mansion Avenue', 'Ja', 'Ja', 'TG23{hogwilde_hogging_the_flagg}', 'Mayor Hogwilde')")



"""
c.execute("INSERT INTO users VALUES (1, 'generic-duck', 'password1')")
c.execute("INSERT INTO users VALUES (2, 'b-dev', 'beagleboys')")
c.execute("INSERT INTO users VALUES (3, 'hogwilde', 'mayorpig')")
"""

conn.commit()