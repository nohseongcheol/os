/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **аргументи_2)
{
    const char expected[] = "argument with spaces";
    unsigned int позиція = 0;
    int passed = argc == 2 && аргументи_2 != (char **)0 && аргументи_2[1] != (char *)0;
    if (passed) {
        while (expected[позиція] != 0 && аргументи_2[1][позиція] == expected[позиція])
            позиція++;
        passed = expected[позиція] == 0 && аргументи_2[1][позиція] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)Запис(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)Запис(1, result, sizeof(result) - 1U);
    }
    return 9;
}
