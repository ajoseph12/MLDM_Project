import numpy as np


# INITIALIZATION
def init(s1, s2):
    m = np.empty((len(s1) + 1, len(s2) + 1))
    m[:] = np.inf
    # initializing the first row
    m[0] = np.arange(m.shape[1])
    # initializing the first column
    counter = 0
    for i in m:
        i[0] = counter
        counter += 1
    return m


# Minimum Edit Distance (MED)
# Modified Version
def modified_med(s1, s2, ec=float(1)):
    # INITIALIZATION
    m = init(s1, s2)
    for i in range(1, m.shape[0]):
        for j in range(1, m.shape[1]):

            # first condition : i is an insertion
            con1 = m[i - 1, j] + cost(s1[i - 1], ec, ec_insertion=True, ec_deletion=False)

            # second condition : j is a deletion
            con2 = m[i, j - 1] + cost(ec, s2[j - 1], ec_insertion=False, ec_deletion=True)

            # third condition : i and j are a substitution
            if s1[i - 1] == s2[j - 1]:
                # if same letters, we add nothing
                con3 = m[i - 1, j - 1]
            else:
                # if different letters, we add one
                con3 = m[i - 1, j - 1] + 1 + cost(s1[i - 1], s2[j - 1], ec_insertion=False, ec_deletion=False)

            # assign minimum value
            m[i][j] = min(con1, con2, con3)
    return m[m.shape[0] - 1][m.shape[1] - 1], m


def cost(x, y, ec_insertion=True, ec_deletion=False):
    if ec_insertion == True and ec_deletion == False:
        return y
    if ec_deletion == True and ec_insertion == False:
        return x
    if ec_insertion == False and ec_deletion == False:
        if abs(x - y) == 1:
            return 0.1
        if abs(x - y) == 2:
            return 0.2
        if abs(x - y) == 3:
            return 0.3
        else:
            return 0.4


if __name__ == "__main__":
    s1 = np.random.randint(0, high=8, size=20)
    s2 = np.random.randint(0, high=8, size=10)
    print(s1)
    print(s2)
    cost, matrix = modified_med(s1, s2, ec=1)
    print(cost)
    #print(matrix)
