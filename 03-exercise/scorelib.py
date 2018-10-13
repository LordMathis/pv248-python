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

    def do_store(self, conn):
        cur = conn.cursor()
        cur.execute('''INSERT INTO score (name, genre, key, incipit)
                    VALUES (?, ?, ?, ?) ''',
                    (self.name, self.genre, self.key, self.incipit))
        id = cur.lastrowid

        for voice in self.voices:
            voice.store(conn, id)

        return id

    def store(self, conn):
        cur = conn.cursor()

        cur.execute('''SELECT * FROM score WHERE name = ?
                    AND genre = ? AND key = ? AND incipit = ?''',
                    ((self.name, self.genre, self.key, self.incipit)))
        rows = cur.fetchall()
        if len(rows) == 0:
            return self.do_store(conn)

        else:
            for row in rows:
                ref_id = row[0]

                cur = conn.cursor()
                cur.execute('''SELECT * FROM voice WHERE score = ?''', (ref_id,))
                voices = cur.fetchall()

                found_all = True
                for voice in voices:
                    found = False
                    for self_voice in self.voices:
                        if (voice[1] == self_voice.number and
                           voice[3] == self_voice.range and
                           voice[4] == self_voice.name):

                           found = True
                    if not found:
                        found_all = False
                        break

                if found_all:
                    return ref_id
                else:
                    return self.do_store(conn)

class Voice:
    def __init__(self, name, range, number):
        self.name = name
        self.range = range
        self.number = number

    def store(self, conn, ref_id):
        cur = conn.cursor()

        cur.execute("INSERT INTO voice (score, number, range, name) VALUES (?, ?, ?, ?)",
                    (ref_id, self.number, self.name, self.range))

class Person:
    def __init__(self, name, born=None, died=None):
        self.name = name
        self.born = born
        self.died = died

    def store(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM person WHERE name = (?)", (self.name,))
        row = cur.fetchall()

        if len(row) == 0:
            cur.execute("INSERT INTO person (name, born, died) VALUES (?, ?, ?)",
                         (self.name, self.born, self.died))
            return cur.lastrowid
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
            return id

        else:
            print("Excuse me, wtf?")
