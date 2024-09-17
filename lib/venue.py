# lib/venue.py
from  __init__ import CURSOR, CONN
from concerts import Concert


class Venue:

    # Dictionary of objects saved to the database.
    all = {}

    def _init_(self, id, name, city, id=None):
        self.id = id
        self.name = name
        self.city = city

    def _repr_(self):
        return (
            f"<Venue {self.id}: {self.name}, {self.city}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Venue instances """
        sql = """
            CREATE TABLE IF NOT EXISTS venues (
            id INTEGER PRIMARY KEY,
            name TEXT,
            city TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Venue instances """
        sql = """
            DROP TABLE IF EXISTS venues;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and city values of the current Venue object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO venues (name, city)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.city))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Venue instance."""
        sql = """
            UPDATE venues
            SET name = ?, city = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.city, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Venue instance,
        delete the dictionary entry, and reassign id attribute"""

        sql = """
            DELETE FROM venues
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]

        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, name, city):
        """ Initialize a new Venue instance and save the object to the database """
        venue = cls(name, city)
        venue.save()
        return venue

    @classmethod
    def instance_from_db(cls, row):
        """Return a Venue object having the attribute values from the table row."""

        # Check the dictionary for  existing instance using the row's primary key
        venue = cls.all.get(row[0])
        if venue:
            # ensure attributes match row values in case local instance was modified
            venue.name = row[1]
            venue.city = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            venue = cls(row[1], row[2])
            venue.id = row[0]
            cls.all[venue.id] = venue
        return venue

    @classmethod
    def get_all(cls):
        """Return a list containing one Venue object per table row"""
        sql = """
            SELECT *
            FROM venues
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Venue object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM venues
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return Venue object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM venues
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def concerts(self):
        """Return list of concerts associated with current venue"""
        from concerts import Concert
        sql = """
            SELECT * FROM concerts
            WHERE venue_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Concert.instance_from_db(row) for row in rows
        ]

    def bands(self):
        """Return list of bands associated with current venue"""
        from concerts import Concert
        from bands import Band
        sql = """
            SELECT * FROM concerts
            WHERE venue_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        concert_ids = [row[0] for row in rows]
        bands = []
        for concert_id in concert_ids:
            concerts = Concert.find_by_id(concert_id)
            band = concerts.band()
            bands.append(band)
        return bands

    def concert_on(self, date):
        """Return the first concert on the specified date at the venue"""
        from concerts import Concert
        sql = """
            SELECT * FROM concerts
            WHERE venue_id = ? AND date = ?
        """
        CURSOR.execute(sql, (self.id, date),)

        row = CURSOR.fetchone()
        return Concert.instance_from_db(row) if row else None

    def most_frequent_band(self):
        """Return the band that has performed the most at the venue"""
        from bands import Band
        sql = """
            SELECT band_id, COUNT(*) as count
            FROM concerts
            WHERE venue_id = ?
            GROUP BY band_id
            ORDER BY count DESC
            LIMIT 1
        """
        row = CURSOR.execute(sql, (self.id,)).fetchone()
        band_id = row[0]
        return Band.find_by_id(band_id)