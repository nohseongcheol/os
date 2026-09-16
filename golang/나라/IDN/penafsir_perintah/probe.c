/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **argumen_2)
{
    const char expected[] = "argument with spaces";
    unsigned int posisi = 0;
    int passed = argc == 2 && argumen_2 != (char **)0 && argumen_2[1] != (char *)0;
    if (passed) {
        while (expected[posisi] != 0 && argumen_2[1][posisi] == expected[posisi])
            posisi++;
        passed = expected[posisi] == 0 && argumen_2[1][posisi] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)Tulis(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)Tulis(1, result, sizeof(result) - 1U);
    }
    return 9;
}
