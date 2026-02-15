
def __main__():
    from os import system

    Board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    Loop = True
    LastThreeTurn = []
    MaxScore = 0
    NeedForTwo = True

    print("\n\tHello Player!")
    print("\tWould You Like To Play 2048")
    print("\tEihter \'yes\' or \'no\'\n")
    play = (input("\tOption : ")).strip().lower()

    if play=="yes":
        while Loop:
            system("cls")
            RandomAppearTwo(Board,NeedForTwo)
            DisplayBoard(Board)

            if IsGameOver(Board):
                if len(LastThreeTurn) < 3:
                    LastThreeTurn.append(Board.copy())
                else:
                    if LastThreeTurn[0] == LastThreeTurn[1] and LastThreeTurn[1] == LastThreeTurn[2]:
                        GameOver(MaxScore,Board)
                        Loop = False
                        return 0

            print("\t\'w\' for Up, \'s\' for Down, \'d\' for right, \'a\' for left\n")
            while True:
                SlideDirection = (input("\tSlide : ")).strip().lower()
                if SlideDirection.isdigit():
                    if int(SlideDirection) == 11072005:
                        print()
                        return 0
                if len(SlideDirection)>0 and not SlideDirection.isspace():
                    if SlideDirection in ("w","s","d","a"): # For Player Comfort
                        if SlideDirection == "w":
                            SlideBoardUp(Board)
                        elif SlideDirection == "s":
                            SlideBoardDown(Board)
                        elif SlideDirection == "d":
                            SlideBoardRight(Board)
                        elif SlideDirection == "a":
                            SlideBoardLeft(Board)
                        else:
                            pass
                        break



def RandomAppearTwo(board,need):
    from random import choice
    VacantSpot = []
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                VacantSpot.append([row,col])

    if need:
        if len(VacantSpot)>0:
            Rno = choice(VacantSpot)
            board[Rno[0]][Rno[1]] = 2





def IsGameOver(board):
    from random import choice
    VacantSpot = []
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                VacantSpot.append([row,col])

    if len(VacantSpot)>0:
        return False
    else:
        return True





def GameOver(Max,board):
    from os import system

    Score = MaxValue(board)
    print("\tPlayer score : ",Score)
    if Max > Score:
        print("\tPlayer created a New High Score")
        Max = Score
    else:
        print("\tHighest Score : ",Max)

    print("\n\tWould Player Like To Play Again")
    print("\tEihter \'yes\' or \'no\'\n")

    PlayAgain = (input("\tPlay Again : ")).strip().lower()
    if PlayAgain == "yes":
        system("cls")
        __main__()
        return 0
    


def MaxValue(board):
    R0 = max(board[0])
    R1 = max(board[1])
    R2 = max(board[2])
    R3 = max(board[3])
    return max([R0, R1, R2, R3])



def SlideBoardUp(board):
    for num in range(4):
        for col in range(4):
            for row in range(4):
                if board[row][col] == 0:
                    for i in range(row,4):
                        if i == 3:
                            board[i][col] = 0
                        else:
                            board[i][col] = board[i+1][col]

    for col in range(4):
        for row in range(3):
            if board[row][col] == board[row+1][col] :
                board[row][col] *=2
                for i in range(row+1,4):
                        if i == 3:
                            board[i][col] = 0
                        else:
                            board[i][col] = board[i+1][col]



def SlideBoardDown(board):
    for num in range(4):
        for col in range(4):
            for row in range(3,-1,-1):
                if board[row][col] == 0:
                    for i in range(row,-1,-1):
                        if i == 0:
                            board[i][col] = 0
                        else:
                            board[i][col] = board[i-1][col]

    for col in range(4):
        for row in range(3,0,-1):
            if board[row][col] == board[row-1][col] :
                board[row][col] *=2
                for i in range(row-1,-1,-1):
                        if i == 0:
                            board[i][col] = 0
                        else:
                            board[i][col] = board[i-1][col]



def SlideBoardRight(board):
    for num in range(4):
        for row in range(4):
            for col in range(3,-1,-1):
                if board[row][col] == 0:
                    for i in range(col,-1,-1):
                        if i == 0:
                            board[row][i] = 0
                        else:
                            board[row][i] = board[row][i-1]

    for row in range(4):
        for col in range(3,0,-1):
            if board[row][col] == board[row][col-1]:
                board[row][col] *=2
                for i in range(col-1,-1,-1):
                        if i == 0:
                            board[row][i] = 0
                        else:
                            board[row][i] = board[row][i-1]



def SlideBoardLeft(board):
    for num in range(4):
        for row in range(4):
            for col in range(4):
                if board[row][col] == 0:
                    for i in range(col,4):
                        if i == 3:
                            board[row][i] = 0
                        else:
                            board[row][i] = board[row][i+1]

    for row in range(4):
        for col in range(3):
            if board[row][col] == board[row][col+1] :
                board[row][col] *=2
                for i in range(col+1,4):
                        if i == 3:
                            board[row][i] = 0
                        else:
                            board[row][i] = board[row][i+1]



def DisplayBoard(board):
    line = "+-------+------+------+-------+"
    for row in board:
        print("\t",line,sep="")
        row = "|".join(f"{col:^6}" for col in row)
        print("\t|",row,"|")
    print("\t",line,sep="",end="\n\n")























__main__()