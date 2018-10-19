from sys import argv
import sqlite3
import traceback
import json

db = './scorelib.dat'


def get_score_id(conn, print_id):
    cur = conn.cursor()

    cur.execute('''SELECT edition.score FROM print JOIN edition
                   on print.edition = edition.id
                   WHERE print.id = ?''', (print_id,))

    return cur.fetchone()[0]


def get_composers(conn, score_id):
    cur = conn.cursor()

    cur.execute('''SELECT person.* FROM person JOIN score_author
                   on person.id = score_author.composer
                   WHERE score_author.score = ?''', (score_id,))

    return cur.fetchall()


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

        score_id = get_score_id(conn, print_num)
        composers_data = []

        composers = get_composers(conn, score_id)
        if composers:
            for composer in composers:
                composers_data.append(format_composer(composer))

        print(json.dumps(composers_data, indent=4, sort_keys=False, ensure_ascii=False))

        conn.commit()


    except:
        tb = traceback.format_exc()
        print(tb)
