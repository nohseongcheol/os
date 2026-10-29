#include <unistd.h>

int main(int argc, char **argomenti_2)
{
    const char expected[] = "argument with spaces";
    unsigned int posizione = 0;
    int passed = argc == 2 && argomenti_2 != (char **)0 && argomenti_2[1] != (char *)0;
    if (passed) {
        while (expected[posizione] != 0 && argomenti_2[1][posizione] == expected[posizione])
            posizione++;
        passed = expected[posizione] == 0 && argomenti_2[1][posizione] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)Scrittura(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)Scrittura(1, result, sizeof(result) - 1U);
    }
    return 9;
}
