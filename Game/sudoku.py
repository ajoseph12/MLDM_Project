import numpy as np
import time
import time
import sys
import random as rn


class Sudoku(object):

    def __init__(self, user_input,size = 4):

        self.user_input = user_input
        gen_puzzle = self.__sudoku(size)
        self.final_arr = self.__transform(gen_puzzle)


    def __sudoku(self, size):

        mydict =  dict()
        n = 0

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
        

        return mydict

    def __transform(self, puzzle_dict):

        temp_list = list()
        temp_dict = dict()

        for n,v in puzzle_dict.items():
            temp_list.append(v)

        temp_arr = np.array(temp_list)
        #print(temp_arr)
        
        for i in range(1,5): 
            temp_dict[i] = self.user_input[i-1]

        for i in range(temp_arr.shape[0]):
            for j in range(temp_arr.shape[1]):
                temp_arr[i,j] = temp_dict[temp_arr[i,j]]

        return temp_arr




if __name__ == '__main__':
    
    s = Sudoku([0,8,7,6])
    print(s.final_arr)







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
        print("Forever is over")
        return s.sudoku
    
    except:
        print('error')
        main()


if __name__ == '__main__':
    dim = 4
    num_list = [1,4,8,9]
    main()



\begin{figure}
    \centering
    \begin{subfigure}
        \centering
        \includegraphics[width=.65\linewidth]{Images/db1_d_1.png}
        \caption{Detection on dataset 1}
    \end{subfigure}
    \begin{subfigure}
        \centering
         \includegraphics[width=.65\linewidth]{Images/db1_d_2.png}
        \caption{Detection on dataset 1}
    \end{subfigure}
    \begin{subfigure}
        \centering
        \includegraphics[width=.65\linewidth]{Images/db2_d_1.png}
        \caption{Detection on dataset 2}
    \end{subfigure}
    \begin{subfigure}
        \centering
        \includegraphics[width=.65\linewidth]{Images/db2_d_2.png}
        \caption{Detection on dataset 2}
    \end{subfigure}

    \caption{Colour-Patch detection on images from datasets 1 and 2}
    \label{yolo_detections}
\end{figure}


"""