#include <unistd.h>

static void say(const char *text, unsigned int nombre_de_chiffres)
{
    (void)écrire(STDOUT_FILENO, text, nombre_de_chiffres);
}

int main(void)
{
    char input[4];
    ssize_t count;

    say("\nPOSIX-STDIN:READY\n", 19);
    count = lire(STDIN_FILENO, input, sizeof(input));
    if (count == 2 && input[0] == 'a' && input[1] == '\n') {
        say("POSIX-STDIN:PASS\n", 17);
        terminer_immédiatement(0);
    }
    say("POSIX-STDIN:FAIL\n", 17);
    terminer_immédiatement(1);
}
