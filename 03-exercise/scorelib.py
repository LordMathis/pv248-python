class DBItem:
    def store(self):
        raise NotImplementedError("Store method not implemented")

class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def composition(self):
        return self.edition.composition

class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition
        self.authors = authors
        self.name = name


class Composition:
    def __init__(self, name, incipit, key, genre, year, voices, authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors

class Voice:
    def __init__(self, name, range):
        self.name = name
        self.range = range

class Person:
    def __init__(self, conn, name, born=None, died=None):
        self.name = name
        self.born = born
        self.died = died

        self.store(conn)

    def store(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM person WHERE name = (?)", (self.name,))
        row = cur.fetchall()
        print(row)

        if len(row) == 0:
            cur.execute("INSERT INTO person (name, born, died) VALUES (?, ?, ?)",
                         (self.name, self.born, self.died))
        elif len(row) == 1:
            id = row[0][0]
            born = row[0][1]
            died = row[0][2]

            new_born = born
            new_died = died

            if born is None and self.born is not None:
                new_born = self.born

            if died is None and self.died is not None:
                new_died = self.died

            cur.execute("UPDATE person SET born = ?, died = ? WHERE id = ?",
                        (born, died, id))

        else:
            print("Excuse me, wtf?")
