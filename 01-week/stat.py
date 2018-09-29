import sys
import re
from collections import Counter

input = sys.argv[1]
type = sys.argv[2]

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
                line = re.sub('\(.*\)', "", line)
                comps = line.split(';')
                for comp in comps:
                    comp = comp.strip()
                    if not line:
                        continue
                    else:
                        results.append(comp)

    elif type == 'century':
        for line in ins:
            if century_start in line:
                line = line[len(century_start):].strip()

                if not line:
                    continue

                match = re.match(century_regex, line)
                if match is not None:
                    results.append(match.group(0) + ' century')
                    continue

                match = re.match(year_regex, line)
                if match is not None:
                    year = int(match.group(0))
                    century = year // 100
                    if year % 100 > 0:
                        century += 1
                    results.append(str(century) + 'th century')


results_counter = Counter(results)

for key in results_counter:

    print("%s: %s" % (key, results_counter[key]))
