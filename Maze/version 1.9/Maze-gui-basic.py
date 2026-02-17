from tkinter import *

Player = None


def CreateMazeDesign(height, width):
    from random import shuffle, randint, choice
    board = []
    
    for row in range(height * 2 + 1):
        Row = []
        for cell in range(width * 2 + 1):
            Row.append("■")
        board.append(Row)
    
    x = randint(1, width) * 2 - 1
    y = randint(1, height) * 2 - 1

    def carve(x, y):
        board[y][x] = '□'  
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Possible directions
        shuffle(directions)

        for direction in directions:
            dx = direction[0]
            dy = direction[1]
            nx = x + dx
            ny = y + dy
            if 0 < nx < width * 2 and 0 < ny < height * 2:
                if board[ny][nx] == '■':
                    board[y + dy // 2][x + dx // 2] = '□'  # Remove wall
                    carve(nx, ny)

    carve(x, y)
        
    while True:
        Exit = [randint(0,height*2 ),randint(0,width)]
        
        if [Exit[0],Exit[1]] in [0, width*2, height*2 ]:
            continue        
        if Exit[0] in (0, height*2):
            break
        if Exit[1] in (0, width*2):
            break
        
    board[Exit[0]][Exit[1]] = "◇"          
    return board, Exit




def CreateMaze(win, BluePrint):
    Row = len(BluePrint)
    Col = len(BluePrint[0])

    maze = list()
    
    for R in range(Row):
        col = list()
        for C in range(Col):
            label = Label(win, text = BluePrint[R][C])#, relief='solid')
            label.place(x=C*15, y=R*15)
            col.append(label)
        maze.append(col)

    return maze




def CreatePlayer(maze, mazeData):
    from random import choice
    
    Locations = list()
    for row in range(len(mazeData)):
        for col in range(len(mazeData[0])):
            if mazeData[row][col] == "□":
                Locations.append([row, col])
                
    location = choice(Locations)
    mazeData[location[0]][location[1]] = "●"
    maze[location[0]][location[1]].config(text = "●")
    return location




def UpdatePlayer(maze, mazeData, dir):
    global Player
    x, y = Player[0], Player[1]
    
    if dir == "w":
        if mazeData[x - 1][y] == "■": 
            return Player
        mazeData[x][y] = "□" 
        mazeData[x - 1][y] = "●" 
        maze[x][y].config(text="□") 
        maze[x - 1][y].config(text="●") 
        Player = [x - 1, y]

    elif dir == "s":
        if mazeData[x + 1][y] == "■": 
            return Player
        mazeData[x][y] = "□"
        mazeData[x + 1][y] = "●"
        maze[x][y].config(text="□")
        maze[x + 1][y].config(text="●")
        Player = [x + 1, y]

    elif dir == "a":
        if mazeData[x][y - 1] == "■":
            return Player
        mazeData[x][y] = "□"
        mazeData[x][y - 1] = "●"
        maze[x][y].config(text="□")
        maze[x][y - 1].config(text="●")
        Player = [x, y - 1]

    elif dir == "d":
        if mazeData[x][y + 1] == "■": 
            return Player
        mazeData[x][y] = "□"
        mazeData[x][y + 1] = "●"
        maze[x][y].config(text="□")
        maze[x][y + 1].config(text="●")
        Player = [x, y + 1]
        



def PathSol(maze, mazeData, path, blocked = None):
    
    for r in range(len(mazeData)):
        for c in range(len(mazeData[0])):
            if mazeData[r][c] == "♧":
                return None
    
    if blocked == None:
        blocked = list()
    
    current = path[-1]
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    possible_moves = []

    for dx, dy in directions:
        nx, ny = current[0] + dx, current[1] + dy
        if mazeData[nx][ny] == "□":
            possible_moves.append([nx, ny])
        elif mazeData[nx][ny] == "◇":  # Exit        
            for x,y in blocked:
                mazeData[x][y] = "□"
                maze[x][y].config(text="□")
            result = path[1:] + [[nx,ny]]
            for x,y in result:
                mazeData[x][y] = "♧"
                maze[x][y].config(text="♧")
            return path + [[nx, ny]]
            
    for move in possible_moves:
        mazeData[move[0]][move[1]] = "■"
        maze[move[0]][move[1]].config(text="■")
        blocked.append(move)
        new_path = PathSol(maze, mazeData, path + [move],blocked)
        if new_path:
            return new_path

    return None  # No path found







def DetectKey(event, maze, mazeData):
    key = str(event.keysym)
    global Player

    print(key, Player)
    if key.lower() in "wasd":
        direction = key.lower()
        UpdatePlayer(maze, mazeData, direction)
    if key == "z":
        PathSol(maze, mazeData, [Player])




def EscapeMaze(height,width):
    from tkinter import Tk
    MainWindow = Tk()
    MainWindow.title("MainWindow")
    if height == 7 and width == 7:
        MainWindow.geometry(f"{width*50}x{height*33}")
    Design, Exit = CreateMazeDesign(height,width)
    MazeMap = CreateMaze(MainWindow, Design)
    global Player
    Player = CreatePlayer(MazeMap, Design)
    MainWindow.bind("<Key>",lambda event: DetectKey(event, MazeMap, Design))
    MainWindow.mainloop()






EscapeMaze(15,15)










