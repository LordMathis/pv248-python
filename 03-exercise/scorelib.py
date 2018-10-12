class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture

    def format(self):

        comp = self.composition()

        composers = []
        for author in comp.authors:
            if author.born or author.died:
                born = author.born if author.born else ""
                died = author.died if author.died else ""
                composers.append(author.name + " (" + born + "--" + died + ")")
            else:
                composers.append(author.name)
        composers_str = "; ".join(composers)

        editors = ", ".join(a.name for a in self.edition.authors)

        print("Print Number: %s" % (str(self.print_id)))
        print("Composer: %s" % composers_str)
        print("Title: %s" % (comp.name if comp.name else ""))
        print("Genre: %s" % (comp.genre if comp.genre else ""))
        print("Key: %s" % (comp.key if comp.key else ""))
        print("Composition Year: %s" % (comp.year if comp.year else ""))
        print("Edition: %s" % (self.edition.name if self.edition.name else ""))
        print("Editor: %s" % editors)
        for i, voice in enumerate(comp.voices):
            if voice.range:
                print("Voice %d: %s %s" % (i+1, voice.name, voice.range))
            else:
                print("Voice %d: %s" % (i, voice.name))
        print("Partiture: %s" % ("yes" if self.partiture else "no"))
        print("Incipit: %s" % (comp.incipit if comp.incipit else ""))






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
    def __init__(self, name, born=None, died=None):
        self.name = name
        self.born = born
        self.died = died
