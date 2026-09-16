/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <प्रणाली/संतान_प्रतीक्षा.h>
#include <unistd.h>

static void say(const char *text, unsigned int अंकों_की_संख्या)
{
    (void)लिखना(STDOUT_FILENO, text, अंकों_की_संख्या);
}

int main(void)
{
    int स्थिति;
    int संचिका_विवरणक;
    char *तर्क_सूची_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (नियत_संतान_की_प्रतीक्षा_करना(-1, &स्थिति, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (संतान_की_प्रतीक्षा_करना(&स्थिति) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    संचिका_विवरणक = खोलना("/USER2", O_RDONLY);
    if (संचिका_विवरणक < 0 || नियत_क्रमांक_पर_संचिका_संदर्भ_प्रतिलिपि_बनाना(संचिका_विवरणक, 10) != 10 || संचिका_नियंत्रित_करना(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        तुरंत_समाप्त_करना(98);
    }
    if (संचिका_विवरणक != 10)
        (void)बंद_करना(संचिका_विवरणक);

    (void)निष्पादन_सामग्री_बदलना("/PXEXEC", तर्क_सूची_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    तुरंत_समाप्त_करना(99);
}
