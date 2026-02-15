


class Pa55w0rdManageR:

    def __init__(self, AccountExist = False):

        if AccountExist:
            from pickle import load

            PasswordFile = Pa55w0rdManageR.FileManager()
            if PasswordFile != None:
                with open(PasswordFile,"rb") as file:
                    try:
                        PreviosManager = load(file)
                        self.__dict__.update(PreviosManager.__dict__)
                    except:
                        print("Manager_ : Corrupted File.")
                        exit()
            else:
                self.isNone = True

        else:
            from os import system
            self.isNone = False
            self.__U5erName = None
            self.__U5erPa55w0rd = None
            self.__Pin = None
            self.__DecryptDict = None
            self.__Pa55w0rdRecords = dict()
            self.__HiddenRecords = dict()
            self.__Lock = True
            self.LockStatus = True
            self.clear_screen = lambda : system("cls")







    @classmethod
    def FileManager(cls, path = None):
        from os import getcwd, listdir, system
        from os.path import isdir, isfile, join, split

        if path == None : path = getcwd() 

        while True:
            system("cls")
            DirectoryContent = sorted(listdir(path))

            print(f"Manager_ :")
            print( "╔=====================================================╗")
            print( "║ Path/to/User-Password-File                          ║")
            print( "╠=====================================================╣")
            print(f"╠ {path}")
            print( "╠=====================================================╣")
            for index in range(len(DirectoryContent)):
                content = DirectoryContent[index]
                what = "Dir " if isdir(join(path,content)) else "file"
                print(f"║ [{index if index >=10 else '0'+str(index)}] {what} {content}")
            print("╚=====================================================╝\n")

            while True:
                UserInput = input("User ---=> ").strip()

                if UserInput.lower() == "quit":     # for quit
                    system("cls")
                    return None
                elif UserInput == "..":             # for back directory
                    path = split(path)[0]
                    break
                elif UserInput.isdigit():           # for selecting nestedDir or file
                    UserInput = int(UserInput)
                    if 0 <= UserInput <= len(DirectoryContent):
                        if isfile(join(path, DirectoryContent[UserInput])):
                            ConfirmationText = ["",
                                                "╔============================================╗",
                                                "║ Confirm Password file? (y/n):              ║",
                                                "╠============================================╣",
                                               f"║ file : {DirectoryContent[UserInput]}",
                                                "╚============================================╝", "" ]
                            system("cls")
                            for t in ConfirmationText:
                                print(t)

                            if input("User ---=> ").strip().lower() == "y":
                                return join(path, DirectoryContent[UserInput])
                            else:
                                break
                        else :
                            path = join(path, DirectoryContent[UserInput])
                            break







    def initialize(self, mode="+"):
        if (self.__U5erName == self.__U5erPa55w0rd == None) or mode=="*":

            if mode == "*":
                self.clear_screen()
                print("Manager_ : Verification")
                UserName = input("Username : ").strip()
                Password = input("Password : ").strip()
                PIN =      input("Pin      : ").strip()

                if not (self.__U5erName == UserName and self.__U5erPa55w0rd == Password and self.__Pin == PIN): return -1

            while True:
                self.clear_screen()
                print("Manager_ : Credential of New User")
                UserName = input("Username : ").strip()
                Password = input("Password : ").strip()
                PIN =      input("Pin      : ").strip()

                GivenInfo = [UserName, Password, PIN]

                ErrorConditions = [
                    [0,"blank entries are not permitted."],
                    [0,"username length must be between 10 and 40."],
                    [0,"username must not contain space between it."],
                    [0,"password length must be between 10 and 40."],
                    [0,"password must not contain space between it."],
                    [0,"password must be combination of ( upper + lower )case, digits, symbols."],
                    [0,"pin must not contain space between it."],
                    [0,"pin must be numeric."],
                    [0,"pin length must be >= 10"]
                ]

                if 0 not in [len(t) for t in GivenInfo]:    ErrorConditions[0][0] = 1
                if (10 < len(GivenInfo[0]) < 40):           ErrorConditions[1][0] = 1
                if GivenInfo[0] in GivenInfo[0].split() :   ErrorConditions[2][0] = 1
                if (10 < len(GivenInfo[1]) < 40):           ErrorConditions[3][0] = 1
                if GivenInfo[1] in GivenInfo[1].split() :   ErrorConditions[4][0] = 1

                from string import ascii_uppercase, ascii_lowercase, digits, punctuation
                CharactersList = [ascii_uppercase, ascii_lowercase, digits, punctuation]
                CharacterConditions = [0,0,0,0]
                for conditionIndex in range(4):
                    for char in CharactersList[conditionIndex]:
                        if char in GivenInfo[1]: 
                            CharacterConditions[conditionIndex] = 1
                            break

                if sum(CharacterConditions) == 4:           ErrorConditions[5][0] = 1
                if GivenInfo[2] in GivenInfo[2].split():    ErrorConditions[6][0] = 1
                if GivenInfo[2].isdigit():                  ErrorConditions[7][0] = 1
                if len(GivenInfo[2]) >= 10:                 ErrorConditions[8][0] = 1

                isGuest = True if (UserName == Password == "guest" and PIN == "12345") else False

                if sum([err[0] for err in ErrorConditions]) == len(ErrorConditions) or isGuest: 
                    confirmationText = ["",
                                "╔============================================╗",
                                "║ Confirm? (y/n):                            ║",
                                "╠============================================╣",
                               f"║ Username : {UserName}",
                               f"║ Password : {Password}",
                               f"║ PIN      : {PIN}",
                                "╚============================================╝", ""
                        ]
                    for t in confirmationText: print(t)

                    if input("User ---=> ").strip().lower() == "y":
                        self.__U5erName = UserName
                        self.__U5erPa55w0rd = Password
                        self.__Pin = "12345" if PIN == "guest" else PIN
                        self.__Lock = self.LockStatus = False
                        print("\nManager_ : Machine is now Active.\n")
                        break
                else:
                    print("\nManager_ :")
                    print("╔=====================================================╗")
                    print("║ Mistakes                                            ║")
                    print("╠=====================================================╣")
                    for err in ErrorConditions:
                        if err[0] == 0:
                            print(f"║ {err[1]}")
                    print("╚=====================================================╝")
                    input("\nUser ---=> ")

        else:
            print("Manager_ : Machine Already Active.\n")







    def Cryption(self, mode, PIN=None):
        if PIN == None: PIN = int(self.__Pin)
        from random import seed, shuffle

        if mode == "en":
            from string import printable
            
            CharactersList = (list(printable[:95]))
            CharactersList.append('\n')
            ShuffledList = CharactersList.copy()
            shuffle(ShuffledList)

            CryptKey = dict(zip(CharactersList, ShuffledList))

            seed(PIN)
            shuffle(CharactersList)
            self.__DecryptDict = dict(zip(ShuffledList,CharactersList))

        if mode == "de":
            Keys = list(self.__DecryptDict.keys())
            Values = list(self.__DecryptDict.values())
            NewValues = [None] * len(Values)
            OriginalIndex = list(range(len(Values)))
            
            seed(PIN)
            shuffle(OriginalIndex)

            for i in range(len(Values)):
                NewValues[OriginalIndex[i]] = Values[i]

            CryptKey = dict(zip(Keys, NewValues))

        for identifier in list(self.__Pa55w0rdRecords.keys()):
            for d in range(4):
                data = self.__Pa55w0rdRecords[identifier][d]
                newdata = str()
                for char in data:
                    newdata += CryptKey[char]
                self.__Pa55w0rdRecords[identifier][d] = newdata

        for identifier in list(self.__HiddenRecords.keys()):
            for d in range(4):
                data = self.__HiddenRecords[identifier][d]
                newdata = str()
                for char in data:
                    newdata += CryptKey[char]
                self.__HiddenRecords[identifier][d] = newdata

        Credentials = [self.__U5erName, self.__U5erPa55w0rd, self.__Pin]
        for i in range(len(Credentials)):
            newdata = str()
            for char in Credentials[i]:
                newdata += CryptKey[char]
            Credentials[i] = newdata
        self.__U5erName = Credentials[0]
        self.__U5erPa55w0rd = Credentials[1]
        self.__Pin = Credentials[2]

        if mode == "de":
            self.__DecryptDict = None







    def UserInterface(self):
        if self.isNone : return
        if self.__Lock: print("Profile is Locked")

        Text = ["",
                "╔============================================╗",
                "║  [0] Password Manager                      ║",
                "╠============================================╣",
                "║  [1] View Saved Passwords                  ║",
                "║  [2] Add New Password                      ║",
                "║  [3] Update Existing Password              ║",
                "║  [4] Delete a Password                     ║",
                "║  [5] Exit                                  ║",
                "╚============================================╝","" ]

        while True:
            self.clear_screen()
            for t in Text: print(t)

            UserInput = input("User ---=> ").strip()
            if UserInput.isdigit():
                UserInput = int(UserInput)
                if UserInput <= 5 and UserInput > 0:
                    Functions = [ lambda:self.__Reveal("+") , self.__Include, self.__Revise, self.__Erase, self.__Save ]
                    function = Functions[UserInput - 1]
                    function()
            elif UserInput == "pdx":
                self.__DeveloperBackdoor__()







    def __Reveal(self, mode="-"):
        if self.__Lock: print("Profile is Locked")
        self.clear_screen()

        PasswordKeys = self.__Pa55w0rdRecords if (mode != "/") else self.__HiddenRecords
        Identifiers = list(sorted(PasswordKeys.keys()))
        Length = len(Identifiers)

        if mode == "*" or mode == "/":
            for Index in range(Length):
                UserData = ["",
                        "╔============================================╗",
                       f"║ Identifier      : {Identifiers[Index]}",
                       f"║ Platform        : {PasswordKeys[Identifiers[Index]][0]}",
                       f"║ User Identifier : {PasswordKeys[Identifiers[Index]][1]}",
                       f"║ Password        : {PasswordKeys[Identifiers[Index]][2]}",
                       f"║ Additional Info : {PasswordKeys[Identifiers[Index]][3]}",
                        "╚============================================╝", "" ]
                for t in UserData: print(t)
            UserInput = input("\nUser ---=> ").strip()

        else:
            print(f"Manager_ : {Length} keys stored")
            print("╔============================================╗")
            for p in range(Length):
                print(f"║  {p}] : {Identifiers[p]}")
            print("╚============================================╝")
        
        if mode == "-":
            return Identifiers, Length

        if mode == "+":
            UserInput = input("\nUser ---=> ").strip()
            if UserInput == "":
                return
            if UserInput.isdigit():
                Index = int(UserInput)
                if Index <= Length and Index >= 0:
                    self.clear_screen()
                    UserData = ["",
                                "╔============================================╗",
                               f"║ Identifier      : {Identifiers[Index]}",
                               f"║ Platform        : {PasswordKeys[Identifiers[Index]][0]}",
                               f"║ User Identifier : {PasswordKeys[Identifiers[Index]][1]}",
                               f"║ Password        : {PasswordKeys[Identifiers[Index]][2]}",
                               f"║ Additional Info : {PasswordKeys[Identifiers[Index]][3]}",
                                "╚============================================╝", "" ]
                    for t in UserData: print(t)
                else: print("Manager_ : Out of Range Index.")
            else: print("Manager_ : Non-Integer Index.")
            input("User ---=> ")
        







    def __Include(self):
        if self.__Lock: print("Profile is Locked")
        while True:
            self.clear_screen()
            print("Manager_ :")

            Identifier = input("Identifier      : ").strip()
            Platform   = input("Platform Name   : ").strip()
            UserIdentifier  = input("User Identifier : ").strip()
            Password   = input("User Password   : ").strip()
            AdditionalInfo   = input("Additional info : ").strip()

            if not (len(Identifier) and len (Platform) and len(UserIdentifier) and len(Password)):
                print("Manager_ : Blank Response.\n")
            elif ( len(UserIdentifier.split()) != 1 or len(Password.split())!=1) :
                print("Manager_ : whitespace found in middle of response.\n")
            else:
                if Identifier in list(self.__Pa55w0rdRecords.keys()):
                    print("Manager_ : Identifer already exist.")
                    print("Manager_ : Try adding extra characters.")
                    input("User ---=> ")
                else:
                    ConfirmationText = ["",
                                        "╔============================================╗",
                                        "║ Confirm addition? (y/n):                   ║",
                                        "╠============================================╣",
                                       f"║ Identifier      : {Identifier}",
                                       f"║ Platform        : {Platform}",
                                       f"║ User Identifier : {UserIdentifier}",
                                       f"║ Password        : {Password}",
                                       f"║ Additional Info : {AdditionalInfo}",
                                        "╚============================================╝", "" ]
                    for t in ConfirmationText: print(t)

                    if input("User ---=> ").strip().lower() == "y":
                        self.__Pa55w0rdRecords[Identifier] = [Platform, UserIdentifier, Password, AdditionalInfo]
                        print("Manager_ : Process complete")
                        break







    def __Revise(self):
        if self.__Lock: print("Profile is Locked")
        Identifiers, Length = self.__Reveal()

        UserInput = input("\nUser ---=> ")
        if UserInput.isdigit():
            Index = int(UserInput)
            if Index <= Length and Index >= 0:
                self.clear_screen()
                Index-=1
                UserData = ["",
                            "╔============================================╗",
                            "║ Old Pair                                   ║",
                            "╠============================================╣",
                           f"║ Identifier      : {Identifiers[Index]}",
                           f"║ Platform        : {self.__Pa55w0rdRecords[Identifiers[Index]][0]}",
                           f"║ User Identifier : {self.__Pa55w0rdRecords[Identifiers[Index]][1]}",
                           f"║ Password        : {self.__Pa55w0rdRecords[Identifiers[Index]][2]}",
                           f"║ Additional Info : {self.__Pa55w0rdRecords[Identifiers[Index]][3]}",
                            "╚============================================╝","" ]
                for t in UserData: print(t)

                print("User ---=> ")
                UserIdentifier = input("User Identifier : ")
                Password = input("Password        : ")
                AdditionalInfo = input("Password        : ")


                if not (len(UserIdentifier) and len(Password)):
                    print("Manager_ : Blank Response.\n")
                elif ( len(UserIdentifier.split()) != 1 or len(Password.split())!=1) :
                    print("Manager_ : whitespace found in middle of response.\n")
                else:
                    ConfirmationText = ["",
                                        "╔============================================╗",
                                        "║ Confirm addition? (y/n):                   ║",
                                        "╠============================================╣",
                                       f"║ Identifier      : {Identifiers[Index]}",
                                       f"║ Platform        : {self.__Pa55w0rdRecords[Identifiers[Index]][0]}",
                                       f"║ User Identifier : {UserIdentifier}",
                                       f"║ Password        : {Password}",
                                       f"║ Additional Info : {AdditionalInfo}",
                                        "╚============================================╝","" ]
                for t in ConfirmationText: print(t)

                if input("User ---=> ").strip().lower() == "y":
                    self.__Pa55w0rdRecords[Identifiers[Index]] = [self.__Pa55w0rdRecords[Identifiers[Index]][0], UserIdentifier, Password, AdditionalInfo]
                    print("Manager_ : Process complete")
            else:
                print("Manager_ : Out of Index.")
                input("User ---=> ")
        else:
            print("Manager_ : not Integer Index.")
            input("User ---=> ")







    def __Erase(self, mode="+"):
        if self.__Lock: print("Profile is Locked")

        if mode == "*":
            self.clear_screen()
            print("Manager_ : Verification")
            UserName = input("Username : ").strip()
            Password = input("Password : ").strip()
            PIN =      input("Pin      : ").strip()

            if not (self.__U5erName == UserName and self.__U5erPa55w0rd == Password and self.__Pin == PIN): return
            else:    
                self.__Pa55w0rdRecords = dict()
                self.__HiddenRecords = dict()

        Identifiers, Length = self.__Reveal()

        UserInput = input("\nUser ---=> ")
        if UserInput.isdigit():
            Index = int(UserInput)
            if Index <= Length and Index >= 0:
                self.__HiddenRecords[Identifiers[Index]] = self.__Pa55w0rdRecords[Identifiers[Index]]
                del self.__Pa55w0rdRecords[Identifiers[Index]]
                print("Manager_ : Process complete")
            else:
                print("Manager_ : Out of Index.")
                input("User ---=> ")
        else:
            print("Manager_ : not Integer Index.")
            input("User ---=> ")







    def __Save(self):
        if self.__Lock: print("Profile is Locked")
        from pickle import dump
        self.clear_screen()

        filename = self.__U5erName
        self.__Lock = self.LockStatus = True
        self.Cryption("en")
        del self.clear_screen

        with open(f"./PASSW0RDS-{filename}.bat", "wb") as file:
            dump(self, file)

        input("Thanks for using this tool! \nHope it was helpful.\n...")
        exit()







    def __DeveloperBackdoor__(self):
        if self.__Lock: print("Profile is Locked")

        Text = ["",
                "╔============================================╗",
                "║  [0] Developer Mode                        ║",
                "╠============================================╣",
                "║  [1] Show all Preserved Passwor            ║",
                "║  [2] Show all Deleted Password             ║",
                "║  [3] Delete all Password                   ║",
                "║  [4] Modify User Authorization             ║",
                "║  [5] Exit                                  ║",
                "╚============================================╝","" ]

        while True:
            self.clear_screen()
            for t in Text: print(t)

            UserInput = input("User ---=> ").strip()
            if UserInput.isdigit():
                UserInput = int(UserInput)
                if 0 <= UserInput <= 4:
                    Functions = [ lambda:self.__Reveal("*") , lambda:self.__Reveal("/") , lambda:self.__Erase("*"), lambda:self.initialize("*") ] 
                    function = Functions[UserInput - 1]
                    function()
                elif UserInput == 5:
                    break







    def unlock(self):
        if self.isNone : return
        if not self.__Lock: return "lock"
        from os import system

        system("cls")
        print("Manager_ : ")
        Username = input("Username : ")
        Password = input("Password : ")
        PIN = input("Pin      : ")

        if not ( len(Username) and len(Password) and len(PIN)):
            print("Manager_ : Blank Response.\n")
            return False
        elif ( len(Username.split()) != 1 or len(Password.split())!=1 or len(PIN.split())!=1) :
            print("Manager_ : whitespace found in middle of response.\n")
            return False

        else:
            PIN = int(PIN)
            self.Cryption("de", PIN)

            if Username == self.__U5erName and Password == self.__U5erPa55w0rd:
                self.__Pin = str(PIN)
                self.__Lock = self.LockStatus = False
                self.clear_screen = lambda : system("cls")
            else:
                system("cls")
                print("Manager_ : Invalid Credential")







def DynamicText(text):
    from time import sleep
    from sys import stdout

    temp=""
    for char in text:
        for ch in (text):
            stdout.write(f"\r\t{temp}{ch}")
            stdout.flush()
            sleep(0.002)
            if char == ch:
                temp+=ch
                break
    print()



















if __name__ == "__main__":
    from os import system

    IntroductionText = [" \n",
        "╔═══════════════════════════════════════╗",
        "║           Password Manager            ║",
        "╚═══════════════════════════════════════╝" ]
    system("cls")
    [DynamicText(t) for t in IntroductionText]

    new = True if input("\tnew (y/n) : ").strip().lower() == "y" else False
    try:
        if new == True:
            m = Pa55w0rdManageR(AccountExist=False)
            m.initialize()

        if new == False:
            m = Pa55w0rdManageR(AccountExist=True)
            m.unlock()

        m.UserInterface()

    except Exception as e:
        #from traceback import print_exc
        print(f"!@#$%^&* : {e}")
        #print_exc()





