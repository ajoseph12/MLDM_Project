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
def modified_med(s1, s2):
    # INITIALIZATION
    m = init(s1, s2)

    for i in range(1, m.shape[0]):
        for j in range(1, m.shape[1]):

            # first condition : i is an insertion
            con1 = m[i - 1, j] + 1

            # second condition : j is a deletion
            con2 = m[i, j - 1] + 1

            # third condition : i and j are a substitution
            if s1[i - 1] == s2[j - 1]:
                # if same letters, we add nothing
                con3 = m[i - 1, j - 1]
            else:
                # if different letters, we add one
                con3 = m[i - 1, j - 1] + cost(s1[i - 1], s2[j - 1])

            # assign minimum value
            m[i][j] = min(con1, con2, con3)
    return m[m.shape[0] - 1][m.shape[1] - 1]


## K-Strip Algorithm
def mod_med_k(s1, s2, k=1):
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
            con1 = m[i - 1, j] + 1

            # second condition : j is a deletion
            con2 = m[i, j - 1] + 1

            # third condition : i and j are a substitution
            if s1[i - 1] == s2[j - 1]:
                # if same letters, we add nothing
                con3 = m[i - 1, j - 1]
            else:
                # if different letters, we add one
                con3 = m[i - 1, j - 1] + cost(s1[i - 1], s2[j - 1])

            # assign minimum value
            m[i][j] = min(con1, con2, con3)
            # print("con1: {} con2: {} con3: {} min: {}".format(con1, con2, con3, m[i][i]))
            # Saving Result
        offset += 1
        if cap < m.shape[1]:
            cap += 1
    return m[m.shape[0] - 1][m.shape[1] - 1]


def cost(x, y):
    if abs(x - y) == 1:
        return float(1/7)
    if abs(x - y) == 2:
        return float(2/7)
    if abs(x - y) == 3:
        return float(3/7)
    if abs(x - y) == 4:
        return float(4/7)
    if abs(x - y) == 5:
        return float(5/7)
    if abs(x - y) == 6:
        return float(6/7)
    if abs(x-y) == 7:
        return float(1)
    else:
        print('No optimal cost found, assigning 1 cost for substitution')
        return 1

if __name__ == "__main__":
    s1 = np.random.randint(0, high=8, size=80)
    s2 = np.random.randint(0, high=8, size=50)
    print(s1)
    print(s2)
    cost, matrix = mod_med_k(s1, s2, ec=1, k=1)
    print(cost)
    print(matrix)
