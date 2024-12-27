import math

class Node:
    def __init__(self, parent=None, row=None, col=None, g=0, h=0):
        self.parent = parent
        self.row = row
        self.col = col
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"Node(row={self.row}, col={self.col}, g={self.g}, h={self.h}, f={self.f})"
    
    #referenced https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2 
    def aStar(self, start, goal, tiles): 
        openList = []
        closedList = set()
        startNode = Node(None, start[0], start[1], 0, self.heuristic(start, goal))
        openList.append(startNode)

        while len(openList) > 0:
            currentNode = openList[0]
            currentInd = 0
            for index, node in enumerate(openList): #chat
                if node.f  < currentNode.f:
                    currentNode = node
                    currentInd = index
            openList.pop(currentInd)
            closedList.add(currentNode)

            #if current position is the goal position
            if currentNode.row == goal[0] and currentNode.col == goal[1]:
                path = []
                current = currentNode
                while current is not None:
                    path.append((current.row, current.col))
                    current = current.parent
                return path[::-1]
            
            childrenNodes = [(currentNode.row+1, currentNode.col),
                             (currentNode.row-1, currentNode.col),
                             (currentNode.row, currentNode.col+1),
                             (currentNode.row, currentNode.col-1)]
            
            for (row, col) in childrenNodes:
                if ((row < 0) or (col < 0) or (row >= len(tiles)) or 
                    (col >= len(tiles[0]))):
                    continue

                g = currentNode.g + 1
                h = self.heuristic((row, col), goal)
                child = Node(currentNode, row, col, g, h)

                if any(child.row == closedChild.row and child.col == closedChild.col for closedChild in closedList): #chat
                    continue
                
                inOpenList = False
                for openChild in openList:
                    if ((child.row == openChild.row) and
                        (child.col == openChild.col)):
                        inOpenList = True
                        
                        if child.g < openChild.g:
                            openChild.g = child.g
                            openChild.f = child.f
                            openChild.parent = child.parent
                        break

                if not inOpenList:
                    openList.append(child)
        return None 
    
    def heuristic(self, start, goal):
        return math.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)


