/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

static void say(const char *text, unsigned int عدد_الخانات)
{
    (void)كتابة(STDOUT_FILENO, text, عدد_الخانات);
}

int main(void)
{
    char input[4];
    ssize_t count;

    say("\nPOSIX-STDIN:READY\n", 19);
    count = قراءة(STDIN_FILENO, input, sizeof(input));
    if (count == 2 && input[0] == 'a' && input[1] == '\n') {
        say("POSIX-STDIN:PASS\n", 17);
        إنهاء_فوري(0);
    }
    say("POSIX-STDIN:FAIL\n", 17);
    إنهاء_فوري(1);
}
