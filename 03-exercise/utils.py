import re
from scorelib import Print, Edition, Composition, Voice, Person

range_str = '(\S+)--(\S+)'
range_regex = re.compile(range_str)
born_regex = re.compile('\((\d\d\d\d)--')
died_regex = re.compile('--(\d\d\d\d)\)')
year_regex = re.compile('\d\d\d\d')
voice_regex = re.compile('\d+')
partiture_regex = re.compile('yes')

def get_composers(composers, conn):
    composers = composers.split(';')
    results = []

    for composer in composers:
        name = re.sub('\(.*\)', "", composer).strip()

        born, died = None, None

        match = re.search(born_regex, composer)
        if match:
            born = match.group(1)

        match = re.search(died_regex, composer)
        if match:
            died = match.group(1)

        p = Person(name, born, died)
        id = p.store(conn)
        if id:
            results.append(id)
    return results

def get_year(line):
    match = re.search(year_regex, line)
    if match:
        return match.group(0)
    return None

def get_editors(line, conn):
    results = []

    editors = line.split(',')

    if len(editors) < 2:
        names = editors
    else:
        names = []
        for i in range(0, len(editors), 2):
            names.append(editors[i] + ',' + editors[i+1])

    for name in names:
        p = Person(name.strip())
        id = p.store(conn)
        if id:
            results.append(id)

    return results

def get_voice(line, voice_num):
    match = re.search(range_regex, line)
    voice_range, name = None, None
    if match:
        voice_range = match.group(0)
        name = re.sub(range_str, "", line)
    else:
        name = line

    if (name.strip() == '') and (not voice_range):
        return None

    return Voice(name.strip(), voice_range, voice_num)


def load(filename, conn):
    prints = []
    with open(filename, 'r') as ins:
        lines = []
        for line in ins:
            line = line.strip()
            if line:
                lines.append(line)
            else:
                new_print = process_print(lines, conn)
                if new_print:
                    prints.append(new_print)
                lines = []

        process_print(lines, conn)


def process_print(lines, conn):

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
            authors = get_composers(key_val[1].strip(), conn)

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
            editors = get_editors(key_val[1].strip(), conn)

        elif 'Voice' in key_val[0]:
            voice_num = 1
            match = re.search(voice_regex, key_val[0])
            if match:
                voice_num = match.group(0)
            new_voice = get_voice(key_val[1].strip(), int(voice_num))
            if new_voice:
                voices.append(new_voice)

        elif key_val[0] == 'Partiture':
            if 'yes' in key_val[1]:
                partiture = True

        elif key_val[0] == 'Incipit':
            incipit = key_val[1].strip()
            if not incipit:
                incipit = None

    composition = Composition(composition_name, incipit, key, genre, year, voices, authors)
    comp_id = composition.store(conn)
    edition = Edition(composition, editors, edition_name)
    edition_id = edition.store(conn, comp_id)
    p = Print(edition, print_id, partiture)
    p.store(conn, edition_id)
