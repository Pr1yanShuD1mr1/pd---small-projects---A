#include <stdio.h>			// FILE 
#include <direct.h>			// _access : check whether a file/dir exists.
#include <io.h>				// __mkdir : make a empty directory.
#include <time.h>  			// time	   : if parameter is NULL, return second passed since epoch i.e. 1970. 
#include <string.h> 		// string related function
#include <ctype.h>			// character identificaation function
#include <stdbool.h>		// for true and false
#include <stdlib.h>			// for malloc

char currentInterface[20] = "void";
bool systemWork = false;

typedef struct US3R {
	char UUId[9];			// user-unique-Id
	char name[30];
	char role[6]; 			// admin, user, guest, none
	int status;			    // 0 for suspend, -1 for not initialized, 1 for active
} US3R;


void sysWork(void);
void genId(char *id);
void userInit(US3R user);
bool userExist(char id[]);
 int verifyuser(US3R user);
 int Parser(char *string, char stringArray[][10]);
void makeFriends(US3R user1, US3R user2);
bool isFriends(US3R user1, US3R user2);


struct {
	void (*sysWork)(void);
	void (*genId)(char *id);
	void (*userInit)(US3R user);	
	bool (*userExist)(char id[]);
	 int (*verifyuser)(US3R user);
	 int (*Parser)(char *string, char stringArray[][10]);
	void (*makeFriends)(US3R user1, US3R user2);
	bool (*isFriends)(US3R user1, US3R user2);
}

pymkCore = { 
	sysWork,
	genId,
	userInit,
	userExist,
	verifyuser,
	Parser,
	makeFriends,
	isFriends
};





void sysWork(void){
/*	It check whether pymk directory is present or not.
	if not it create a new directory. */
	
	bool MoreWork = false;
	
	// _access as function, return 0 if directory exist and !0 if doesnot.
	
	if (_access("../systemFiles", 0)){
		_mkdir("../systemFiles");
		MoreWork = true;
	}
	if (_access("../systemFiles/pymk", 0)){
		_mkdir("../systemFiles/pymk");
		fclose(fopen("../systemFiles/pymk/UUIDs.txt","w"));
	}	
	if (_access("../systemFiles/Users", 0)){
		_mkdir("../systemFiles/Users");
	}


	if (MoreWork){
		systemWork = true;
		// creating a { admin, guest } account.
		US3R admin = { "admin123", "admin123", "admin", 1 };
		US3R guest = { "guest123", "guest123", "guest", 1 };

		pymkCore.userInit(admin);
		pymkCore.userInit(guest);
		systemWork = false;
	}
}





void genId(char *id){
/*	Generate a unique 8 charecter Id. */

	unsigned char bytes[4];
	
	srand(time(NULL));			// Seed the random generator with current time. it may generate unique pattern.

	int i, I=0;
	while(I<100){ I++;
		for (i=0; i<4; i++) { bytes[i] = (unsigned char)(rand() % 256); }
		sprintf(id, "%02x%02x%02x%02x", bytes[0], bytes[1], bytes[2], bytes[3]);
		printf("- %s -\n", id);
		if (!pymkCore.userExist(id)){break;}	// if id exist , loop continue.
	}
}





bool userExist(char id[]){
/*	Check whether a user exist based on UUID.
	return - (int) {1,0} = {exist, does-not-exist} 
	where, 
		id is placeholder for input UUID. */

	FILE *idFile = fopen("../systemFiles/pymk/UUIDs.txt","r");

	int i;
	char UserInfo[40];
	while(fgets(UserInfo, 40, idFile)){
		int r=1;								// if after loop r is 1, it implies that id match
		for(i=0; i<8; i++){
			if (UserInfo[i] == id[i]){ r&=1;}
			else { r&=0; }
		}
		if(r){ 
			fclose(idFile); 
			return true;
		}
	} 
	fclose(idFile);
	return false;
}





void userInit(US3R user){ 
/*  for a user,
	it may not store user data in database.
	but 
		it leaves a footprint for it existences. */

	// uploading user existance
	FILE *idFile = fopen("../systemFiles/pymk/UUIDs.txt","a");
	fprintf(idFile, "%s\t%d\t%s \n", user.UUId, user.status, user.name);
	fclose(idFile);	

	// Making User Dir
	char UserDir[40] = "../systemFiles/Users/";
	strcat(UserDir, user.UUId);
	_mkdir(UserDir);
	
	char file[50];

	sprintf(file, "%s/%s.txt", UserDir, "attributes");		// for - gender, age, occupation, city
	fclose(fopen(file,"w"));

	sprintf(file, "%s/%s.txt", UserDir, "friends");
	fclose(fopen(file,"w"));

	sprintf(file, "%s/%s.txt", UserDir, "requests");
	fclose(fopen(file,"w"));
	
	if (!systemWork){
		//default freinds
		US3R admin = { "admin123", "admin123", "admin", 1 };
		US3R guest = { "guest123", "guest123", "guest", 1 };
	
		pymkCore.makeFriends(user, admin);
		pymkCore.makeFriends(user, guest);	
	}
}





int verifyuser(US3R user){
/*  Verify whether a user exist or not.
	return - (int) verification Status as {-1, 0, 1} = { doesnot-exist, suspended, active }
	where
		user is a placeholder, carrying input value to be compared.  */

	US3R dummy;
	FILE *idFile = fopen("../systemFiles/pymk/UUIDs.txt","r");
	
	int vs = -1;       // verification Status - {-1, 0, 1} = { doesnot-exist, suspended, active }
	int v1=0, v2=0;    // verification condition {1,2} for userId, userName
	while(fscanf(idFile, "%s\t%d\t%s", dummy.UUId, &dummy.status, dummy.name)==3){
		
		//printf(" %2d - '%s' \n", strlen(dummy.UUId), dummy.UUId);
		//printf(" %2d - '%s' \n", strlen(user.UUId), user.UUId);
		//printf(" %2d - '%s' \n", strlen(dummy.name), dummy.name);
		//printf(" %2d - '%s' \n", strlen(user.name), user.name);

		if (strcmp(dummy.UUId, user.UUId)==0){ v1=1; }
		if (strcmp(dummy.name, user.name)==0){ v2=1; }	

		if (v1&&v2){
			if (dummy.status){
				vs = 1; 
				break; 
			}else{
				vs = 0; 
				break; 
			}
		}else{ v1 = v2 = 0; }
	}

	fclose(idFile);
	return vs;
}





int Parser(char *string, char stringArray[][10]){
/*	split string , with space as delimitor,
	store substring in stringArray, 
	return no of substring				*/
	
	fflush(stdin);			// needed 
	fflush(stdout);			// needed 
	
	int i, j, k;
	int n = strlen(string);
	char character;
	
	int charAppeared = 0;
	
	for (i=0, j=0, k=0; i<n; i++){
		character = string[i];
		//printf(" '%c' ", character);

		if (isprint(character)){
			//printf(" printable ");
			if (isalnum(character)){
				//printf(" alphaNumeric ");
				if (!charAppeared) { charAppeared = 1; }
				stringArray[j][k++] = character;

			}else if (isspace(character)){
				//printf(" space ");
				if (charAppeared){
					stringArray[j][k] = '\0';
					//printf(" '%s' ", stringArray[j]);
					j++;
					k=0;
				}else{ continue; }				
			}

			if (i== (n-1)){
				stringArray[j][k] = '\0';
				//printf(" '%s' ", stringArray[j]);
				j++;
			} 
			//printf("\n");	
		}
	}
	return j;	
}





void makeFriends(US3R user1, US3R user2){
/*	write name of {user1, user2} in friends.txt file of {user2, user1}  */

	char UserDir[25] = "../systemFiles/Users";
	char user1Friends[40], 
		 user2Friends[40];

	sprintf(user1Friends, "%s/%s/%s.txt", UserDir, user1.UUId, "friends");
	sprintf(user2Friends, "%s/%s/%s.txt", UserDir, user2.UUId, "friends");

	FILE *friendList1 = fopen(user1Friends, "a");
	FILE *friendList2 = fopen(user2Friends, "a");

	fprintf(friendList1, "%s\t%s\n", user2.UUId, user2.name);
	fprintf(friendList2, "%s\t%s\n", user1.UUId, user1.name);

	fclose(friendList1);
	fclose(friendList2);
}




bool isFriends(US3R user1, US3R user2){
/*	return true if user1 and user2 are friends, else false.
	check if userid and unsname of one user is in another user friends.txt file.  */

	char UserDir[25] = "../systemFiles/Users";
	char user1Friends[40];
	sprintf(user1Friends, "%s/%s/%s.txt", UserDir, user1.UUId, "friends");
	FILE *friendList1 = fopen(user1Friends, "r");
	US3R dummy;

	bool condition1, condition2, result;
	while(fscanf(friendList1, "%s\t%s", dummy.UUId, dummy.name)==2){
		condition1 = false;
		condition2 = false;

		//printf(" %d:%s ; %d:%s  ==  %d:%s ; %d:%s \n", 
		//	strlen(user2.UUId), user2.UUId,
		//	strlen(user2.name), user2.name,
		//	strlen(dummy.UUId), dummy.UUId,
		//	strlen(dummy.name), dummy.name
		//);

		if (strcmp(dummy.UUId, user2.UUId)==0){ condition1 = true; }
		if (strcmp(dummy.name, user2.name)==0){ condition2 = true; }

		if (condition1 && condition1){
			result = true;
			break;
		}else{ result = false; }
	}

	fclose(friendList1);
	return result;
}





US3R *RecommendList(US3R target, int *rLimit){
	int tLimit = 50;
	
	// using Depth First Search (DFS)
	// starts at a source vertex and explores as far as possible along each branch before backtracking.
	// uses a stack to remember to get the next vertex to start a search, when a dead end occurs in any iteration. 
	
	typedef struct uuid { char UUId[9]; } uuid;

	uuid *stack      = (uuid*)malloc(tLimit*sizeof(uuid));
	uuid *visited    = (uuid*)malloc(tLimit*sizeof(uuid));
	US3R *recommend  = (US3R*)malloc((*rLimit)*sizeof(US3R));

	int sI = 0, vI = 0, rI = 0;
	bool isVisted, inStack, isRecommended;
	char selected[9];
	int i;

	strcpy(stack[sI++].UUId, target.UUId);

	char UserDir[25] = "../systemFiles/Users";
	char selectedFriends[40];
	US3R dummy;

	while (sI != 0){
		if (rI == *rLimit ){ break; }

		//printf("visited   :"); for (i=0; i<vI; i++){ printf(": %s ", visited[i].UUId); } printf("; \n");
		//printf("stack     :"); for (i=0; i<sI; i++){ printf(": %s ", stack[i].UUId); } printf("; \n");
		strcpy(selected, stack[--sI].UUId);
		//printf(" select    : %s \n", selected);

		isVisted = false;
		// checking if seleceted user is visted or not... if yes , skip ... else , add it to visited list
		for (i=0; i<vI; i++){
			if (strcmp(selected, visited[i].UUId) == 0){
				isVisted = true; 
				break;
			}
		}
		if (!isVisted){ strcpy(visited[vI++].UUId, selected); }

		sprintf(selectedFriends, "%s/%s/%s.txt", UserDir, selected, "friends");
		FILE *friendList = fopen(selectedFriends, "r");

		while(fscanf(friendList, "%s\t%s", dummy.UUId, dummy.name)==2){
			//printf(" scanned   : %s ", dummy.UUId);

			if (rI == *rLimit ){ break; }

			// checking if scanned user is in recommendList
			isRecommended = false;
			for (i=0; i<rI; i++){ 
				if (strcmp(dummy.UUId, recommend[i].UUId) == 0){ 
					//printf("was recommended");
					isRecommended = true;
					break;
				}
			}
			// if not , checking is it is user or it friend ... else recommeding it
			if (!isRecommended){
				if (strcmp(target.UUId, dummy.UUId) != 0){ 
					if (!pymkCore.isFriends(target, dummy)){
						//printf(": is recommended");
						strcpy(recommend[rI].UUId, dummy.UUId);
						strcpy(recommend[rI].name, dummy.name);
						rI++;
					}
				}
			}

			// checking if scanned user is visited previously
			isVisted = false;
			for (i=0; i<vI; i++){ 
				if (strcmp(dummy.UUId, visited[i].UUId) == 0){ 
					isVisted = true; 
					break;
				}
			}
			// if not, checking if it is in stack
			if (!isVisted){
				//printf(": not visited");
				inStack = false;
				for (i=0; i<sI; i++){ 
					if (strcmp(dummy.UUId, stack[i].UUId) == 0){ 
						inStack = true; 
						break;
					}
				}
				// else, adding it in stack for visiting
				if (!inStack){
					//printf(": add to stack"); 
					strcpy(stack[sI++].UUId, dummy.UUId); 
				}
			}
			//printf("\n");
		}
		fclose(friendList);
		//printf("recommend :"); for (i=0; i<rI; i++){ printf(": %s ", recommend[i].UUId); } printf("; \n\n");
	}

	free(stack);
	free(visited);

	*rLimit = rI;
	return recommend;
}





