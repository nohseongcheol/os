/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **đối_số_2)
{
    const char expected[] = "argument with spaces";
    unsigned int vị_trí = 0;
    int passed = argc == 2 && đối_số_2 != (char **)0 && đối_số_2[1] != (char *)0;
    if (passed) {
        while (expected[vị_trí] != 0 && đối_số_2[1][vị_trí] == expected[vị_trí])
            vị_trí++;
        passed = expected[vị_trí] == 0 && đối_số_2[1][vị_trí] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)Ghi(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)Ghi(1, result, sizeof(result) - 1U);
    }
    return 9;
}
