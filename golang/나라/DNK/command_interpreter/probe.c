/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **argv)
{
    const char expected[] = "argument with spaces";
    unsigned int position = 0;
    int passed = argc == 2 && argv != (char **)0 && argv[1] != (char *)0;
    if (passed) {
        while (expected[position] != 0 && argv[1][position] == expected[position])
            position++;
        passed = expected[position] == 0 && argv[1][position] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)Skrive(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)Skrive(1, result, sizeof(result) - 1U);
    }
    return 9;
}
