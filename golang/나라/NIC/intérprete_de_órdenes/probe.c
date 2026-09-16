/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **argumentos_2)
{
    const char expected[] = "argument with spaces";
    unsigned int posición = 0;
    int passed = argc == 2 && argumentos_2 != (char **)0 && argumentos_2[1] != (char *)0;
    if (passed) {
        while (expected[posición] != 0 && argumentos_2[1][posición] == expected[posición])
            posición++;
        passed = expected[posición] == 0 && argumentos_2[1][posición] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)escribir(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)escribir(1, result, sizeof(result) - 1U);
    }
    return 9;
}
