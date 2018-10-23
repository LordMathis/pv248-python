from sys import argv
import sqlite3
import traceback
import json

db = './scorelib.dat'


def get_matching_composers(search_string, conn):
    cur = conn.cursor()

    cur.execute('''SELECT id, name FROM person WHERE name like ?''',
                (search_string,))

    return cur.fetchall()


def get_scores(id, conn):
    cur = conn.cursor()

    cur.execute('''SELECT score.* FROM score_author JOIN score
                   on score_author.score = score.id
                   WHERE score_author.composer = ?''', (id,))

    return cur.fetchall()

def get_all_composers(score_id, conn):
    cur = conn.cursor()

    cur.execute('''SELECT person.* FROM person JOIN score_author
                   on score_author.composer = person.id
                   WHERE score_author.score = ?''', (score_id,))

    composers = cur.fetchall()

    res = []
    for composer in composers:
        cp_born, cp_died, cp_name = composer[1:4]
        if cp_name or cp_born or cp_died:
            res.append({
                "name": cp_name,
                "born": cp_born,
                "died": cp_died
            })
    return res

def get_voices(score_id, conn):
    cur = conn.cursor()

    cur.execute('''SELECT * FROM voice WHERE score = ?''', (score_id,))

    voices = {}
    for voice in cur.fetchall():
        number = voice[1]
        range = voice[3]
        name = voice[4]
        voices[number] = {
            "range": range,
            "name": name
        }
    return voices

def get_edition(score_id, conn):
    cur = conn.cursor()

    cur.execute('''SELECT edition.id, edition.name,
                   person.name, person.born, person.died FROM
                   edition LEFT JOIN
                   (edition_author JOIN person
                   on edition_author.editor = person.id)
                   on edition_author.edition = edition.id
                   WHERE score = ?''', (score_id,))

    rows = cur.fetchall()
    edition_id = rows[0][0]
    edition_name = rows[0][1]
    editors = []

    for editor in rows:
        ed_name, ed_born, ed_died = editor[2:5]
        if ed_name or ed_born or ed_died:
            editors.append({
                "name": ed_name,
                "born": ed_born,
                "died": ed_died
            })
    return (edition_id, edition_name, editors)

def get_print(edition_id, conn):
    cur = conn.cursor()

    cur.execute('''SELECT * FROM print WHERE edition = ?''', (edition_id,))

    return cur.fetchall()


if __name__ == '__main__':

    name = '%' + argv[1] + '%'

    try:
        conn = sqlite3.connect(db)

        all_data = {}

        for composer_id, composer_name in get_matching_composers(name, conn):

            composer_data = []

            for score in get_scores(composer_id, conn):

                score_id = score[0]

                voices =  get_voices(score_id, conn)
                edition_id, edition_name, editors = get_edition(score_id, conn)
                print_data = get_print(edition_id, conn)
                all_composers = get_all_composers(score_id, conn)

                for print_item in print_data:

                    print_object = {
                        "Print Number": print_item[0],
                        "Composer": all_composers,
                        "Title": score[1],
                        "Genre": score[2],
                        "Key": score[3],
                        "Incipit": score[4],
                        "Composition Year": score[5],
                        "Voices": voices,
                        "Edition": edition_name,
                        "Editor": editors,
                        "Partiture": True if print_item[1] == 'Y' else False
                    }

                    composer_data.append(print_object)

            all_data[composer_name] = composer_data

        print(json.dumps(all_data, indent=4, sort_keys=False, ensure_ascii=False))

        conn.commit()

    except:
        tb = traceback.format_exc()
        print(tb)
