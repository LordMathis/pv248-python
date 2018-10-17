from sys import argv
import sqlite3
import traceback

db = './scorelib.dat'


def get_person_id(conn):
    cur = conn.cursor()

    cur.execute('''SELECT edition_author.id FROM print NATURAL JOIN edition
                   INNER JOIN edition_author
                   on edition.id = edition_author.edition
                   WHERE print.id = ?''', (print_num,))

    rows = cur.fetchall()
    results = []

    for row in rows:
        results.append(row[0])

    return results


def get_composer(conn, id):
    cur = conn.cursor()

    cur.execute('''SELECT * FROM person WHERE id = ?''', (id,))
    return cur.fetchone()


def format_composer(composer):

    return {
        "name": composer[3],
        "born": composer[1],
        "died": composer[2]
    }


if __name__ == '__main__':

    print_num = int(argv[1])

    try:
        conn = sqlite3.connect(db)

        composer_ids = get_person_id(conn)
        composers = []

        for composer_id in composer_ids:

            composer = get_composer(conn, composer_id)
            composers.append(format_composer(composer))

        conn.commit()

        print(composers)


    except:
        tb = traceback.format_exc()
        print(tb)
