# lib/band.py
from . import CURSOR, CONN
from venue import Venue
from concerts import Concert

class Band:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, id, name, hometown, genre=None):
        self.id = id
        self.name = name
        self.hometown = hometown
        self.genre = genre

    def __repr__(self):
        return (
            f"<Band {self.id}: {self.name}, {self.hometown}, {self.genre}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Band instances """
        sql = """
            CREATE TABLE IF NOT EXISTS bands (
            id INTEGER PRIMARY KEY,
            name TEXT,
            hometown TEXT,
            genre TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Band instances """
        sql = """
            DROP TABLE IF EXISTS bands;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name, hometown, and genre values of the current Band object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO bands (name, hometown, genre)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.hometown, self.genre))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Band instance."""
        sql = """
            UPDATE bands
            SET name = ?, hometown = ?, genre = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.hometown, self.genre, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Band instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM bands
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, name, hometown, genre=None):
        """ Initialize a new Band instance and save the object to the database """
        band = cls(None, name, hometown, genre)
        band.save()
        return band

    @classmethod
    def instance_from_db(cls, row):
        """Return a Band object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        band = cls.all.get(row[0])
        if band:
            # ensure attributes match row values in case local instance was modified
            band.name = row[1]
            band.hometown = row[2]
            band.genre = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            band = cls(row[0], row[1], row[2], row[3])
            cls.all[band.id] = band
        return band

    @classmethod
    def get_all(cls):
        """Return a list containing one Band object per table row"""
        sql = """
            SELECT *
            FROM bands
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Band object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM bands
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return Band object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM bands
            WHERE name = ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def concerts(self):
        """Return list of concerts associated with current band"""
        from concert import Concert
        sql = """
            SELECT * FROM concerts
            WHERE band_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Concert.instance_from_db(row) for row in rows
        ]

    def venues(self):
        """Return list of venues associated with current band"""
        from concert import Concert
        from venue import Venue
        sql = """
            SELECT * FROM concerts
            WHERE band_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        concert_ids = [row[0] for row in rows]
        venues = []
        for concert_id in concert_ids:
            concert = Concert.find_by_id(concert_id)
            venue = concert.venue()
            venues.append(venue)
        return venues

    def play_in_venue(self, venue_title, date):
        venue = Venue.find_by_name(venue_title)
        if venue:
            concert = Concert.create(self.id, venue.id, date)
            return concert
        else:
            raise ValueError("Venue not found")

    def all_introductions(self):
        introductions = []
        for concert in self.concerts():
            venue = concert.venue()
            introduction = f"Hello {venue.city}!!!!! We are {self.name} and we're from {self.hometown} and we play {self.genre}"
            introductions.append(introduction)
        return introductions

    @staticmethod
    def most_performances():
        sql = """
            SELECT band_id, COUNT(*) as count
            FROM concerts
            GROUP BY band_id
            ORDER BY count DESC
        """
        rows = CURSOR.execute(sql).fetchall()
        max_count = max(row[1] for row in rows)
        most_performing_bands = [Band.find_by_id(row[0]) for row in rows if row[1] == max_count]
        return most_performing_bands