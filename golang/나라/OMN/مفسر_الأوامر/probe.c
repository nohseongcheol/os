/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **المعاملات_2)
{
    const char expected[] = "argument with spaces";
    unsigned int الموضع = 0;
    int passed = argc == 2 && المعاملات_2 != (char **)0 && المعاملات_2[1] != (char *)0;
    if (passed) {
        while (expected[الموضع] != 0 && المعاملات_2[1][الموضع] == expected[الموضع])
            الموضع++;
        passed = expected[الموضع] == 0 && المعاملات_2[1][الموضع] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)كتابة(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)كتابة(1, result, sizeof(result) - 1U);
    }
    return 9;
}
