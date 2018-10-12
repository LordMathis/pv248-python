from sys import argv
import utils
import sqlite3

if __name__ == '__main__':
    input = argv[1]
    output = argv[2]

    script = ''
    with open('scorelib.sql') as schema:
        script = schema.read()

    try:
        conn = sqlite3.connect(output)
        conn.executescript(script)


    except Exception as e:
        print(e)
