#include <unistd.h>

static void say(const char *text, unsigned int Ziffernanzahl)
{
    (void)schreiben(STDOUT_FILENO, text, Ziffernanzahl);
}

int main(void)
{
    char input[4];
    ssize_t count;

    say("\nPOSIX-STDIN:READY\n", 19);
    count = lesen(STDIN_FILENO, input, sizeof(input));
    if (count == 2 && input[0] == 'a' && input[1] == '\n') {
        say("POSIX-STDIN:PASS\n", 17);
        sofort_beenden(0);
    }
    say("POSIX-STDIN:FAIL\n", 17);
    sofort_beenden(1);
}
