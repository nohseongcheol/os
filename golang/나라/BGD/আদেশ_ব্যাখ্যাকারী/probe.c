/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **আর্গুমেন্ট_তালিকা_2)
{
    const char expected[] = "argument with spaces";
    unsigned int অবস্থান = 0;
    int passed = argc == 2 && আর্গুমেন্ট_তালিকা_2 != (char **)0 && আর্গুমেন্ট_তালিকা_2[1] != (char *)0;
    if (passed) {
        while (expected[অবস্থান] != 0 && আর্গুমেন্ট_তালিকা_2[1][অবস্থান] == expected[অবস্থান])
            অবস্থান++;
        passed = expected[অবস্থান] == 0 && আর্গুমেন্ট_তালিকা_2[1][অবস্থান] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)lekha(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)lekha(1, result, sizeof(result) - 1U);
    }
    return 9;
}
