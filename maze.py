#COMP SCI 1XA3 project
#maze.py
#Levin Noronha

'''
This program uses stacks and depth-first algorithms to draw out a perfect maze
as well as its solution. To visualize the maze, graphics.py was used.

LEGEND
------
Green  = Start
Yellow = Key
Red    = Exit
Pink Circles = path to key
Black dots   = path to exit

Format of Cell Locations is (Row,Column)

NOTE: the design concept on mazeworks.com suggested using of 4 lists of length
four to store properties of each cell, like so...

[0,0,0,0] [0,0,0,0] [0,0,0,0] [0,0,0,0]
Backtrack  Solution   Walls    Borders

However, during the design, I discovered a way to backtrack and solve the maze,
without using the Backtrack and Solutions list. So therefore, the backtrack and
solution properties of each cell in the maze below were left untouched as
[1,1,1,1]. Instead, I used a stack to store the solution paths.

Also, stacks were only used for lists of importance, such as visitedCells when
creating a perfect maze and the solution path to the matrix. For lists of
lesser importance, such as, accumulators and temporary variables, regular lists
were used.

P.S. If the user inputs any dimension less than 2, this program automatically
generates a 2x2 maze to avoid special cases.

'''

from graphics import *
from random import *

class MyStack:
    def __init__(self):
        self = []
    def push(self, item, S):
        return S + [item]
    def pop(self,S):
        return S.pop()
    def isEmpty(self,S):
        return len(S) == 0
    def size(self,S):
        return len(S)

class Maze:
    
    def __init__(self,N):
        #accounts for specials cases where dimensions provided are less than 2
        if N < 2:
            self.N = 2
        else:
            self.N = N

        #generates matrix for maze
        self.maze = [[[[1 for x in range(4)],[1 for x in range(4)],[1 for x in range(4)],[0 for x in range(4)]] for x in range(self.N)] for i in range(self.N)]

        self.scale = 30 #dimension of each cell in the maze
        self.translate = self.scale//2 #hor & vert. dist to center of each cell

        self.PerfectMaze()#generates perfect maze

        #finds quickest path from start to key 
        self.pathtoKey = self.Explore(self.start[0],self.start[1],self.key[0],self.key[1])

        #Prints quickest path from start to key
        print('Path from start to key: ',end=' ')
        for i in range(len(self.pathtoKey)):
            print('('+str(self.pathtoKey[i][0]+1)+','+str(self.pathtoKey[i][1]+1)+')',end=' ')
        print()

        #finds quickest path from key to exit
        self.pathtoEnd = self.Explore(self.key[0],self.key[1],self.end[0],self.end[1])

        #Prints quickest path from start to end
        print('Path from key to end: ',end=' ')
        for i in range(len(self.pathtoEnd)):
            print('('+str(self.pathtoEnd[i][0]+1)+','+str(self.pathtoEnd[i][1]+1)+')',end=' ')
        print()

    def PerfectMaze(self):

        TotalCells = self.N*self.N
        VisitedCells = 1

        #initialze stack required stack variables
        self.stack = MyStack()
        cellStack = []

        #random generation of starting point
        row = randrange(0,self.N)
        col = randrange(0,self.N)

        self.start = (row,col) #Randomly assigns a start
        #print('Start is', self.start)
        
        #assign start cell as current cell
        self.CurrentCell = (row,col)

        #Maze[Row][Column][Property][W,S,E,N]

        #Depth-First Search Algotirithm
        while VisitedCells < TotalCells:

            #generates list of available neighbours
            neighbours = self.neighbour(row,col)
                        
            if len(neighbours) != 0:

                #randomly chooses which neighbour to pick
                randNum = randrange(0,len(neighbours))

                #assign randomly chosen neighbour as next cell
                newCell = neighbours[randNum]
                newRow, newCol = newCell[0], newCell[1]
                
                #North Neighbour
                if row - 1 == newRow and col == newCol:
                    
                    #Breaks down wall between both cells                 
                    self.maze[newRow][newCol][2][1] = 0
                    self.maze[row][col][2][3] = 0

                    #Pushes current cell location to cell stack
                    cellStack = self.stack.push((row,col),cellStack)
                    row,col = newRow, newCol #Assign next cell as current cell
                    VisitedCells += 1

                    #print(True,'N')

                #South Neighbour
                elif row + 1 == newRow and col == newCol:
                    #print(True,'S')
                    self.maze[newRow][newCol][2][3] = 0
                    self.maze[row][col][2][1] = 0
                    cellStack = self.stack.push((row,col),cellStack)
                    row,col = newRow, newCol
                    VisitedCells += 1

                #East Neighbour
                elif row == newRow and col - 1 == newCol:
                    #print(True,'E')
                    self.maze[newRow][newCol][2][2] = 0
                    self.maze[row][col][2][0] = 0
                    cellStack = self.stack.push((row,col),cellStack)
                    row,col = newRow, newCol
                    VisitedCells += 1

                #West Neighbour
                elif row == newRow and col + 1 == newCol:
                    #print(True,'W')
                    self.maze[newRow][newCol][2][0] = 0
                    self.maze[row][col][2][2] = 0
                    cellStack = self.stack.push((row,col),cellStack)
                    row,col = newRow, newCol
                    VisitedCells += 1
            else:
                #print(True,5)
                #Backtrack to previous cell location
                row,col = self.stack.pop(cellStack)  
            
        #self.printMaze()

        #Sets last position as the exit
        self.end = (row,col)

        #Assigns random cell with key
        self.key = (randrange(0,self.N),randrange(0,self.N))
        while self.key == self.start or self.key == self.end:
            self.key = (randrange(0,self.N),randrange(0,self.N))

        #print('Start is', self.start)
        #print('Key is', self.key)    
        #print('End is',self.end)
            
        #Maze[Row][Column][Property][W,S,E,N]

        #Puts up borders of cell
        self.createBorders()

    #Initializes borders of the maze
    def createBorders(self):
        N = self.N
        for i in range(0,N):
            self.maze[0][i][3][3] = 1 #North Border
            self.maze[i][0][3][0] = 1 #West Border
            self.maze[i][N-1][3][2] = 1 #East Border
            self.maze[N-1][i][3][1] = 1 #South Border
        #self.printMaze()

    def printMaze(self):
        for i in self.maze:
            print(i)            
    
    #Checks for all neighbours of any given cell that have all 4 walls intact
    def neighbour(self,x,y):
       
        available = [] #list will store coordinates of all available neighbours
        
        if 0 <= x-1 < self.N: #North
            if self.maze[x-1][y][2] == [1,1,1,1]:
                available.append((x-1, y))
        if 0 <= x+1 < self.N: #South
            if self.maze[x+1][y][2] == [1,1,1,1]:
                available.append((x+1, y))
        if 0 <= y-1 < self.N: #East
            if self.maze[x][y-1][2] == [1,1,1,1]:
                available.append((x, y-1))
        if 0 <= y+1 < self.N: #West
            if self.maze[x][y+1][2] == [1,1,1,1]:
                available.append((x, y+1))
            
        return available
        
    def Draw(self):
        scale = self.scale
        N = self.N

        #Create graphics window
        self.win = GraphWin('Maze',(N*scale)+20,(N*scale)+20)
        self.win.setBackground('white')
        self.win.setCoords(-5,N*scale,N*scale,-5) #defines coordinate system for grid

        #Generate N*N grid
        for i in range(0,N):
            for j in range(0,N):
                rect = Rectangle(Point(scale*i,scale*(j+1)),Point(scale*(i+1),scale*j))
                rect.draw(self.win)

        self.drawStart_Key_Exit()

        #break down walls
        self.whiteWalls()

        #draw path from start -> key -> exit
        self.printPath()

    #Function iterates through each cell and paints broken walls with white    
    def whiteWalls(self):
        scale = self.scale
        translate = self.translate
        N = self.N

        x = -1 #initialzes row variable

        for j in range(translate,N*scale,scale):
            
            x +=1 #increments row
            y = 0 # initalizes column variable
            
            #Maze[Row][Column][Property][W,S,E,N]
            
            for i in range(translate,N*scale,scale):
                #Destroy West
                if self.maze[x][y][2][0] == 0 and (not self.BorderPresent(x,y,0)):
                    line = Line(Point(i-translate,j-translate),Point(i-translate,j+translate))
                    #print(True,1)
                    #print((i-5,j-5),(i-5,j+5))
                    line.setFill('white')
                    line.draw(self.win)
                #Destroy South
                if self.maze[x][y][2][1] == 0 and (not self.BorderPresent(x,y,1)):
                    line = Line(Point(i-translate,j+translate),Point(i+translate,j+translate))
                    #print(True,2)
                    #print((i-5,j+5),(i+5,j+5))
                    line.setFill('white')
                    line.draw(self.win)
                #Destroy East
                if self.maze[x][y][2][2] == 0 and (not self.BorderPresent(x,y,2)):
                    line = Line(Point(i+translate,j-translate),Point(i+translate,j+translate))
                    #print(True,3)
                    #print((i+5,j-5),(i+5,j+5))
                    line.setFill('white')
                    line.draw(self.win)
                #Destroy North
                if self.maze[x][y][2][3] == 0 and (not self.BorderPresent(x,y,3)):
                    line = Line(Point(i-translate,j-translate),Point(i+translate,j-translate))
                    #print(True,4)
                    #print((i-5,j-5),(i+5,j-5))
                    line.setFill('white')
                    line.draw(self.win)
                    
                y += 1 #increments column
                
    #Checks if wall is also a border
    def BorderPresent(self,x,y,direction):
        return self.maze[x][y][3][direction] == 1

    #Method for drawing out shortest path from start -> key and key -> exit
    def printPath(self):
        translate = self.translate
        scale = self.scale
        
        for i in self.pathtoKey[1:-1]:
            row,col = i
            row,col = row*scale,col*scale
            path = Circle(Point(col+translate,row+translate),0.3*scale)
            path.setFill('pink')
            path.setOutline('pink')
            path.draw(self.win)

        for i in self.pathtoEnd[1:-1]:
            row,col = i
            row,col = row*scale,col*scale
            path = Circle(Point(col+translate,row+translate),0.1*scale)
            path.setFill('black')
            path.setOutline('black')
            path.draw(self.win)

    #Method for drawing out start, key, and exit onto the maze    
    def drawStart_Key_Exit(self):
        scale = self.scale 

        #control size of start, key and exit rectangles
        adjLeft = 0.10*scale
        adjRight = 0.90*scale
        
        #local variables for start and end
        row,col = self.start
        keyRow, keyCol = self.key
        row1,col1 = self.end

        #scale cell coordinates to match maze grid
        row = (row) * scale
        col = (col) * scale
        keyRow = keyRow * scale
        keyCol = keyCol * scale
        row1 = (row1) * scale
        col1 = (col1) * scale
        
        #Draw Start Rectangle        
        start = Rectangle(Point(col+adjLeft,row+adjLeft),Point(col+adjRight,row+adjRight))
        start.setFill('green')
        start.setOutline('green')
        start.draw(self.win)

        #Draw Key Rectangle
        key = Rectangle(Point(keyCol+adjLeft,keyRow+adjLeft),Point(keyCol+adjRight,keyRow+adjRight))
        key.setFill('yellow')
        key.setOutline('yellow')
        key.draw(self.win)

        #Draw End Rectangle
        end = Rectangle(Point(col1+adjLeft,row1+adjLeft),Point(col1+adjRight,row1+adjRight))
        end.setFill('red')
        end.setOutline('red')
        end.draw(self.win)

    #Maze[Row][Column][Property][W,S,E,N]
        
    def Explore(self,row,col,row1,col1):
        
        self.stack = MyStack()
        visited = [] #stores list of all cell visted by explore function
        path = [] #stores list of cells that form the quickest path out of all visited
        
        #print('Starting at',row,col)
        while (row,col) != (row1,col1):
            if 0 <= row < self.N and 0 <= row < self.N:
                #Checks wall North
                if self.maze[row][col][2][3] == 0 and ((row-1,col) not in visited) and (not self.BorderPresent(row,col,3)):
                    #print('No wall north of',row,col)
                    visited.append((row,col))
                    path = self.stack.push((row,col),path)
                    row,col = row-1,col
                    #print('Moving to',row,col)
                #Checks wall East
                elif self.maze[row][col][2][2] == 0 and ((row,col+1) not in visited) and (not self.BorderPresent(row,col,2)):
                    #print('No wall east of',row,col)
                    visited.append((row,col))
                    path = self.stack.push((row,col),path)
                    row,col = row,col+1
                    #print('Moving to',row,col)
                #Checks wall South
                elif self.maze[row][col][2][1] == 0 and ((row+1,col) not in visited) and (not self.BorderPresent(row,col,1)):
                    #print('No wall south of',row,col)
                    visited.append((row,col))
                    path = self.stack.push((row,col),path)
                    row,col = row+1,col
                    #print('Moving to',row,col)
                #Checks wall West
                elif self.maze[row][col][2][0] == 0 and ((row,col-1) not in visited) and (not self.BorderPresent(row,col,0)):
                    #print('No wall west of',row,col)
                    visited.append((row,col))
                    path = self.stack.push((row,col),path)
                    row,col = row,col-1
                    #print('Moving to',row,col)
                else:
                    visited.append((row,col))
                    row,col = self.stack.pop(path)
                    #print('Backtrack to',row,col)
            
        visited.append((row,col))
        
        path = self.stack.push((row,col),path)
        #print('Ended explore at',row,col)
        
        return path

def main():
    print('COMP SCI 1XA3 WINTER 2015 PROJECT')
    print('by Levin Noronha\n')

    print('This program uses stacks and depth-first algorithms')
    print('to draw out a perfect maze as well as its solution.')

    print('\nGreen = Start')
    print('Yellow = Key')
    print('Red = Exit')
    print('Pink Circles = path to key')
    print('Black dots = path to exit\n')
    print('To draw this maze...',end=' ')

    #ask user for N dimension in order to generate N*N maze
    dimension = eval(input('Enter dimension(N) to make a NxN maze: '))

    print('\nFormat of Cell Locations is (Row,Column)\n')
    
    x = Maze(dimension) #create perfect maze
    x.Draw() #draw perfect maze

main()
