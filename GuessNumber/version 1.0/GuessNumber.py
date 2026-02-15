
def __main__():
    from random import randint , choice
    from os import system
    from time import sleep

    system("cls")
    
    print("\n\tWelcome Player In Guess a Number.\t(⌐■_■)\n")
    print("\t1. Easy\n\t2. Intermediate\n\t3. Hard\n")#11 for insane

    mode = (input("\tmode : ")).strip().lower()

    if not mode.isdigit():
        Modes = {"easy":"1", "intermediate" :"2", "hard":"3", "insane":"11"}
        if mode in Modes:
            mode = Modes[mode]

    if mode.isdigit():
        mode = int(mode)
        if mode > 0 and mode < 4 or mode == 11:
            system("cls")
            if mode == 1:
                MinPossibleNo = randint(1,40)
                MaxPossibleNo = randint(70,100)
                print("\n\t","■⟬  Mode : Easy  ⟭■".center(30,"="))
            elif mode == 2:
                MinPossibleNo = randint(100,400)
                MaxPossibleNo = randint(700,1000)
                print("\n\t","■⟬  Mode : Intermediate  ⟭■".center(30,"="))
            elif mode == 3:
                MinPossibleNo = randint(1000,4000)
                MaxPossibleNo = randint(7000,10000)
                print("\n\t","■⟬  Mode : Hard  ⟭■".center(30,"="))
            elif mode == 11:
                MinPossibleNo = randint(100000,4000000)
                MaxPossibleNo = randint(7000000,10000000)
                print("\n\t","■⟬  Mode : Insane  ⟭■".center(30,"="))
            else:
                pass
                
            Required_No = randint(MinPossibleNo,MaxPossibleNo)
            print("\n\tI have selected a number between ",MinPossibleNo," and ",MaxPossibleNo)
            print("\tCan you guess it?")
            
            Time_For_Game_Over = False
            Attempts = 0
            Guess = 0
            NearRightSideNo = MinPossibleNo
            NearLeftSideNo = MaxPossibleNo
            
            GuessList = list()
            GuessList.extend([Required_No,MinPossibleNo,MaxPossibleNo])
            
            while Time_For_Game_Over == False:
                Guess = (input("\n\tEnter Your Guess : ")).strip()

                if Guess == "ll07":
                    print("\tHelp : The Number is between",NearRightSideNo,"and",NearLeftSideNo) # Help
                elif Guess == "ll072005":
                    print("\tSecret : The required no is : ",Required_No) #Cheat

                elif Guess.isdigit():
                    Expression = ["(►__◄)", "◑﹏◐", "(. ❛ ᴗ ❛.)", "(っ´Ι`)っ", "(╬▔皿▔)╯", "～(　TロT)", "σ(ㆆ_ㆆ)", "(^◕.◕^)", "(。﹏。*)", "(＠_＠;)", "♨︎_♨︎", "⊙﹏⊙∥", "ಥ_ಥ", "(┬┬﹏┬┬)", "〒▽〒"]
                    Guess = int(Guess)
                    
                    if (Guess < MaxPossibleNo and Guess > MinPossibleNo):
                        GuessList.append(Guess)
                    GuessList = list(set(GuessList))
                    GuessList.sort()
                    ReqIndex = GuessList.index(Required_No)
                    NearRightSideNo = GuessList[ReqIndex-1]
                    NearLeftSideNo = GuessList[ReqIndex+1]

                    if Guess < Required_No:
                        print("\tToo Low, Try Again.\t",(choice(Expression)).center(15))
                    elif Guess > Required_No:
                        print("\tToo High, Trt Again.\t",(choice(Expression)).center(15))
                    else:
                        print("\n\tCongratulation! You guess the number in",Attempts,"attempts    👈(ﾟヮﾟ👈)    ")
                        Time_For_Game_Over = True

                    Attempts += 1
                else:
                    print("\t"," "*25,"(+_+)?".center(10))    #(+_+)? #(⊙_⊙)？
                    
            PlayAgain = (input("\n\n\tWould You Like To Play Again (yes/no): ")).strip().lower()
            if PlayAgain =="yes":
                system("cls")
                print("\n\tStarting a new game...")
                __main__()
                return
            else:
                system("cls")
                print("\n\tThank You For Your Precious Time. ")
                print("\tI Hope You Enjoy This.")
                sleep(5)

        else: 
            print("\n\tX﹏X\n")
            sleep(5)

    else: 
        print("\n\tX﹏X\n")
        sleep(5)





    
__main__()


    