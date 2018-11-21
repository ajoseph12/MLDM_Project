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


## K-Strip Algorithm
def mod_med_k(s1, s2, k=1, ec=float(1)):
    if len(s1) > len(s2):
        temp = s1
        s1 = s2
        s2 = temp
    # K value exception
    if k > min((len(s1)), (len(s2))) or k < 1:
        raise Exception('K VALUE OUT OF BOUNDS')

    # INITIALIZATION
    m = init(s1, s2)

    # Offset counter
    offset = - (k - 2)
    # Limit counter
    cap = k + 1 + abs(len(s1) - len(s2))
    # Loop for K strips around the main diagonal
    for i in range(1, m.shape[0]):
        for j in range(max(1, offset), cap):
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
                con3 = m[i - 1, j - 1] + cost(s1[i - 1], s2[j - 1], ec_insertion=False, ec_deletion=False)

            # assign minimum value
            m[i][j] = min(con1, con2, con3)
            # print("con1: {} con2: {} con3: {} min: {}".format(con1, con2, con3, m[i][i]))
            # Saving Result
        offset += 1
        if cap < m.shape[1]:
            cap += 1
    return m[m.shape[0] - 1][m.shape[1] - 1]


def cost(x, y, ec_insertion=True, ec_deletion=False):
    if ec_insertion and not ec_deletion:
        return y
    if ec_deletion and not ec_insertion:
        return x
    if ec_insertion == False and ec_deletion == False:
        if x == 7:
            x = 1
        if y == 7:
            y = 1
        if x == 6:
            x = 2
        if y == 6:
            y = 2
        if x == 5:
            x = 3
        if y == 5:
            y = 3

        if abs(x - y) == 1:
            return 0.25
        if abs(x - y) == 2:
            return 0.50
        if abs(x - y) == 3:
            return 0.75
        else:
            return 1


if __name__ == "__main__":
    s1 = np.random.randint(0, high=8, size=9)
    s2 = np.random.randint(0, high=8, size=5)
    print(s1)
    print(s2)
    cost, matrix = mod_med_k(s1, s2, ec=1, k=1)
    print(cost)
    print(matrix)
