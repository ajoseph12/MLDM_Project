import os
import itertools
from operator import itemgetter
from itertools import groupby
from collections import defaultdict

class FilterPatterns:

    def __init__(self):
         self.pattern_dir = os.path.dirname(__file__)

    def filter_patterns(self):

        for x in range(10):
            print("Filtering started for: ", str(x))

            with open(os.path.join(self.pattern_dir, "./patterns/" + str(x) + ".txt"), mode='r') as pattern_file:
                patterns = pattern_file.readlines()
                print('length of pattern before removing: ', str(len(patterns)))
                i = 0
                mined_patterns = []
                for pattern in patterns[:]:
                    mined_pattern = list(map(int, pattern.split(" -1")[0].split(" ")))
                    i += 1
                    if len(mined_pattern) == 15:
                        mined_patterns.append(mined_pattern)
                        if i%10000 == 0:
                            print(i)

                print('Length of pattern after removing: ', str(len(mined_patterns)))

                mined_patterns.sort()
                list(mined_patterns for mined_patterns,_ in itertools.groupby(mined_patterns))

                #sort remove grouped
                grouped_patterns = [list(g) for _,g in groupby(sorted(mined_patterns),itemgetter(0,1,2))]
                final_patterns = []
                for grouped_pattern in grouped_patterns:
                    vote_list = defaultdict(lambda: defaultdict(lambda:0))
                    for grouped_pattern_item in grouped_pattern:
                        for idx, item in enumerate(grouped_pattern_item):
                            vote_list[idx][item] += 1
                    merged_pattern = []
                    for k,v in vote_list.items():
                        selected_item = max(v.items(), key=lambda a: a[1])[0]
                        merged_pattern.append(selected_item)
                    final_patterns.append(merged_pattern)





                with open(os.path.join(self.pattern_dir, "./filtered_patterns/" + str(x) + ".txt"), "w") as text_file:
                    for pattern_i in final_patterns:
                        print(pattern_i, file=text_file)
            print("Filtering finished for: ", str(x), 'with length after grouping: ', str(len(final_patterns)))

#testing
if __name__ == '__main__':
    FilterPatterns().filter_patterns()
