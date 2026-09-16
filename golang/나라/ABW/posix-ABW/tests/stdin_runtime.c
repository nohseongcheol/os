/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

static void say(const char *text, unsigned int aantal_cijfers)
{
    (void)Schrijven(STDOUT_FILENO, text, aantal_cijfers);
}

int main(void)
{
    char input[4];
    ssize_t count;

    say("\nPOSIX-STDIN:READY\n", 19);
    count = Lezen(STDIN_FILENO, input, sizeof(input));
    if (count == 2 && input[0] == 'a' && input[1] == '\n') {
        say("POSIX-STDIN:PASS\n", 17);
        _exit(0);
    }
    say("POSIX-STDIN:FAIL\n", 17);
    _exit(1);
}
