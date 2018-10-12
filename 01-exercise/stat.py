import sys
import re
from collections import Counter

def year_to_century(year):
    century = year // 100
    if year % 100 > 0:
        century += 1
    return str(century)

def print_results(results):
    for key in results:
        print("%s: %s" % (key, results[key]))

def process_composers(composer_line):
    line = re.sub('\(.*\)', "", composer_line)
    comps = line.split(';')
    results = []
    for comp in comps:
        comp = comp.strip()
        if not comp:
            continue
        else:
            results.append(comp)
    return results

def process_centuries(century_line, century_regex, year_regex):

    results = []

    if not century_line:
        return None

    match = re.search(century_regex, century_line)
    if match is not None:
        return match.group(0) + ' century'

    match = re.search(year_regex, century_line)
    if match is not None:
        year = int(match.group(0))
        century = year_to_century(year)
        return century + 'th century'

def main(input, type):

    results = []

    composer_start = 'Composer:'
    century_start = 'Composition Year:'

    century_regex = re.compile('\d\dth')
    year_regex = re.compile('\d\d\d\d')

    with open(input, 'r') as ins:
        if type == 'composer':
            for line in ins:
                if composer_start in line:
                    line = line[len(composer_start):]
                    composers = process_composers(line)
                    results.extend(composers)

        elif type == 'century':
            for line in ins:
                if century_start in line:
                    line = line[len(century_start):].strip()
                    centuries = process_centuries(line, century_regex, year_regex)
                    results.append(centuries)


    results = [r for r in results if r is not None]
    results_counter = Counter(results)
    print_results(results_counter)

if __name__ == '__main__':
    input = sys.argv[1]
    type = sys.argv[2]
    main(input, type)
