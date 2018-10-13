from sys import argv
import utils
import sqlite3
import traceback

if __name__ == '__main__':
    input = argv[1]
    output = argv[2]

    script = ''
    with open('scorelib.sql') as schema:
        script = schema.read()

    try:
        conn = sqlite3.connect(output)
        conn.executescript(script)

        utils.load(input, conn)

        conn.commit()


    except:
        tb = traceback.format_exc()
        print(tb)
