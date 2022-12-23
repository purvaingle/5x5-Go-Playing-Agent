import copy
import numpy as np

def readIP():
    with open("input.txt", 'r') as f:
        lines = f.readlines()
        P1 = int(lines[0])
        previousB = [[int(x) for x in line.rstrip('\n')] for line in lines[1:sizeOfB+1]]
        curr_B = [[int(x) for x in line.rstrip('\n')] for line in lines[sizeOfB+1: 2*sizeOfB+1]]  
    return P1, previousB, curr_B

def writeOP(NM):
    f=open("output.txt", 'w')
    if NM is None or NM == ("r", "r"):
        f.write('PASS')
    else:
        f.write(f'{NM[0]},{NM[1]}')
    f.close()

def StepNum(previousB, curr_B):
    previousB_val = 1
    curr_B_val = 1
    i=-1
    while i<sizeOfB-2:
        i=i+1
        j=-1
        while j<sizeOfB-2:
            j=j+1
            if previousB[i][j] != 0:
                previousB_val = 2
                curr_B_val = 2
                break
            elif curr_B[i][j] != 0:
                curr_B_val = 2

    f= open("step.txt",'r')
    if previousB_val==1 and curr_B_val==1:
        numOfS = 0
    elif previousB_val==1 and curr_B_val==2:
        numOfS = 1
    else:
        numOfS = int(f.readline())
        numOfS += 2
    f.close()

    f= open("step.txt", 'w')
    f.write(f'{numOfS}')
    f.close()
    return numOfS


class GoPlayer1:
    def __init__(self, P1, previousB, curr_B):
        self.P1 = P1
        self.previousB = previousB
        self.curr_B = curr_B

    def AlphaBeta(self, d, numOfS):
        steps=numOfS
        actionMax, maxActionVal = self.maxim(0,-99999, 99999, self.P1, d, 0, self.curr_B, steps, None)
        writeOP(actionMax)

    def maxim(self, game_over, Alph, Bet, P1, d, d_curr,  B_state,  numOfS, end_move):
        maxActionVal = -99999
        if d == d_curr or numOfS + d_curr == 24:
            return self.evaluation(P1, B_state)
        if game_over==1:
            return self.evaluation(P1, B_state)
        actionMax = None
        game_over = 0
        vm = self.ValidMoves(P1, B_state)
        vm.append(("r", "r"))
        if end_move == ("r", "r"):
            game_over = 1
        for ValidMove in vm[:20]:
            if ValidMove == ("r", "r"):
                new_B_state = copy.deepcopy(B_state)
            else:
                new_B_state = self.move(P1, B_state, ValidMove)
            minActionVal = self.minim(game_over, Alph, Bet, 3-self.P1, d, d_curr + 1, new_B_state, numOfS, ValidMove)
            if maxActionVal < minActionVal:
                maxActionVal = minActionVal
                actionMax = ValidMove
            if maxActionVal >= Bet:
                if d_curr == 0:
                    return actionMax, maxActionVal
                else:
                    return maxActionVal

            if maxActionVal> Alph:
                Alph=maxActionVal

            else:
                Alph=maxActionVal
        if d_curr == 0:
            return actionMax, maxActionVal
        else:
            return maxActionVal

    def minim(self, game_over, Alph, Bet, P1, d, d_curr, B_state, numOfS, end_move):
        if d == d_curr:
            return self.evaluation(P1, B_state)
        if numOfS + d_curr == 24 or game_over==1:
            return self.evaluation(self.P1, B_state)
        game_over = 0
        minActionVal = 99999
        vm = self.ValidMoves(P1, B_state)
        vm.append(("r", "r"))
        if end_move == ("r", "r"):
            game_over = 1
        for ValidMove in vm[:20]:
            if ValidMove == ("r", "r"):
                new_B_state = copy.deepcopy(B_state)
            else:
                new_B_state = self.move(P1, B_state, ValidMove)
            maxActionVal = self.maxim(game_over, Alph, Bet, 3-P1, d, d_curr + 1, new_B_state, numOfS, ValidMove)
            if maxActionVal < minActionVal:
                minActionVal = maxActionVal
            if minActionVal <= Alph:
                return minActionVal

            if Bet>minActionVal:
                Bet=minActionVal
            else:
                Bet=Bet
        return minActionVal

    def EulerNum(self, P1, B_state):
        q1_P1 = 0
        new_B_state = np.zeros((sizeOfB + 2, sizeOfB + 2), dtype=int)
        q3_P1 = 0
        qd_P1 = 0
        i=-1
        while i<sizeOfB-1:
            i=i+1
            j=-1
            while j<sizeOfB-1:
                j=j+1
                new_B_state[i + 1][j + 1] = B_state[i][j]

        q1_P2 = 0
        q3_P2 = 0
        qd_P2 = 0
        
        i=-1
        while i<sizeOfB-1:
            i=i+1
            while j<sizeOfB-1:
                j=j+1
                new_state = new_B_state[i: i + 2, j: j + 2]
              
                check= self.Q1(P1, new_state)
                if check==1:
                    q1_P1 = q1_P1+check
                
                check= self.Q3(P1, new_state)
                if check==1:
                    q3_P1=q3_P1+check
                
                check= self.Qd(P1, new_state)
                if check==1:
                    qd_P1=qd_P1+check
                
                check= self.Q1(3-P1, new_state)
                if check==1:
                    q1_P2= q1_P2+check
                
                check= self.Q3(3-P1, new_state)
                if check==1:
                    q3_P2=q3_P2+check
                
                check= self.Qd(3-P1, new_state)
                if check==1:
                    qd_P2=qd_P2+check
                
        eulerNum=(2 * 1 * q3_P1 - (q1_P2 - qd_P2 + 2 * q3_P2) + q1_P1 - qd_P1 + 0) / 4 *1
        return eulerNum

    def Q1(self, P1, state):
        BL=state[0][0]
        BR=state[0][1]
        TL=state[1][0]
        TR=state[1][1]  
        if BL==P1 and BR!=P1 and TL!=P1 and TR!=P1:
            set1=1
        
        if BL != P1 and BR == P1 and TL != P1 and TR != P1:
            set2=2
        
        if BL != P1 and BR != P1 and TL == P1 and TR != P1:
            set3=3
        
        if BL != P1 and BR != P1 and TL != P1 and TR == P1:
            set4=4
        
        if (set1==1 or set2==2 or set3==3 or set4==4):
            return 1
        else:
            return 2
        

    def Q3(self, P1, state):
        BL=state[0][0]
        BR=state[0][1]
        TL=state[1][0]
        TR=state[1][1] 
        
        if BL == P1 and BR != P1 and TL != P1 and TR == P1:
            set1=1
        
        if BL != P1 and BR == P1 and TL == P1 and TR != P1:
            set2=2
        
        if set1==1 or set2==2:
            return 1
        else:
            return 2

    def Qd(self, P1, state):
        BL=state[0][0]
        BR=state[0][1]
        TL=state[1][0]
        TR=state[1][1] 
        if BL == P1 and BR == P1 and TL == P1 and TR != P1:
            set1=1
            
        if BL != P1 and BR == P1 and TL == P1 and TR == P1:
            set2=2
        
        if BL == P1 and BR != P1 and TL == P1 and TR == P1:
            set3=3
            
        if BL != P1 and BR == P1 and TL == P1 and TR == P1:
            set4=4
        if set1==1 or set2==2 or set3==3 or set4==4:
            return 1
        else:
            return 2    

    def evaluation(self, P1, B_state):
        P1_num = 0
        P1Lib = set()
        P2_num = 0
        P2Lib = set()
        i=-1
        while i<sizeOfB-1:
            i=i+1
            j=-1
            while j<sizeOfB-1:
                j=j+1
                if B_state[i][j] == P1:
                    P1_num += 1
                elif B_state[i][j] == 3-P1:
                    P2_num += 1
                else:
                    ind=-1
                    while ind<3:
                        ind=ind+1
                        if 0 <= i + changes[ind][0] < sizeOfB and 0 <= j + changes[ind][1] < sizeOfB:
                            if B_state[i + changes[ind][0]][j + changes[ind][1]] == P1:
                                P1Lib.add((i, j))
                            elif B_state[i + changes[ind][0]][j + changes[ind][1]] == 3-P1:
                                P2Lib.add((i, j))

        P1_edge = 0
        j=-1
        while j<sizeOfB-1:
            j=j+1
            if B_state[0][j] == P1 or B_state[sizeOfB - 1][j] == P1:
                P1_edge += 1
         
        j=0
        while j<sizeOfB-2:
            j=j+1
            if B_state[j][0] == P1 or B_state[j][sizeOfB - 1] == P1:
                P1_edge += 1
        
        e=self.EulerNum(P1, B_state)
        SC_val = min(max((len(P1Lib) - len(P2Lib)), -4), 4) -  P1_edge + (-4 * e) + 0 + (5 * (P1_num - P2_num))
        
        if self.P1==1:
            return SC_val
        elif self.P1 == 2:
            SC_val =SC_val+2.5

        return SC_val

    def move(self, P1, B_state, move):
        new_B_state = copy.deepcopy(B_state)
        new_B_state[move[0]][move[1]] = P1
        ind=-1
        while ind<3:
            ind=ind+1
            if 0 <= move[0] + changes[ind][0] < sizeOfB and 0 <= move[1] + changes[ind][1] < sizeOfB:
                if new_B_state[move[0] + changes[ind][0]][move[1] + changes[ind][1]] == 3-P1:
                    ST = [(move[0] + changes[ind][0], move[1] + changes[ind][1])]
                    Vis = set()
                    delete_P2 = 1
                    while ST:
                        T = ST.pop()
                        Vis.add(T)
                        ind2=-1
                        while ind2<3:
                            ind2=ind2+1
                            if 0 <= T[0] + changes[ind2][0] < sizeOfB and 0 <= T[1] + changes[ind2][1] < sizeOfB:
                                if (T[0] + changes[ind2][0], T[1] + changes[ind2][1]) in Vis:
                                    continue
                                elif new_B_state[T[0] + changes[ind2][0]][T[1] + changes[ind2][1]] == 0:
                                    delete_P2 = 2
                                    break
                                elif new_B_state[T[0] + changes[ind2][0]][T[1] + changes[ind2][1]] == 3-P1 and (T[0] + changes[ind2][0], T[1] + changes[ind2][1]) not in Vis:
                                    ST.append((T[0] + changes[ind2][0], T[1] + changes[ind2][1]))

                    if delete_P2==1:
                        for item in Vis:
                            new_B_state[item[0]][item[1]] = 0
        return new_B_state

    

    def ValidMoves(self, P1, B_state):
        highest_rank=[]
        second_rank=[]
        third_rank=[]
        i=-1
        while i<sizeOfB-1:
            i=i+1
            j=-1
            while j<sizeOfB-1:
                j=j+1
                if B_state[i][j] == 0:
                    check=self.Liberty(i, j, B_state,  P1)
                    if check==1:
                        check2=self.KO(i, j)
                        if check2==2 :
                            if i == 0 or j == 0 or i == sizeOfB - 1 or j == sizeOfB - 1:
                                third_rank.append((i,j))
                            else:
                                second_rank.append((i, j))
                    else:
                        ind=-1
                        while ind<3:
                            ind=ind+1
                            if 0 <= i + changes[ind][0] < sizeOfB and 0 <= j + changes[ind][1] < sizeOfB:
                                if B_state[i + changes[ind][0]][j + changes[ind][1]] == 3-P1:
                                    new_B_state = copy.deepcopy(B_state)
                                    new_B_state[i][j] = P1
                                    check= self.Liberty(i + changes[ind][0], j + changes[ind][1], new_B_state, 3-P1)
                                    if check==2 :
                                        check2=self.KO(i, j)
                                        if check2==2:
                                            highest_rank.append((i, j))
                                        break

        vm_list = []
        x=-1
        while x<len(highest_rank)-1:
            x=x+1
            vm_list.append(highest_rank[x])
        x=-1
        while x<len(second_rank)-1:
            x=x+1
            vm_list.append(second_rank[x])
        x=-1
        while x<len(third_rank)-1:
            x=x+1
            vm_list.append(third_rank[x])
        return vm_list

    def Liberty(self, i, j, B_state,  P1):
        ST = [(i, j)]
        Vis = set()
        while ST:
            T = ST.pop()
            Vis.add(T)
            ind=-1
            while ind<3:
                ind=ind+1
                if 0 <= T[0] + changes[ind][0] < sizeOfB and 0 <= T[1] + changes[ind][1] < sizeOfB:
                    if (T[0] + changes[ind][0], T[1] + changes[ind][1]) in Vis:
                        continue
                    elif B_state[T[0] + changes[ind][0]][T[1] + changes[ind][1]] == 0:
                        return 1
                    elif B_state[T[0] + changes[ind][0]][T[1] + changes[ind][1]] == P1 and (T[0] + changes[ind][0], T[1] + changes[ind][1]) not in Vis:
                        ST.append((T[0] + changes[ind][0], T[1] + changes[ind][1]))
        return 2

    def KO(self, i, j):
        if self.previousB[i][j] != self.P1:
            return 2
        new_B_state = copy.deepcopy(self.curr_B)
        new_B_state[i][j] = self.P1
        P2_i, P2_j = self.P2Move()
        ind=-1
        while ind<3:
            ind=ind+1
            if i + changes[ind][0] == P2_i and j + changes[ind][1] == P2_j:
                check=self.Liberty(i + changes[ind][0], j + changes[ind][1], new_B_state,  3-self.P1)
                if check==2 :
                    self.DeleteCluster(i + changes[ind][0], j + changes[ind][1], new_B_state, 3-self.P1)
        if np.array_equal(new_B_state, self.previousB):
            return 1
        return 2

    def P2Move(self):
        if np.array_equal(self.curr_B, self.previousB):
            return None
        i=-1
        while i<sizeOfB-1:
            i=i+1
            j=-1
            while j<sizeOfB-1:
                j=j+1
                if self.curr_B[i][j] != self.previousB[i][j] and self.curr_B[i][j] != 0:
                    return i, j

    def DeleteCluster(self, i, j, B_state, P1):
        ST = [(i, j)]
        Vis = set()
        while ST:
            T = ST.pop()
            Vis.add(T)
            B_state[T[0]][T[1]] = 0
            ind=-1
            while ind<3:
                ind=ind+1
                if 0 <= T[0] + changes[ind][0] < sizeOfB and 0 <= T[1] + changes[ind][1] < sizeOfB:
                    if (T[0] + changes[ind][0], T[1] + changes[ind][1]) in Vis:
                        continue
                    elif B_state[T[0] + changes[ind][0]][T[1] + changes[ind][1]] == P1:
                        ST.append((T[0] + changes[ind][0], T[1] + changes[ind][1]))
        return B_state

def main():
    global sizeOfB
    global changes
    sizeOfB = 5
    changes=[[1,0],[0,1],[-1,0],[0,-1]]
    P1, previousB, curr_B = readIP()
    player = GoPlayer1(P1, previousB, curr_B)
    numOfS = StepNum(previousB, curr_B)
    player.AlphaBeta(4, numOfS)

if __name__ == '__main__':
    main()