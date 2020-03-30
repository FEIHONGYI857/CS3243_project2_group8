import sys
import copy

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.domains = list()
        self.unassignedVars = set()
        self.prunes = list() #used to recall
        self.prune = list()
        self.constraints = list()#store (a1,a2) for ac-3
        self.build_constraints()
        self.neighbors = dict()
        self.build_neighbors()#store (a1,a2) for ac-3 and forward checking

    def build_constraints(self):
        for a in range(9):
            for b in range(9):#get one node
                for c in range(9):
                    for r in range(9):#get another node
                        if a == c or b == r:
                            if not(a == c  and  b == r):
                                if [a,b,c,r] not in self.constraints:
                                    self.constraints.append([a,b,c,r])
                layers = [[0,1,2], [3,4,5], [6,7,8]]
                for layer in layers:
                    if a in layer:
                        neighbourr = layer
                    if b in layer:
                        neighbourc = layer
                for d in neighbourr:
                    for e in neighbourc:
                        if [a,b,d,e] not in self.constraints:
                            if a != d and b != e:
                                self.constraints.append([a,b,d,e])
        #print(self.constraints)

    def build_neighbors(self):

        for a in range(9):
            for b in range(9):
                self.neighbors[a*9 + b] = list()
                for c in self.constraints:
                    if a == c[0] and b == c[1]:
                        self.neighbors[a*9 + b].append([c[2],c[3]])
        #print(self.neighbors[42])

    def ac3(self):
        queue = list(self.constraints)
        while queue:
            xa,xb,xc,xd = queue.pop(0)
            if self.revise(xa,xb,xc,xd):
                if len(self.domains[xa*9+xb]) == 0:
                    if xa * 9 + xb == 42:
                        print(self.domains[42])
                    return False
                for xk in self.neighbors[xa*9+xb]:
                    if xk == xa*9+xb:
                        queue.append([xa,xb,xk[0],xk[1]])
        return True

    def revise(self,xa,xb,xc,xd):
        revised = False
        for x in self.domains[xa * 9 + xb]:
            if not any([self.constraint(x, y) for y in self.domains[xc * 9 + xd]]):
                self.domains[xa * 9 + xb].remove(x)
                revised = True
        return revised

    def constraint(self, xi, xj):
        return xi != xj

    def solve(self):
        self.initDomains()
        #print(self.domains)
        self.ac3()
       # print(self.domains)
        self.backtrack()
        #print(puzzle)
        return self.ans
    def backtrack(self):
        if len(self.unassignedVars) == 0:
            return True

        #variable selection
        currVar = self.mostConstrVar(self.unassignedVars)
        #value selection
        domain = self.varDomain(self.domains,currVar)
        #print(len(domain))
        for index in range(len(domain)):
                self.assignVal(currVar,domain[index])
                if self.validCheck(currVar,domain[index]) == False:
                    self.unassignVal(currVar,domain[index])
                    continue
                if self.backtrack() == False:
                    self.unassignVal(currVar,domain[index])
                    continue
                else:
                    return True
        #add back to unassigned
        self.unassignedVars.add(currVar)
        return False
    def mostConstrVar(self,unassignedVars):
        MCV = unassignedVars.pop()
        return MCV
    def varDomain(self,domainList,currVar):
        varIndex = currVar[0]*9 + currVar[1]
        currDomain = self.domains[varIndex]
        return currDomain
    def assignVal(self,currVar,value):
        self.puzzle[currVar[0]][currVar[1]] = value
        return 1
    def unassignVal(self,currVar,value):
        self.puzzle[currVar[0]][currVar[1]] = 0
        return 1
    def initDomains(self):
        domainSet = [1,2,3,4,5,6,7,8,9]
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] == 0:
                    self.domains.append(copy.copy(domainSet))
                    self.unassignedVars.add((row,col))
                else:
                    list_addvalue = []
                    self.domains.append([puzzle[row][col]])
        return 1

    def validCheck(self,currVar,value):
        row = currVar[0]
        col = currVar[1]
        for c in range(9):
            if c != col:
                if self.puzzle[row][c] == value:
                    return False
        for r in range(9):
            if r != row:
                if self.puzzle[r][col] == value:
                    return False
        layers = [[0,1,2],[3,4,5],[6,7,8]]
        for layer in layers:
            if row in layer:
                neighbourRow = layer
            if col in layer:
                neighbourCol = layer
        #print(neighbourCol)
       # print(neighbourRow)
        for sqRow in neighbourRow:
            for sqCol in neighbourCol:
                if sqRow != row or sqCol != col:
                    if self.puzzle[sqRow][sqCol] == value:
                        return False
        return True
    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")