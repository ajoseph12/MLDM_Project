import numpy as np
import time
import timeout_decorator

def sudoku(size):
    import time
    start_time=time.time()

    import sys
    import random as rn

    mydict = {}
    n = 0

    print('--started calculating--')
    while len(mydict) < size:
        n += 1
        x = range(1, size+1)
        testlist = rn.sample(x, len(x))

        isgood = True
        for dictid,savedlist in mydict.items():
            if isgood == False:
                break
            for v in savedlist:
                if testlist[savedlist.index(v)] == v:
                    isgood = False
                    break

        if isgood == True:
            isgoodafterduplicatecheck = True
            mod = len(mydict) % 3
            dsavedlists = {}
            dtestlists = {}
            dcombindedlists = {}
            for a in range(1,mod + 1):
                savedlist = mydict[len(mydict) - a]               
                for v1 in savedlist:
                    modsavedlists = (savedlist.index(v1) / 3) % 3
                    dsavedlists[len(dsavedlists)] = [modsavedlists,v1]
                for t1 in testlist:
                    modtestlists = (testlist.index(t1) / 3) % 3
                    dtestlists[len(dtestlists)] = [modtestlists,t1]
                for k,v2 in dsavedlists.items():
                    dcombindedlists[len(dcombindedlists)] = v2
                    dcombindedlists[len(dcombindedlists)] = dtestlists[k]
            vsave = 0
            lst1 = []
            for k, vx in dcombindedlists.items():
                vnew = vx[0]
                if not vnew == vsave:
                    lst1 = []
                    lst1.append(vx[1])
                else:
                    if vx[1] in lst1:
                        isgoodafterduplicatecheck = False
                        break
                    else:
                        lst1.append(vx[1])
                vsave = vnew

            if isgoodafterduplicatecheck == True:

                mydict[len(mydict)] = testlist
                print('success found', len(mydict), 'row')

    print('--finished calculating--')
    total_time = time.time()-start_time
    return mydict, n, total_time

return_dict, total_tries, amt_of_time = sudoku(4)
print('')
print('--printing output--')
for n,v in return_dict.items():
    print(v)
print('process took',total_tries,'tries in', round(amt_of_time,2), 'secs')
print('-------------------')

"""
class Sudoku(object):

    def __init__(self, dim = 4, num_list = [1,2,3,4]):

        self.dim = dim
        self.num_list = num_list
        self.sudoku = self.__create_sudoku()

    @timeout_decorator.timeout(2, use_signals=False, timeout_exception=ValueError('fucked'))
    def __create_sudoku(self):

        memory_dict = dict()
        for num in self.num_list: memory_dict[num] = [0,1,2,3]

        sudoku = np.zeros((self.dim, self.dim))

        for i in range(self.dim):

            check = list()
            for j in self.num_list:

                temp = np.random.choice(memory_dict[j])
                while temp in check:
                    temp = np.random.choice(memory_dict[j])

                check.append(temp)
                sudoku[i, temp] = j
                memory_dict[j].remove(temp)

        return sudoku

 

def main():

    try:
        s = Sudoku()
        return s.sudoku
    
    except:
        print('error')
        main()


if __name__ == '__main__':
    dim = 4
    num_list = [1,4,8,9]
    main()

"""