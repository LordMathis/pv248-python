class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def composition(self):
        return self.edition.composition

    def store(self, conn, edition_id):
        cur = conn.cursor()

        partiture = 'Y' if self.partiture else 'N'
        cur.execute('''INSERT INTO print (id, partiture, edition) VALUES (?, ?, ?)''',
                    (self.print_id, partiture, edition_id))

class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition
        self.authors = authors
        self.name = name

    def store(self, conn, score_id):
        cur = conn.cursor()

        cur.execute('''INSERT INTO edition (score, name, year) VALUES (?, ?, ?)''',
                    (score_id, self.name, None))
        edition_id = cur.lastrowid

        for author_id in self.authors:
            cur = conn.cursor()
            cur.execute('''INSERT INTO edition_author (edition, editor) VALUES (?, ?)''',
                        (edition_id, author_id))

        return edition_id

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

        for author_id in self.authors:

            cur = conn.cursor()
            cur.execute('''INSERT INTO score_author (score, composer) VALUES (?, ?)''',
                        (id, author_id))


        return id

    def check_voices(self, conn, rows):
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

        return None

    def check_authors(self, conn, rows):
        for row in rows:
            ref_id = row[0]

            cur = conn.cursor()
            cur.execute('''SELECT * FROM score_author WHERE score = ?''', (ref_id,))
            score_authors = cur.fetchall()

            found_all = True
            for score_author in score_authors:
                cur = conn.cursor()
                cur.execute('''SELECT * FROM person WHERE id = ?''', (score_author[2]))
                author = cur.fetchone()

                found = False
                for self_author in self.authors:
                    if (author[1] == self_author.born and
                        authors[2] == self_author.died and
                        authors[3] == self_author.name) :

                        found = True

                if not found:
                    found_all = False
                    break

            if found_all:
                return ref_id

        return None

    def store(self, conn):
        cur = conn.cursor()

        cur.execute('''SELECT * FROM score WHERE name = ?
                    AND genre = ? AND key = ? AND incipit = ?''',
                    ((self.name, self.genre, self.key, self.incipit)))
        rows = cur.fetchall()
        if len(rows) == 0:
            return self.do_store(conn)

        else:
            voice_id = self.check_voices(conn, rows)
            author_id = self.check_authors(conn, rows)

            if voice_id == author_id:
                return voice_id

            else:
                self.do_store(conn)

class Voice:
    def __init__(self, name, range, number):
        self.name = name
        self.range = range
        self.number = number

    def store(self, conn, ref_id):
        cur = conn.cursor()

        cur.execute("INSERT INTO voice (score, number, range, name) VALUES (?, ?, ?, ?)",
                    (ref_id, self.number, self.range, self.name))

class Person:
    def __init__(self, name, born=None, died=None):
        self.name = name
        self.born = born
        self.died = died

    def store(self, conn):
        cur = conn.cursor()
        cur.execute("SELECT * FROM person WHERE name = (?)", (self.name,))
        row = cur.fetchall()

        if 'Bach, Johann Sebastian' in self.name:
            print(self.born, self.died, self.name)
            print(row)
            print('\n')

        if len(row) == 0:
            cur.execute("INSERT INTO person (name, born, died) VALUES (?, ?, ?)",
                         (self.name, self.born, self.died))
            return cur.lastrowid
        else:
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
                        (new_born, new_died, id))
            return id
