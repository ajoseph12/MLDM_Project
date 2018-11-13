from collections import defaultdict

def frequent_rec(patt, mdb):
    results.append((len(mdb), patt))

    occurs = defaultdict(list)
    for (i, startpos) in mdb:
        seq = db[i]
        for j in range(startpos + 1, len(seq)):
            l = occurs[seq[j]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, j))

    for (c, newmdb) in occurs.items():
        if len(newmdb) >= minsup:
            frequent_rec(patt + [c], newmdb)


db = [
    [0, 1, 2, 3, 4],
    [1, 1, 1, 3, 4],
    [2, 1, 2, 2, 0],
    [1, 1, 1, 2, 2],
]

#import freeman code for drawn image

#mine the image



minsup = 2

results = []

frequent_rec([], [(i, -1) for i in range(len(db))])

import cv
print(cv2.)
#print(results)