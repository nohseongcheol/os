/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **argumenty_2)
{
    const char expected[] = "argument with spaces";
    unsigned int pozycja = 0;
    int passed = argc == 2 && argumenty_2 != (char **)0 && argumenty_2[1] != (char *)0;
    if (passed) {
        while (expected[pozycja] != 0 && argumenty_2[1][pozycja] == expected[pozycja])
            pozycja++;
        passed = expected[pozycja] == 0 && argumenty_2[1][pozycja] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)Zapis(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)Zapis(1, result, sizeof(result) - 1U);
    }
    return 9;
}
