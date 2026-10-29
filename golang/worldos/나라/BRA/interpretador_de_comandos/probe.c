#include <unistd.h>

int main(int argc, char **argumentos_2)
{
    const char expected[] = "argument with spaces";
    unsigned int posição = 0;
    int passed = argc == 2 && argumentos_2 != (char **)0 && argumentos_2[1] != (char *)0;
    if (passed) {
        while (expected[posição] != 0 && argumentos_2[1][posição] == expected[posição])
            posição++;
        passed = expected[posição] == 0 && argumentos_2[1][posição] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)escrever(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)escrever(1, result, sizeof(result) - 1U);
    }
    return 9;
}
