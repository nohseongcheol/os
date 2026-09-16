/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

static void say(const char *text, unsigned int अंकों_की_संख्या)
{
    (void)लिखना(STDOUT_FILENO, text, अंकों_की_संख्या);
}

int main(void)
{
    char input[4];
    ssize_t count;

    say("\nPOSIX-STDIN:READY\n", 19);
    count = पढ़ना(STDIN_FILENO, input, sizeof(input));
    if (count == 2 && input[0] == 'a' && input[1] == '\n') {
        say("POSIX-STDIN:PASS\n", 17);
        तुरंत_समाप्त_करना(0);
    }
    say("POSIX-STDIN:FAIL\n", 17);
    तुरंत_समाप्त_करना(1);
}
