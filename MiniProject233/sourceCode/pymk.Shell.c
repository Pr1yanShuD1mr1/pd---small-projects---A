#include <stdio.h>
#include <string.h> 
#include "pymk.Core.c"




char IntroductionUI(void);
US3R LoginUI(void);
US3R SigninUI(void);
void updateAttributes(US3R user);
void showAttributes(US3R user);
void startGuide(void);
int invokeCommand(US3R *user, char tokens[][10], int nt);
int request(US3R user);
void showFriends(US3R user);
void RecommendFriend(US3R user);


struct {
	char (*IntroductionUI)(void);
	US3R (*LoginUI)(void);
	US3R (*SigninUI)(void);
	void (*updateAttributes)(US3R user);
	void (*showAttributes)(US3R user);
	void (*startGuide)(void);
	int (*invokeCommand)(US3R *user, char tokens[][10], int nt);
	int (*request)(US3R user);
	void (*showFriends)(US3R user);
	void (*RecommendFriend)(US3R user);
	
}

pymkShell = {
	IntroductionUI,
	LoginUI, 
	SigninUI,
	updateAttributes,
	showAttributes,
	startGuide,
	invokeCommand,
	request,
	showFriends,
	RecommendFriend
};





struct{
	char Reset[9], Blink[8], Invisible[8];

	struct{ char Bold[8], Italic[8], Underline[8], Strike[8]; } format;
	struct{ char Green[8], Yellow[8], Red[8]; } color; 
	struct{ char Blue[8]; } background;
	struct{ char Hide[8], Show[8]; 
		struct{ char up[8], left[8]; } move ;
	} cursor;
}

TextEffects = {
	"\033[0m", "\033[5m", "\033[8m", 
	{"\033[1m", "\033[2m", "\033[4m", "\033[9m"}, 
	{"\033[92m", "\033[33m", "\033[31m"}, 
	{"\033[44m"}, 
	{"\033[?25l", "\33[?25h" , 
		{"\033[A", "\033[D"}
	}
};





char IntroductionUI(void){	
	sprintf(currentInterface, "Introduction");

	char *InitialLogo[] = {
	"                                               ",
	"    +---------------------------------------+  ",
	"    |       <<-people-you-may-know->>       |  ",
	"    +---------------------------------------+  ",
	"    Loading...                                 "};

	system("cls");
	printf(TextEffects.cursor.Hide);
	printf("%s%s", TextEffects.format.Bold, TextEffects.color.Green);		// Give Green Bold Italic font.
	
	int i, j, k;
	int lowerlimit = 32, upperlimit = 127;		// Range of Printable i.e. ( digit, lowercase, uppercase, symbol )
	for (i = 0; i<5; i++){
		if (i==4){ printf("%s%s%s", TextEffects.format.Bold ,TextEffects.Blink, TextEffects.color.Yellow); }    // Blink in yellow at 5 row
		for(j=0; j<46; j++){
			for(k=lowerlimit; k<upperlimit; k++){
				printf("%c", InitialLogo[i][j]);
				printf(TextEffects.cursor.move.left);
				if (k == InitialLogo[i][j]){
					printf("%c", InitialLogo[i][j]);	
				} 
			}
		} printf("\n");
	}

	printf(TextEffects.Invisible);
	getchar(); 
	fflush(stdin);
	printf("%s%s%s%s", TextEffects.cursor.move.up, TextEffects.cursor.move.up, "\033[2K", TextEffects.Reset); 	// Clear a line
	printf("    new (y/n) : %s", TextEffects.cursor.Show);
	char isNewUser = getchar(); 
	fflush(stdin);
	system("cls");
	return isNewUser;
}





US3R LoginUI(void){
	sprintf(currentInterface, "Login");
	US3R user;

	system("cls");
	int attempts = 3;
	while(attempts>0){				
		printf("$ Login %d\n", attempts);

		printf("$ Username : ");
		fgets(user.name, sizeof(user.name), stdin);
		fflush(stdin);

		printf("$ Password : ");
		fgets(user.UUId, sizeof(user.UUId), stdin);
		fflush(stdin);

		// to overcome logic error that occur in verification, cause is unknown.
		if (strlen(user.UUId)<8){ user.UUId[strlen(user.UUId)-1] = '\0'; }
		else{ user.UUId[strlen(user.UUId)] = '\0'; }
		user.name[strlen(user.name)-1] = '\0';			

		system("cls");
		if (pymkCore.verifyuser(user)==1){
			user.status = 1;
			sprintf(user.role, "user");
			break;
		}else{ attempts--; }
	}
	
	if (attempts==0){
		sprintf(user.UUId, "none");
		sprintf(user.name, "none");
		sprintf(user.role, "none");
		user.status = -1;
	}

	return user;
}





US3R SigninUI(void){
	sprintf(currentInterface, "Signin");
	US3R user;
	
	sprintf(user.role, "NONE");
	user.status = -1;
	
	char *confirmationText[] = {
	"    Manager_                                   ",
	"    +---------------------------------------+  ",
	"    | Confirm? (y/n)                        |  ",
	"    +---------------------------------------+  "};

	int i, j;
	char userConfirm;
	while(1){
		system("cls");
		printf("$ Signin \n");
		printf("$ Username : ");
		
		fgets(user.name, sizeof(user.name), stdin);
		user.name[strcspn(user.name, "\n")] = '\0';
		pymkCore.genId(user.UUId);		// generate a user-id
		fflush(stdin);

		system("cls");
		for (i = 0; i<4; i++){
			for(j=0; j<46; j++){
				printf("%c", confirmationText[i][j]);
			} printf("\n");
		}

		printf("    | User Id  : %s \n", user.UUId);
		printf("    | Username : %s \n", user.name);
		printf("%s \n", confirmationText[1]);
		printf("    user ---=> ");

		userConfirm = getchar();
		system("cls");
		fflush(stdin);

		if (userConfirm == 'y'){
			sprintf(user.role, "user");
			user.status = 1;
			pymkCore.userInit(user); 
			break;
		} 
		else if (userConfirm == 'q'){ // for exit without user initialisation.
			sprintf(user.UUId, "none");
			sprintf(user.name, "none");
			sprintf(user.role, "none");
			user.status = -1;
			break;
		}
	}
	if (userConfirm != 'q'){ pymkShell.updateAttributes(user); }
	return user;
}





void updateAttributes(US3R user){
	sprintf(currentInterface, "updateAttributes");

	char gender;
	int age;
	char occupation[20];
	char city[20];
	
	char fileName[50];
	sprintf(fileName, "%s/%s/%s", "../systemFiles/Users", user.UUId, "attributes.txt");

	int i;
	char userConfirm = 0;
	char *Text[] = {
	"    Manager_ : user_information                ",
	"    +---------------------------------------+  ",
	"    | gender      : ",
	"    | age         : ",
	"    | occupation  : ",
	"    | city        : ",
	"    +---------------------------------------+  "};

	while(1){
		system("cls");
		fflush(stdin);

		printf("$ user_information \n");

		printf("$ gender (m/f) : ");	scanf("%c", &gender);
		printf("$ age          : ");	scanf("%d", &age);
        while ((i = getchar()) != '\n' && i != EOF);  // clear input buffer caused by above input. specially newline character, that was ledt by above two input

		//												    remove the trailing newline left by gets
		printf("$ occupation   : ");	gets(occupation);	occupation[strcspn(occupation, "\n")] = '\0';
		printf("$ city         : ");	gets(city);			city[strcspn(city, "\n")] = '\0';
		
		system("cls");
		for(i=0; i<7; i++){
			printf("%s", Text[i]);
			switch (i){
				case 2: printf("'%c'", gender);    break;
				case 3:	printf("'%d'", age);    break;
				case 4: printf("'%s'", occupation);    break;
				case 5: printf("'%s'", city);  break;
			}
			printf("\n");
		}
		printf("    confirm ? (y/n) : ");
		userConfirm = getchar();
		
		if (userConfirm == 'y'){
			// updating user attributes
			FILE *attributeFile = fopen(fileName,"w");
			fprintf(attributeFile, "%c\n%d\n%s\n%s", gender, age, occupation, city);
			fclose(attributeFile);

			break;
		}
	} fflush(stdin);
}





void showAttributes(US3R user){
	sprintf(currentInterface, "showAttributes");

	char gender;
	int age;
	char occupation[20];
	char city[20];
	
	char fileName[50];
	sprintf(fileName, "%s/%s/%s", "../systemFiles/Users", user.UUId, "attributes.txt");
	FILE *attributeFile = fopen(fileName,"r");
	fscanf(attributeFile, "%c\n%d\n%s\n%s", &gender, &age, &occupation, &city);
	fclose(attributeFile);
	
	system("cls");
	
	char *Text[] = { "",
	"    Manager_                                   ",
	"    +---------------------------------------+  ",
	"    | User Id     : ",
	"    | Username    : ",
	"    | role        : ",
	"    | status      : ",
	"    +---------------------------------------+  ",
	"    | gender      : ",
	"    | age         : ",
	"    | occupation  : ",
	"    | city        : ",
	"    +---------------------------------------+  ", ""};

	int i;
	for(i=0; i<14; i++){
		printf("%s", Text[i]);
		switch (i){
			case  3: printf("'%s'", user.UUId);    	break;
			case  4: printf("'%s'", user.name);    	break;
			case  5: printf("'%s'", user.role);    	break;
			case  6: printf("'%d'", user.status);  	break;
			case  8: printf("'%c'", gender);  		break;
			case  9: printf("'%d'", age);  			break;
			case 10: printf("'%s'", occupation);  	break;
		    case 11: printf("'%s'", city);  		break;
		    
			default : break;
		}
		printf("\n");
	}
}





void startGuide(){
	sprintf(currentInterface, "startGuide");
	char *Text[] = {
		"",
		"PROJECT   : PEOPLE YOU MAY KNOW (pymk)",
		"OBJECTIVE : SOCIAL NETWORK FRIEND SUGGESTION",
		"-----------------------------------------------------------------------------------------------------------",
		"",
		"-----------------------------------------------------------------------------------------------------------",
		"Welcome to pymk ver 1.0",
		"",
		"It is program designed to simulate the core functionality of a social networking platform.",
		"It uses graph data structures and algorithms to identify and recommend potential new connections to users.",
		"",
		"Available commands",
		"",
		"  >>> help",
		"  >>> feed",
		"  >>> post",
		"  >>> network",
		"  >>> network suggest",
		"  >>> network connect",
		"  >>> network message",
		"  >>> account",
		"  >>> account delete",
		"  >>> logout",
		"  >>> quit",
		"-----------------------------------------------------------------------------------------------------------"
	};

	int i;
	system("cls");
	for(i=0; i<25; i++){ 
		printf("  %s \n", Text[i]); 
	}
}





int invokeCommand(US3R *user, char tokens[][10], int nt){
	sprintf(currentInterface, "invokeCommand");
	if (nt == 0){ return 0; }

	//int i;
	//for (i=0; i<nt; i++){ printf("... %s \n", tokens[i]); }

	int isInvalid = 0;
	switch(tokens[0][0]){

		case 'h':
			if (strcmp(tokens[0], "help")==0){ pymkShell.startGuide(); }
			else{ isInvalid = 1; }
			break;

		case 'a':
			if (strcmp(tokens[0], "account")==0){
				if (nt==1){ pymkShell.showAttributes(*user); }
				else { isInvalid = 1; }
			}
			else{ isInvalid = 1; }
			break;
			
		case 'l':
			if (strcmp(tokens[0], "logout")==0){
				if (nt==1){ 
					*user = pymkShell.LoginUI(); 
					if (user->status == -1 ){ isInvalid = -1; }
					else{ pymkShell.startGuide(); }
				}
				else { isInvalid = 1; }
			}
			else{ isInvalid = 1; }
			break;
		
		case 'n':
			if (strcmp(tokens[0], "network")==0){ 
				if (nt==1){ pymkShell.showFriends(*user); }
				else if (nt==2){
					if (strcmp(tokens[1], "connect")==0){ pymkShell.request(*user); }
					else if (strcmp(tokens[1], "suggest")==0){ pymkShell.RecommendFriend(*user); }
					else { isInvalid = 1; }
				}
				else { isInvalid = 1; }
			}
			else{ isInvalid = 1; }
			break;
			
		case 'q':
			if (strcmp(tokens[0], "quit")==0){
				if (nt==1){ isInvalid = -1; }
				else { isInvalid = 1; }
			}
			else { isInvalid = 1; }
			break;

		default:
			isInvalid = 1;
			break;
	}

	return isInvalid;
}





int request(US3R user){
	sprintf(currentInterface, "sendRequest");
	US3R unknown;

	system("cls");
	printf("\n");
	printf("$ request \n");
	printf("$ Username : ");	fgets(unknown.name, sizeof(unknown.name), stdin);	fflush(stdin);
	printf("$ User Id  : ");	fgets(unknown.UUId, sizeof(unknown.UUId), stdin);	fflush(stdin);
	printf("\n");

	sprintf(unknown.role, "none");
	unknown.status = -1;


	char status[80];
	char message[80];
	bool failed = false;

	if (pymkCore.userExist(unknown.UUId)){
		if (pymkCore.verifyuser(unknown)){
			unknown.status = 1;
			if (!pymkCore.isFriends(user, unknown)){
				pymkCore.makeFriends(user, unknown);
				sprintf(status,  "%s%s%s", TextEffects.color.Green, "request sent", TextEffects.Reset);
				sprintf(message, "%s%s%s", TextEffects.color.Green, "request is accepted (default)", TextEffects.Reset);
			} else{
				sprintf(status,  "%s%s%s", TextEffects.color.Yellow, "request withdraw", TextEffects.Reset);
				sprintf(message, "%s%s%s", TextEffects.color.Yellow, "already friend", TextEffects.Reset);
			}
		}else{ failed = true; }
	}else{ failed = true; }

	if (failed){
		sprintf(status,  "%s%s%s", TextEffects.color.Red, "User Not Found", TextEffects.Reset);
		sprintf(message, "%s%s%s", TextEffects.color.Red, "verify information and try again", TextEffects.Reset);
	}


	char *Text[] = { "",
		"+----------------------------------------------------------------------------+",
		"|  friend request status                                                     ¦",
		"+----------------------------------------------------------------------------+",
		"|  Search Criteria                                                           |",
		"|  º User Id    :",
		"|  º Username   :",
		"+----------------------------------------------------------------------------+",
		"|  Result                                                                    |",
		"|  º Status     :",
		"|  º Message    :",
		"+----------------------------------------------------------------------------+", ""
	} ;

	unknown.name[strlen(unknown.name) -1] = '\0';
	unknown.UUId[strlen(unknown.UUId) -1] = '\0';
	
	int i;
	system("cls");
	for (i=0; i<13; i++){
		printf("%s", Text[i]);
		switch (i){
			case 5 : printf(" %s%s%s", TextEffects.color.Yellow, unknown.UUId, TextEffects.Reset); break;
			case 6 : printf(" %s%s%s", TextEffects.color.Yellow, unknown.name, TextEffects.Reset); break;
			case 9 : printf(" %s", status);		break;
			case 10: printf(" %s", message);	break;
			default: break;
		}
		printf("\n");
	}

	return 0;
}





void showFriends(US3R user){
	
	char UserDir[25] = "../systemFiles/Users";
	char userFriends[40];
	sprintf(userFriends, "%s/%s/%s.txt", UserDir, user.UUId, "friends");
	FILE *friendList = fopen(userFriends, "r");

	char *Text[] = {"",
	"+----------------------------------------------------------------------------+",
	"|  friend network                                                            ¦",
	"+----------------------------------------------------------------------------+",
	"" };

	int i;
	system("cls");
	US3R dummy;
	for(i=0; i<4; i++){ printf("%s \n", Text[i]); } 
	while(fscanf(friendList, "%s\t%s", dummy.UUId, dummy.name)==2){
		printf("|  º %s    :    %s \n", dummy.UUId, dummy.name);
	}	printf("%s \n\n", Text[3]);

	fclose(friendList);
}





void RecommendFriend(US3R user){

	int rLimit = 20;
	US3R *Recommended = RecommendList(user, &rLimit);
	
	char gender;
	int  age;
	char occupation[20];
	char city[20];
	char fileName[50];

	char *Text[] = { "",
		"+----------------------------------------------------------------------------+",
		"|  friend suggested ",
		"+----------------------------------------------------------------------------+",
		"|  º ______id  º  __USERNAME  º  G  º  AGE  º  __________  º  ______CITY",
		"+----------------------------------------------------------------------------+",
	};

	int i;
	system("cls");
	for (i=0; i<6; i++){
		printf("%s", Text[i]);
		if (i==2){ printf("(%d)", rLimit); }
		printf("\n");
	}

	for (i=0; i<rLimit; i++){

		sprintf(fileName, "%s/%s/%s", "../systemFiles/Users", Recommended[i].UUId, "attributes.txt");
		FILE *attributeFile = fopen(fileName,"r");
		fscanf(attributeFile, "%c\n%d\n%s\n%s", &gender, &age, &occupation, &city);
		fclose(attributeFile);

		printf("|  º %8s  º  %10s  º  %c  º  %3d  º  %10s  º  %10s \n", Recommended[i].UUId, Recommended[i].name, gender, age, occupation, city);
	}	printf("%s \n\n", Text[1]);

	free(Recommended);
}





