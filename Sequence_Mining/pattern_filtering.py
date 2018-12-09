import os

pattern_dir = os.path.dirname(__file__)

for x in range(10):
    with open(os.path.join(pattern_dir, "./patterns/" + str(x) + ".txt"), mode='r') as pattern_file:
        patterns = pattern_file.readlines()
        filtered_patterns = []
        for pattern in patterns[:]:
            mined_pattern = list(map(int, pattern.split(" -1")[0].split(" ")))
            if len(mined_pattern) < 15:
                patterns.remove(pattern)

        with open(os.path.join(pattern_dir, "./filtered_patterns/" + str(x) + ".txt"), "w") as text_file:
            for pattern in patterns:
                print(pattern[:-1], file=text_file)
    print("fininshed for ", str(x))


