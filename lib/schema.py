import sqlite3

# Connect to the database
conn = sqlite3.connect("concerts.db")
cursor = conn.cursor()

# Create some sample bands
cursor.execute("INSERT INTO bands (name, hometown) VALUES ('Band 1', 'City 1'), ('Band 2', 'City 2'), ('Band 3', 'City 3')")
conn.commit()

# Create some sample venues
cursor.execute("INSERT INTO venues (title, city) VALUES ('Venue 1', 'City 1'), ('Venue 2', 'City 2'), ('Venue 3', 'City 3')")
conn.commit()

# Create some sample concerts
cursor.execute("INSERT INTO concerts (date, band_id, venue_id) VALUES ('2022-01-01', 1, 1), ('2022-01-02', 1, 2), ('2022-01-03', 2, 1), ('2022-01-04', 2, 3), ('2022-01-05', 3, 2)")
conn.commit()

# Close the database connection
conn.close()