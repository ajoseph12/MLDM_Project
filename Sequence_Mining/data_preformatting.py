#preprocess input freeman codes
import pandas as pd
import os

script_dir = os.path.dirname(__file__)

#import freeman code for drawn all images
freeman_codes = pd.read_hdf('train_freemancode.hdf')
db = []

#mine the codes from 0 to 9
for x in range(10):
    db = []
    temp_class = freeman_codes.loc[freeman_codes['Label'] == float(x)]

    # generate input array from pandas dataframe
    for index, row in temp_class.iterrows():
        db.append(row["Freeman Code"].tolist())

    with open(os.path.join(script_dir, "./input/input_patterns_for_" + str(x) + ".txt"), "w") as text_file:
        for item in db:
            item1 = str.replace(str(item), ',', '')
            item2 = str.replace(item1, '[', '')
            item3 = str.replace(item2, ']', '')
            print(item3 + ' -1 -2', file=text_file)







#frequent_rec([], [(i, -1) for i in range(len(db))])

#print(results)
