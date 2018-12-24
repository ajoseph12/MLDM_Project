import os
import itertools

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
                for pattern in patterns[:]:
                    mined_pattern = list(map(int, pattern.split(" -1")[0].split(" ")))
                    i += 1
                    if len(mined_pattern) < 15:
                        patterns.remove(pattern)
                        if i%1000 == 0:
                            print(i)

                print('length of pattern after removing: ', str(len(patterns)))

                patterns.sort()
                list(patterns for patterns,_ in itertools.groupby(patterns))
                print('length of pattern after duplicate removing: ', str(len(patterns)))

                with open(os.path.join(self.pattern_dir, "./filtered_patterns/" + str(x) + ".txt"), "w") as text_file:
                    for pattern in patterns:
                        print(pattern[:-1], file=text_file)
            print("Filtering finished for: ", str(x))

#testing
if __name__ == '__main__':
    FilterPatterns().filter_patterns()
