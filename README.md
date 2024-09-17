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

## License
This project is licensed under the MIT License. See the LICENSE file for details.

