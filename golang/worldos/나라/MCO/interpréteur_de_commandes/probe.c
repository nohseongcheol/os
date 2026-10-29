#include <unistd.h>

int main(int argc, char **arguments_2)
{
    const char expected[] = "argument with spaces";
    unsigned int position = 0;
    int passed = argc == 2 && arguments_2 != (char **)0 && arguments_2[1] != (char *)0;
    if (passed) {
        while (expected[position] != 0 && arguments_2[1][position] == expected[position])
            position++;
        passed = expected[position] == 0 && arguments_2[1][position] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)écrire(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)écrire(1, result, sizeof(result) - 1U);
    }
    return 9;
}
