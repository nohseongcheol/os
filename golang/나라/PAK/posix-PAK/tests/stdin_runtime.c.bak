#include <unistd.h>

static void say(const char *text, unsigned int ہندسوں_کی_تعداد)
{
    (void)لکھیں(STDOUT_FILENO, text, ہندسوں_کی_تعداد);
}

int main(void)
{
    char input[4];
    ssize_t count;

    say("\nPOSIX-STDIN:READY\n", 19);
    count = پڑھیں(STDIN_FILENO, input, sizeof(input));
    if (count == 2 && input[0] == 'a' && input[1] == '\n') {
        say("POSIX-STDIN:PASS\n", 17);
        _exit(0);
    }
    say("POSIX-STDIN:FAIL\n", 17);
    _exit(1);
}
