from sys import argv
import sqlite3
import traceback

db = '../03-exercise/scorelib.dat'


def get_composers(search_string, conn):
    cur = conn.cursor()

    cur.execute('''SELECT id, name FROM person WHERE name like ?''',
                (search_string,))

    return cur.fetchall()


def get_scores(id, conn):
    cur = conn.cursor()

    cur.execute('''SELECT score.* FROM score_author NATURAL JOIN score
                   WHERE score_author.composer = ?''', (id,))

    return cur.fetchall()


def get_voices(score_id, conn):
    cur = conn.cursor()

    cur.execute('''SELECT * FROM voice WHERE score = ?''', (score_id,))

    return cur.fetchall()

def get_edition(score_id, conn):
    cur = conn.cursor()
    print(score_id)

    cur.execute('''SELECT edition.id, edition.name, person.name FROM
                   edition NATURAL LEFT JOIN
                   (edition_author NATURAL JOIN person)
                   WHERE score = ?''', (score_id,))

    return cur.fetchone()

def get_print(edition_id, conn):
    cur = conn.cursor()

    cur.execute('''SELECT * FROM print WHERE edition = ?''', (edition_id,))

    return cur.fetchall()

if __name__ == '__main__':

    name = '%' + argv[1] + '%'

    try:
        conn = sqlite3.connect(db)
        print(get_composers(name, conn))

        for composer_id, composer_name in get_composers(name, conn):
            print()
            print(composer_id, composer_name)
            for score in get_scores(composer_id, conn):
                print("Score:", score)
                print("Voice:", get_voices(score[0], conn))
                edition = get_edition(score[0], conn)
                print("Edition:", edition)
                print("Print:", get_print(edition[0], conn))


        conn.commit()

    except:
        tb = traceback.format_exc()
        print(tb)
