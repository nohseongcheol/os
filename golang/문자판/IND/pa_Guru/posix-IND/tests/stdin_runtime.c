#include <unistd.h>

static void say(const char *text, unsigned int ਆਕਾਰ)
{
    (void)ਲਿਖਣਾ(STDOUT_FILENO, text, ਆਕਾਰ);
}

int main(void)
{
    char input[4];
    ssize_t count;

    say("\nPOSIX-STDIN:READY\n", 19);
    count = ਪੜ੍ਹਨਾ(STDIN_FILENO, input, sizeof(input));
    if (count == 2 && input[0] == 'a' && input[1] == '\n') {
        say("POSIX-STDIN:PASS\n", 17);
        _exit(0);
    }
    say("POSIX-STDIN:FAIL\n", 17);
    _exit(1);
}
