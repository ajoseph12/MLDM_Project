import numpy as np
import time
import signal


class Sudoku(object):

    def __init__(self, dim = 4, num_list = [1,2,3,4]):

        self.dim = dim
        self.num_list = num_list
        self.sudoku = self.__create_sudoku()

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


def handler(signum, frame):
    #print("Forever is over")
    raise Exception("end of time") 

def loop_forever():
    while 1:
        print('sec')
        time.sleep(1)

def main():

    while True:
        
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(2)

        try:
            s = Sudoku(dim,num_list)
            print(s.sudoku)
        
        except:
            continue

        break


if __name__ == '__main__':
    dim = 4
    num_list = [1,4,8,9]
    main()

