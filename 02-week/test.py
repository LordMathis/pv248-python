from sys import argv
from scorelib import Print, Edition, Composition, Voice, Person
import re

def get_composers(composers):
    composers = composers.split(';')
    results = []

    for composer in composers:
        name = re.sub('\(.*\)', "", composer)

        born, died = None
        match = re.search(year_regex, composer)
        if match:
            born = match.group(0)
            died = match.group(1)

        results.append(Person(name, born, died))

def get_year(line):
    match = re.search(year_regex, line)
    if match:
        return match.group(0)
    return None

def get_editors(line):
    results = []
    editors = line.split(',')
    names = [",".join(editors[i:i+span]) for i in range(0, len(words), 2)]
    for name in names:
        results.append(Person(name))

def get_voice(line):
    match = re.search(range_regex, line)
    range, name = None
    if match:
        range = match.group(0)
        name = re.sub(range, "", line)
    else:
        name = line

    return Voice(name, range)


def load(filename):
    prints = []
    with open(filename, 'r') as ins:
        lines = []
        for line in ins:
            if line:
                lines.append(line)
            else:
                prints.append(process_print(lines))
                lines = []
    return prints

def process_print(lines):

    print_id, composition_name, genre, key, year, edition_name, incipit = None
    authors, editors, voices = []
    partiture = False

    for line in lines:
        key_val = line.split(':')

        if key_val[0] == 'Print Number':
            print_id = int(key_val[1].strip())

        elif key_val[0] == 'Composer':
            authors = get_composers(key_val[1].strip())

        elif key_val[0] == 'Title':
            composition_name = key_val[1].strip()

        elif key_val[0] == 'Genre':
            genre = key_val[1].strip()

        elif key_val[0] == 'Key':
            key = key_val[1].strip()

        elif key_val[0] == 'Composition Year':
            year = get_year(key_val[1].strip())

        elif key_val[0] == 'Publication Year':
            pass

        elif key_val[0] == 'Edition':
            edition_name = key_val[1].strip()

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

    composition = Composition(composition_name, incipit, key, genre, year, voices, authors)
    edition = Edition(composition, editors, edition_name)
    return Print(edition, print_id, partiture)

range = '(\S+)--(\S+)'
range_regex = re.compile(range)
year_regex = re.compile('\d\d\d\d')
partiture_regex = re.compile('yes')

if __name__ == '__main__':
    filename = argv[1]
    prints = load(filename)
    print(prints)
    for p in prints:
        p.format()
