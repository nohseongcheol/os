#include <unistd.h>

static void say(const char *text, unsigned int cantidad_de_dígitos)
{
    (void)escribir(STDOUT_FILENO, text, cantidad_de_dígitos);
}

int main(void)
{
    char input[4];
    ssize_t count;

    say("\nPOSIX-STDIN:READY\n", 19);
    count = leer(STDIN_FILENO, input, sizeof(input));
    if (count == 2 && input[0] == 'a' && input[1] == '\n') {
        say("POSIX-STDIN:PASS\n", 17);
        terminar_inmediatamente(0);
    }
    say("POSIX-STDIN:FAIL\n", 17);
    terminar_inmediatamente(1);
}
