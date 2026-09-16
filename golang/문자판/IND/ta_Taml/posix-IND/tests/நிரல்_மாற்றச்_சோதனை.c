/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <அமைப்பு/சேய்_காத்திருப்பு.h>
#include <unistd.h>

static void say(const char *text, unsigned int இலக்கங்களின்_எண்ணிக்கை)
{
    (void)எழுது(STDOUT_FILENO, text, இலக்கங்களின்_எண்ணிக்கை);
}

int main(void)
{
    int நிலை;
    int கோப்பு_விவரிப்பி;
    char *செயலுருபுகள்_2[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *envp[] = {(char *)"POSIX_TEST=1", (char *)0};

    say("\nPOSIX-EXEC:START\n", 18);
    errno = 0;
    if (குறித்த_சேய்க்குக்_காத்திரு(-1, &நிலை, WNOHANG) == -1 && errno == ECHILD)
        say("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        say("PTEST:FAIL:waitpid-echild-empty\n", 32);
    errno = 0;
    if (சேய்க்குக்_காத்திரு(&நிலை) == -1 && errno == ECHILD)
        say("PTEST:PASS:wait-echild-empty\n", 29);
    else
        say("PTEST:FAIL:wait-echild-empty\n", 29);

    கோப்பு_விவரிப்பி = திற("/USER2", O_RDONLY);
    if (கோப்பு_விவரிப்பி < 0 || குறித்த_எண்ணுக்கு_கோப்புக்_குறிப்பை_நகலெடு(கோப்பு_விவரிப்பி, 10) != 10 || கோப்பைக்_கட்டுப்படுத்து(10, F_SETFD, FD_CLOEXEC) != 0) {
        say("PTEST:FAIL:cloexec-setup\n", 25);
        உடனே_முடி(98);
    }
    if (கோப்பு_விவரிப்பி != 10)
        (void)மூடு(கோப்பு_விவரிப்பி);

    (void)இயங்கும்_நிரலை_மாற்று("/PXEXEC", செயலுருபுகள்_2, envp);
    say("PTEST:FAIL:exec-image\n", 22);
    உடனே_முடி(99);
}
