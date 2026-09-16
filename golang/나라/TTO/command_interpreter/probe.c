/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argument_count_2, char **arguments_2)
{
    const char expected[] = "argument with spaces";
    unsigned int position = 0;
    int passed_test = argument_count_2 == 2 && arguments_2 != (char **)0 && arguments_2[1] != (char *)0;
    if (passed_test) {
        while (expected[position] != 0 && arguments_2[1][position] == expected[position])
            position++;
        passed_test = expected[position] == 0 && arguments_2[1][position] == 0;
    }
    if (passed_test) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)write(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)write(1, result, sizeof(result) - 1U);
    }
    return 9;
}
