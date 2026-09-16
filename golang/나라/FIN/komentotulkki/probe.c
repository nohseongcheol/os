/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **argumentit_2)
{
    const char expected[] = "argument with spaces";
    unsigned int paikka = 0;
    int passed = argc == 2 && argumentit_2 != (char **)0 && argumentit_2[1] != (char *)0;
    if (passed) {
        while (expected[paikka] != 0 && argumentit_2[1][paikka] == expected[paikka])
            paikka++;
        passed = expected[paikka] == 0 && argumentit_2[1][paikka] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)Kirjoitus(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)Kirjoitus(1, result, sizeof(result) - 1U);
    }
    return 9;
}
