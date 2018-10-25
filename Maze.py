#Maze.py
#Rebecca Tran
#1425611

from graphics import *
from random import choice, randint

class MyStack:
    def push(item,s):
        return [item] + s
    def pop(s):
        return s.pop(0)
    def isEmpty(s):
        if s == []:
            return True
        else:
            return False 
    def size(s):
        return len(s)

class Cell(object):
    """Cell singleton object, holds four walls"""
    north = True
    south = True
    east = True
    west = True
    visited = True
    
    def __init__(self):
        pass
 

class Maze(object):
    """Maze object"""

    maze_size = 0
    cell_grid = []

    def __init__(self, maze_size):
        # set sizes
        self.maze_size = maze_size
        visited_cells = 1
        total_cells = maze_size * maze_size
        cell_stack = []
        self.kvisited = []
        self.evisited = []
        self.key_path = []
        self.end_path = []

        #makes window
        self.win = GraphWin("MakeMaze", maze_size*50, maze_size*50)
        #self.Draw(self.win)

        #start and end
        self.startX = randint(1, maze_size)
        self.startY = randint(1, maze_size)

        rectangle = Rectangle(Point(self.startX*40 + 15, self.startY*40 + 15), Point(self.startX*40 - 15, self.startY*40 - 15))
        rectangle.move(20, 20)
        rectangle.setFill("Green")
        rectangle.draw(self.win)

        self.endX = randint(1, maze_size)
        self.endY = randint(1, maze_size)

        rectangle = Rectangle(Point(self.endX*40 + 15, self.endY*40 + 15), Point(self.endX*40 - 15, self.endY*40 - 15))
        rectangle.move(20, 20)
        rectangle.setFill("Red")
        rectangle.draw(self.win)

        self.keyX = randint(1, maze_size)
        self.keyY = randint(1, maze_size)
        
        rectangle = Rectangle(Point(self.keyX*40 + 15, self.keyY*40 + 15), Point(self.keyX*40 - 15, self.keyY*40 - 15))
        rectangle.move(20, 20)
        rectangle.setFill("Grey")
        rectangle.draw(self.win)

        # generate the cell grid
        self.cell_grid = [[Cell() for _ in range(maze_size + 2)] \
                                  for i in range(maze_size + 2)]
        for i in range(1, maze_size + 1):
            for j in range(1, maze_size + 1):
                self.cell_grid[i][j].visited = False

        # dfs path creation
        #currentX, currentY = randint(1, maze_size), randint(1, maze_size)
        currentX = 1
        currentY = 1

        while visited_cells < total_cells:
            # find neighbours
            neighbours = self.try_visit(currentX, currentY)
            if (len(neighbours) >= 1):
                # choose neighbour at random
                nextX, nextY, direction = choice(neighbours)

                # knock down wall
                if direction == "east":
                    self.cell_grid[currentX][currentY].east = False
                    self.cell_grid[nextX][nextY].west = False
                elif direction == "west":
                    self.cell_grid[currentX][currentY].west = False
                    self.cell_grid[nextX][nextY].east = False
                elif direction == "north":
                    self.cell_grid[currentX][currentY].north = False
                    self.cell_grid[nextX][nextY].south = False
                elif direction == "south":
                    self.cell_grid[currentX][currentY].south = False
                    self.cell_grid[nextX][nextY].north = False

                self.cell_grid[currentX][currentY].visited = True
                # push current cell to stack, and make new
                cell_stack = MyStack.push((currentX, currentY),cell_stack)
                currentX, currentY = nextX, nextY
                self.cell_grid[currentX][currentY].visited = True

                visited_cells += 1
            else:
                currentX, currentY = MyStack.pop(cell_stack)


    def get_cell(self, posX, posY):
        cell = self.cell_grid[posX][posY]
        return cell, cell.visited == False

    def try_visit(self, currentX, currentY):
        ret = []
        cell, good = self.get_cell(currentX + 1, currentY)
        if good:
            ret.append((currentX + 1, currentY, "east"))

        cell, good = self.get_cell(currentX - 1, currentY)
        if good:
            ret.append((currentX - 1, currentY, "west"))

        cell, good = self.get_cell(currentX, currentY + 1)
        if good:
            ret.append((currentX, currentY + 1, "north"))

        cell, good = self.get_cell(currentX, currentY - 1)
        if good:
            ret.append((currentX, currentY - 1, "south"))

        return ret


    def Draw(self,win):
        for x in range(1,len(self.cell_grid)-1):
            for y in range(1,len(self.cell_grid[x])-1):
                if self.cell_grid[x][y].north == True:
                    line=Line(Point(x*40,y*40+40),Point(x*40+40,y*40+40))
                    line.setFill("Black")
                    line.draw(self.win)
                if self.cell_grid[x][y].south == True:
                    line=Line(Point(x*40,y*40),Point(x*40+40,y*40))
                    line.setFill("Black")
                    line.draw(self.win)
                if self.cell_grid[x][y].east == True:
                    line=Line(Point(x*40+40,y*40+40),Point(x*40+40,y*40))
                    line.setFill("Black")
                    line.draw(self.win)
                if self.cell_grid[x][y].west == True:
                    line=Line(Point(x*40,y*40+40),Point(x*40,y*40))
                    line.setFill("Black")
                    line.draw(self.win)
                if (x, y) in self.key_path:
                    rectangle = Rectangle(Point(x*40+10,y*40+10),Point(x*40+30,y*40+30))
                    rectangle.setFill("Orange")
                    rectangle.draw(self.win)
                if (x, y) in self.end_path:
                    rectangle = Rectangle(Point(x*40+15,y*40+15),Point(x*40+25,y*40+25))
                    rectangle.setFill("Blue")
                    rectangle.draw(self.win)
                    
            
    def Explore(self,x,y,fx,fy,path,visited):
        if x == fx and y == fy:
            path += [(x, y)]
            return True
        if (x, y) in visited:
            return False
        visited += [(x, y)]
        if x + 1 < self.maze_size and self.cell_grid[x][y].east == False:
            if self.Explore(x + 1,y,fx,fy,path,visited):
                path += [(x, y)]
                return True
        if x - 1 >= 0 and self.cell_grid[x][y].west == False:
            if self.Explore(x - 1,y,fx,fy,path,visited):
                path += [(x, y)]
                return True
        if y + 1 < self.maze_size and self.cell_grid[x][y].north == False:
            if self.Explore(x, y + 1,fx,fy,path,visited):
                path += [(x, y)]
                return True
        if y - 1 >= 0 and self.cell_grid[x][y].south == False:
            if self.Explore(x, y - 1,fx,fy,path,visited):
                path += [(x, y)]
                return True
        
def Main():
    m = Maze(10)
    m.Explore(m.startX, m.startY, m.keyX, m.keyY, m.key_path, m.kvisited)
    print(m.key_path)
    m.Explore(m.keyX, m.keyY, m.endX, m.endY, m.end_path, m.evisited)
    print(m.end_path)
    m.Draw(m.win)


Main()


        
