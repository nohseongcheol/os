#include <unistd.h>

int main(int argc, char **Argumente_2)
{
    const char expected[] = "argument with spaces";
    unsigned int Position = 0;
    int passed = argc == 2 && Argumente_2 != (char **)0 && Argumente_2[1] != (char *)0;
    if (passed) {
        while (expected[Position] != 0 && Argumente_2[1][Position] == expected[Position])
            Position++;
        passed = expected[Position] == 0 && Argumente_2[1][Position] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)schreiben(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)schreiben(1, result, sizeof(result) - 1U);
    }
    return 9;
}
