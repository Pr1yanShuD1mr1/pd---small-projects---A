


def __main__():
    from random import choice
    from time import sleep
    from os import system

    Board = [["=","=","="],["=","=","="],["=","=","="]]
    KeyPad = [["7","8","9"],["4","5","6"],["1","2","3"]]

    print("\n\t~ Welcome To Game Of Tic-Tac-Toe\n")
    print("\t~ Will You Train Against The Ai Or Duel With Another Warrior")
    print("\t~ Choose Btw \"ai\" OR \"dual\"\n")

    while True:
        mode = input("\t_ MODE : ").strip().lower()
        if mode == "ai" or mode == "dual":
            break

    Turn = choice(["O","X"])
    Player = Turn
    Loop = True
    while Loop:
        system("cls")

        DisplayBoard(Board)
        DisplayBoard(KeyPad)

        Winner = CheckBoard(Board)
        if Winner != None:
            if mode == "dual":
                print("\t~ For The Winner : Victory Is Your! Well Played")
                print("\t~ For The Loser : Keep Practicing! Every Defeat Is Step Toward Mastery")
            elif mode == "ai":
                if Winner == Player:
                    print("\t~ Victory Over The Ai! Your Skill Have Prevailed")
                else:
                    print("\t~ DEFEATED BY The Ai, Use THis Setback As Fuel For Your Next Challenge")
                    
            print("\n\t~ Ready For Another Challenge")
            print("\t~ Type \"yes\" For Rematch")
            print("\n\t~ Your Choice : ",end="")
            again = (input()).strip().lower()
            if again == "yes":
                system("cls")
                __main__()
                return
            else:
                return

        if Turn == Player or mode == "dual":
            Text = "\t~ Player " + Turn +" : "
            Option = input(Text)
            if Option.isdigit():
                Option = int(Option)
                if Option>0 and Option<10:
                    Spot = NumToSpot(Option)
                    if Spot in VacantSpot(Board):
                        UpdatingBoard(Turn,Option,Board)
                        if Turn == "O":
                            Turn = "X"
                        else:
                            Turn = "O"
                            
        else: #there is somthing wrong with ai mode
            Ai = True
            Text = "\t~ Player " + Turn +" : "
            while Ai:
                AiOption = choice([1,2,3,4,5,6,7,8,9])
                Spot = NumToSpot(AiOption)
                if Spot in VacantSpot(Board):
                        print(Text,end="")
                        sleep(1)
                        print(AiOption)
                        sleep(1)
                        UpdatingBoard(Turn,AiOption,Board)
                        if Turn == "O":
                            Turn = "X"
                        else:
                            Turn = "O"
                Ai = False


def DisplayBoard(board):
    print()
    for i in board:
        Rcount = 0
        print("\t",end="")
        for j in i:
            if Rcount<2:
                print(j,"  |  ",sep="",end="")
            else:
                print(j,end="")
            Rcount+=1
        print()
    print()


def NumToSpot(Num):
    NumDict = {1:[2,0],2:[2,1],3:[2,2],4:[1,0],5:[1,1],6:[1,2],7:[0,0],8:[0,1],9:[0,2]}
    return NumDict[Num]


def VacantSpot(board):
    List = []
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == "=":
                List.append([i,j])
    return List


def UpdatingBoard(turn,Num,board):
    Spot = NumToSpot(Num)
    board[Spot[0]][Spot[1]] = turn


def CheckBoard(board):
    x = CheckBoardVertically(board)
    y= CheckBoardHorizontally(board)
    z = CheckBoardDiagonally(board)

    if x != None:
        return x
    if y != None:
        return y
    if z != None:
        return z


def CheckBoardVertically(board):
    for i in range(3):
        if board[0][i] != "=":
            if board[0][i] == board[1][i]:
                if board[1][i] == board[2][i]:
                    return board[0][i]


def CheckBoardHorizontally(board):
    for i in range(3):
        if board[i][0] != "=":
            if board[i][0] == board[i][1]:
                if board[i][0] == board[i][2]:
                    return board[i][0]


def CheckBoardDiagonally(board):
    if board[0][0] != "=":
        if board[0][0] == board[1][1]:
            if board[0][0] ==board[2][2]:
                return board[1][1]
    elif board[0][2] != "=":
        if board[0][2] == board[1][1]:
            if board[0][2] == board[2][0]:
                return board[1][1]





__main__()













