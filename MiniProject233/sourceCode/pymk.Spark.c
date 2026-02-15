#include <stdio.h>
#include "pymk.Shell.c"

int main(){
	char isNewUser;
	US3R user;

	char command[50];
	char tokens[5][10];
	int nt;
	int wasInvalid = 0 , isInvalid = 0;

	pymkCore.sysWork();
	isNewUser = pymkShell.IntroductionUI();

     if (isNewUser=='y'){ user = pymkShell.SigninUI();  }
else if (isNewUser=='n'){ user = pymkShell.LoginUI(); 	}
else{ printf("Thank you..."); return 0; }
	 if (user.status == -1 ){ return 0; }

	pymkShell.startGuide();
	while (1){
		command[0] = '\0';

		if (!isInvalid) { wasInvalid = isInvalid; }
		else { wasInvalid += isInvalid;	}

		printf(">>> ");
		scanf("%[^\n]s", command);

		nt = pymkCore.Parser(command, tokens);
		isInvalid = pymkShell.invokeCommand(&user, tokens, nt);

		if (isInvalid == -1){ system("cls"); break; }
		if (isInvalid){
			if (wasInvalid){
				printf("%s%s", TextEffects.cursor.move.up, "\033[2K"); 
				printf("%s%s", TextEffects.cursor.move.up, "\033[2K"); 	
				printf("%s%s%s x%d %s",TextEffects.color.Red , "$$$ Invalid Command", TextEffects.Reset, wasInvalid+1, "\n");
			}else{
				printf("%s%s", TextEffects.cursor.move.up, "\033[2K"); 
				printf("%s%s%s",TextEffects.color.Red ,  "$$$ Invalid Command \n", TextEffects.Reset );
			}
		}
	}
	return 0;
}





