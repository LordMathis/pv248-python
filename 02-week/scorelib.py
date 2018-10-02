import re

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


def get_composers(composers):
    composers = composers.split(';')
    results = []

    for composer in composers:
        name = re.sub('\(.*\)', "", composer).strip()

        born, died = None, None

        match = re.search(born_regex, composer)
        if match:
            born = match.group(0)

        match = re.search(died_regex, composer)
        if match:
            died = match.group(0)

        results.append(Person(name, born, died))
    return results

def get_year(line):
    match = re.search(year_regex, line)
    if match:
        return match.group(0)
    return None

def get_editors(line):
    results = []

    editors = line.split(',')

    if len(editors) < 2:
        names = editors
    else:
        names = []
        for i in range(0, len(editors), 2):
            names.append(editors[i] + ',' + editors[i+1])

    for name in names:
        results.append(Person(name.strip()))

    return results

def get_voice(line):
    match = re.search(range_regex, line)
    voice_range, name = None, None
    if match:
        voice_range = match.group(0)
        name = re.sub(range_str, "", line)
    else:
        name = line

    return Voice(name.strip(), voice_range)


def load(filename):
    prints = []
    with open(filename, 'r') as ins:
        lines = []
        for line in ins:
            line = line.strip()
            if line:
                lines.append(line)
            else:
                new_print = process_print(lines)
                if new_print:
                    prints.append(new_print)
                lines = []

        new_print = process_print(lines)
        if new_print:
            prints.append(new_print)

    prints.sort(key=lambda x: x.print_id)
    return prints


def process_print(lines):

    if not lines:
        return None

    print_id, composition_name, genre, key, year, edition_name, incipit = [None]*7
    authors, editors, voices = [], [], []
    partiture = False

    for line in lines:
        key_val = line.split(':')

        if key_val[0] == 'Print Number':
            print_id = int(key_val[1].strip())

        elif key_val[0] == 'Composer':
            authors = get_composers(key_val[1].strip())

        elif key_val[0] == 'Title':
            composition_name = key_val[1].strip()
            if not composition_name:
                composition_name = None

        elif key_val[0] == 'Genre':
            genre = key_val[1].strip()
            if not genre:
                genre = None

        elif key_val[0] == 'Key':
            key = key_val[1].strip()
            if not key:
                key = None

        elif key_val[0] == 'Composition Year':
            year = get_year(key_val[1].strip())
            if not year:
                year = None

        elif key_val[0] == 'Publication Year':
            pass

        elif key_val[0] == 'Edition':
            edition_name = key_val[1].strip()
            if not edition_name:
                edition_name = None

        elif key_val[0] == 'Editor':
            editors = get_editors(key_val[1].strip())

        elif 'Voice' in key_val[0]:
            voices.append(get_voice(key_val[1].strip()))

        elif key_val[0] == 'Partiture':
            if 'yes' in key_val[1]:
                partiture = True
            partiture = False

        elif key_val[0] == 'Incipit':
            incipit = key_val[1].strip()
            if not incipit:
                incipit = None

    composition = Composition(composition_name, incipit, key, genre, year, voices, authors)
    edition = Edition(composition, editors, edition_name)
    return Print(edition, print_id, partiture)

range_str = '(\S+)--(\S+)'
range_regex = re.compile(range_str)
born_regex = re.compile('\(\d\d\d\d--')
died_regex = re.compile('--\d\d\d\d\)')
year_regex = re.compile('\d\d\d\d')
partiture_regex = re.compile('yes')
