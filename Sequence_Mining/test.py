from collections import defaultdict
import pandas as pd
from prefixspan import PrefixSpan
from pymining import seqmining


#import freeman code for drawn all images
freeman_codes = pd.read_hdf('df_freemancode.hdf')

print(freeman_codes)