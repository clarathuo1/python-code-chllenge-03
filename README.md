# Concert Management System
This project provides a basic Concert Management System that allows for tracking bands, venues, and concerts using raw SQL queries. The schema is designed to manage and retrieve information about musical performances, including relationships between bands and venues.

## Project Structure
### Schema Setup

- bands table: Stores information about bands.
- venues table: Stores information about venues.
- concerts table: Links bands and venues with performance details.
### Python Methods

- Methods to retrieve and manipulate data using raw SQL queries.
## Schema
### Tables
#### bands
- name: TEXT (Primary Key)
- hometown: TEXT
#### venues
- title: TEXT (Primary Key)
- city: TEXT
### concerts
- id: INTEGER (Primary Key, Auto-increment)
- band_name: TEXT (Foreign Key referencing bands.name)
- venue_title: TEXT (Foreign Key referencing venues.title)
- date: TEXT
## Setup Instructions
### 1. Database Creation

First, create the database and tables using SQLite. You can execute the following SQL commands to set up the schema:

sql
Copy code
-- Create the 'bands' table
CREATE TABLE bands (
    name TEXT PRIMARY KEY,
    hometown TEXT
);

-- Create the 'venues' table
CREATE TABLE venues (
    title TEXT PRIMARY KEY,
    city TEXT
);

-- Create the 'concerts' table
CREATE TABLE concerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    band_name TEXT,
    venue_title TEXT,
    date TEXT,
    FOREIGN KEY (band_name) REFERENCES bands(name),
    FOREIGN KEY (venue_title) REFERENCES venues(title)
);
Python Methods

Use the following Python methods to interact with the database. Make sure to have the sqlite3 module available in your environment.

python
Copy code
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('concerts.db')
Methods
Band Methods
get_concerts_for_band(conn, band_name) Retrieves all concerts performed by a specific band.

get_venues_for_band(conn, band_name) Retrieves all venues where the specified band has performed.

Venue Methods
get_concerts_for_venue(conn, venue_title) Retrieves all concerts held at a specific venue.

get_bands_for_venue(conn, venue_title) Retrieves all bands that have performed at a specific venue.

Concert Methods
get_band_for_concert(conn, concert_id) Retrieves the band performing at a specific concert.

get_venue_for_concert(conn, concert_id) Retrieves the venue hosting a specific concert.

is_hometown_show(conn, concert_id) Determines if the concert is in the band's hometown.

get_introduction_for_concert(conn, concert_id) Provides an introduction string for the concert.

Band Aggregations
play_in_venue(conn, band_name, venue_title, date) Creates a new concert record for a band at a specified venue on a given date.

get_all_introductions_for_band(conn, band_name) Retrieves all introductions for a specific band.

get_band_with_most_performances(conn) Identifies the band with the most concerts.

Venue Aggregations
get_concert_on_date(conn, venue_title, date) Retrieves the first concert on a specific date at a venue.

get_most_frequent_band_at_venue(conn, venue_title) Identifies the band that has performed most frequently at a venue.

Example Usage
Here's an example of how to use the methods:

python
Copy code
import sqlite3

# Establish a connection
conn = sqlite3.connect('concerts.db')

# Get all concerts for a specific band
concerts = get_concerts_for_band(conn, 'The Rockers')
print(concerts)

# Check if a concert is in the band's hometown
is_hometown = is_hometown_show(conn, 1)  # Assuming concert_id is 1
print("Is hometown show:", is_hometown)

# Add a new concert
play_in_venue(conn, 'The Rockers', 'Grand Arena', '2024-09-16')

# Get all introductions for a band
introductions = get_all_introductions_for_band(conn, 'The Rockers')
print(introductions)

# Close the connection
conn.close()
Dependencies
Python 3.x
SQLite (comes with Python's standard library)
License
This project is licensed under the MIT License. See the LICENSE file for details.

