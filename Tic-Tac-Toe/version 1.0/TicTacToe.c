#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>  // For sleep function

#define SIZE 3

void DisplayBoard(char board[SIZE][SIZE]);
int NumToSpot(int Num, int *row, int *col);
void VacantSpot(char board[SIZE][SIZE], int spots[SIZE*SIZE][2], int *count);
void UpdatingBoard(char turn, int Num, char board[SIZE][SIZE]);
char CheckBoard(char board[SIZE][SIZE]);
char CheckBoardVertically(char board[SIZE][SIZE]);
char CheckBoardHorizontally(char board[SIZE][SIZE]);
char CheckBoardDiagonally(char board[SIZE][SIZE]);

int main() {
    char Board[SIZE][SIZE] = {{'=', '=', '='}, {'=', '=', '='}, {'=', '=', '='}};
    char KeyPad[SIZE][SIZE] = {{'7', '8', '9'}, {'4', '5', '6'}, {'1', '2', '3'}};

    printf("\n\t~ Welcome To Game Of Tic-Tac-Toe\n");
    printf("\t~ Will You Train Against The Ai Or Duel With Another Warrior\n");
    printf("\t~ Choose Between \"ai\" OR \"dual\"\n");

    char mode[10];
    while (1) {
        printf("\t_ MODE : ");
        gets(mode);
        if (strcmp(mode, "ai") == 0 || strcmp(mode, "dual") == 0) {
            break;
        }
    }

    srand(time(0));
    char Turn = (rand() % 2) == 0 ? 'O' : 'X';
    char Player = Turn;
    int Loop = 1;

    while (Loop) {
        system("cls");

        DisplayBoard(Board);
        DisplayBoard(KeyPad);

        char Winner = CheckBoard(Board);
        if (Winner != '\0') {
            if (strcmp(mode, "dual") == 0) {
                printf("\t~ For The Winner : Victory Is Yours! Well Played\n");
                printf("\t~ For The Loser : Keep Practicing! Every Defeat Is A Step Toward Mastery\n");
            } else if (strcmp(mode, "ai") == 0) {
                if (Winner == Player) {
                    printf("\t~ Victory Over The Ai! Your Skill Has Prevailed\n");
                } else {
                    printf("\t~ DEFEATED BY The Ai, Use This Setback As Fuel For Your Next Challenge\n");
                }
            }

            printf("\n\t~ Ready For Another Challenge\n");
            printf("\t~ Type \"yes\" For Rematch\n");
            printf("\n\t~ Your Choice : ");
            char again[10];
            scanf("%s", again);
            if (strcmp(again, "yes") == 0) {
                system("cls");
                main();
                return 0;
            } else {
                return;
            }
        }

        if (Turn == Player || strcmp(mode, "dual") == 0) {
            int Option;
            printf("\t~ Player %c : ", Turn);
            scanf("%d", &Option);
            if (Option >= 1 && Option <= 9) {
                int row, col;
                NumToSpot(Option, &row, &col);
                if (Board[row][col] == '=') {
                    UpdatingBoard(Turn, Option, Board);
                    Turn = (Turn == 'O') ? 'X' : 'O';
                }
            }
        } else {
            int AiOption;
            printf("\t~ Player %c : ", Turn);
            while (1) {
                AiOption = (rand() % 9) + 1;
                int row, col;
                NumToSpot(AiOption, &row, &col);
                if (Board[row][col] == '=') {
                    sleep(2);
                    printf("%d\n", AiOption);
                    sleep(2);
                    UpdatingBoard(Turn, AiOption, Board);
                    Turn = (Turn == 'O') ? 'X' : 'O';
                    break;
                }
            }
        }
    }
}

void DisplayBoard(char board[SIZE][SIZE]) {
    printf("\n");
    int i, j;
    for (i = 0; i < SIZE; i++) {
        printf("\t");
        for (j = 0; j < SIZE; j++) {
            if (j < SIZE - 1) {
                printf("%c  |  ", board[i][j]);
            } else {
                printf("%c", board[i][j]);
            }
        }
        printf("\n");
    }
    printf("\n");
}

int NumToSpot(int Num, int *row, int *col) {
    switch (Num) {
        case 1: *row = 2; *col = 0; break;
        case 2: *row = 2; *col = 1; break;
        case 3: *row = 2; *col = 2; break;
        case 4: *row = 1; *col = 0; break;
        case 5: *row = 1; *col = 1; break;
        case 6: *row = 1; *col = 2; break;
        case 7: *row = 0; *col = 0; break;
        case 8: *row = 0; *col = 1; break;
        case 9: *row = 0; *col = 2; break;
        default: return 0;
    }
    return 1;
}

void VacantSpot(char board[SIZE][SIZE], int spots[SIZE*SIZE][2], int *count) {
    *count = 0;
    int i, j;
    for (i = 0; i < SIZE; i++) {
        for (j = 0; j < SIZE; j++) {
            if (board[i][j] == '=') {
                spots[*count][0] = i;
                spots[*count][1] = j;
                (*count)++;
            }
        }
    }
}

void UpdatingBoard(char turn, int Num, char board[SIZE][SIZE]) {
    int row, col;
    if (NumToSpot(Num, &row, &col)) {
        board[row][col] = turn;
    }
}

char CheckBoard(char board[SIZE][SIZE]) {
    char x = CheckBoardVertically(board);
    char y = CheckBoardHorizontally(board);
    char z = CheckBoardDiagonally(board);

    if (x != '\0') return x;
    if (y != '\0') return y;
    if (z != '\0') return z;

    return '\0';
}

char CheckBoardVertically(char board[SIZE][SIZE]) {
	int i;
    for ( i = 0; i < SIZE; i++) {
        if (board[0][i] != '=' && board[0][i] == board[1][i] && board[1][i] == board[2][i]) {
            return board[0][i];
        }
    }
    return '\0';
}

char CheckBoardHorizontally(char board[SIZE][SIZE]) {
	int i;
    for ( i = 0; i < SIZE; i++) {
        if (board[i][0] != '=' && board[i][0] == board[i][1] && board[i][0] == board[i][2]) {
            return board[i][0];
        }
    }
    return '\0';
}

char CheckBoardDiagonally(char board[SIZE][SIZE]) {
    if (board[0][0] != '=' && board[0][0] == board[1][1] && board[0][0] == board[2][2]) {
        return board[1][1];
    } else if (board[0][2] != '=' && board[0][2] == board[1][1] && board[0][2] == board[2][0]) {
        return board[1][1];
    }
    return '\0';
}



