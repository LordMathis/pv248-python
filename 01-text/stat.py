import sys
import re
from collections import Counter

input = sys.argv[1]
type = sys.argv[2]

results = []

composer_start = 'Composer:'
century_start = 'Composition year:'

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

results_counter = Counter(results)

for key in results_counter:
    print("%s: %s" % (key, results_counter[key]))
