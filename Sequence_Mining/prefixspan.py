from collections import defaultdict
import pandas as pd

def frequent_rec(patt, mdb):
    results.append((len(mdb), patt))

    occurs = defaultdict(list)
    for (i, startpos) in mdb:
        seq = db[i]
        for j in range(startpos + 1, len(seq)):
            try:
                l = occurs[seq[j]]
                if len(l) == 0 or l[-1][0] != i:
                    l.append((i, j))
            except TypeError:
                print('typeErroroccured')

    for (c, newmdb) in occurs.items():
        if len(newmdb) >= minsup:
            frequent_rec(patt + [c], newmdb)


#import freeman code for drawn all images
freeman_codes = pd.read_hdf('df_freemancode.hdf')

results = []

minsup = 2

db = []

#mine the codes from 0 to 9
for x in range(10):
    results = []
    db = []
    temp_class = freeman_codes.loc[freeman_codes['Label'] == float(x)]

    # generate input array from pandas dataframe
    for index, row in temp_class.iterrows():
        db.append(row["Freeman Code"][0].tolist())
    frequent_rec([], [(i, -1) for i in range(len(db))])
    with open("Output_patterns_for_" + x + ".txt", "w") as text_file:
        print(results, file=text_file)







#frequent_rec([], [(i, -1) for i in range(len(db))])

#print(results)
