# lib/concert.py
from . import CURSOR, CONN
from bands import Band
from venue import Venue


class Concert:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, id, band_id, venue_id, date, id=None):
        self.id = id
        self.band_id = band_id
        self.venue_id = venue_id
        self.date = date

    def __repr__(self):
        return (
            f"<Concert {self.id}: {self.band_id}, {self.venue_id}, " +
            f"{self.date}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Concert instances """
        sql = """
            CREATE TABLE IF NOT EXISTS concerts (
            id INTEGER PRIMARY KEY,
            band_id INTEGER,
            venue_id INTEGER,
            date TEXT,
            FOREIGN KEY (band_id) REFERENCES bands(id),
            FOREIGN KEY (venue_id) REFERENCES venues(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Concert instances """
        sql = """
            DROP TABLE IF EXISTS concerts;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the band_id, venue_id, and date values of the current Concert object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO concerts (band_id, venue_id, date)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.band_id, self.venue_id, self.date))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Concert instance."""
        sql = """
            UPDATE concerts
            SET band_id = ?, venue_id = ?, date = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.band_id, self.venue_id, self.date, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Concert instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM concerts
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, band_id, venue_id, date):
        """ Initialize a new Concert instance and save the object to the database """
        concert = cls(None, band_id, venue_id, date)
        concert.save()
        return concert

    @classmethod
    def instance_from_db(cls, row):
        """Return a Concert object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        concert = cls.all.get(row[0])
        if concert:
            # ensure attributes match row values in case local instance was modified
            concert.band_id = row[1]
            concert.venue_id = row[2]
            concert.date = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            concert = cls(row[0], row[1], row[2], row[3])
            cls.all[concert.id] = concert
        return concert

    @classmethod
    def get_all(cls):
        """Return a list containing one Concert object per table row"""
        sql = """
            SELECT *
            FROM concerts
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Concert object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM concerts
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def band(self):
        """Return the band associated with the current concert"""
        from bands import Band
        sql = """
            SELECT * FROM bands
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.band_id,),)

        row = CURSOR.fetchone()
        return Band.instance_from_db(row) if row else None

    def venue(self):
        """Return the venue associated with the current concert"""
        from venue import Venue
        sql = """
            SELECT * FROM venues
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.venue_id,),)

        row = CURSOR.fetchone()
        return Venue.instance_from_db(row) if row else None

    def hometown_show(self):
        """Return true if the concert is in the band's hometown, false if it is not"""
        band = self.band()
        venue = self.venue()
        return band.genre = venue.location

    def introduction(self):
        """Return a string with the band's introduction for this concert"""
        band = self.band()
        venue = self.venue()
        return f"Hello {venue.city}!!!!! We are {band.name} and i am a {band.genre}"