/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **செயலுருபுகள்_2)
{
    const char expected[] = "argument with spaces";
    unsigned int இடம் = 0;
    int passed = argc == 2 && செயலுருபுகள்_2 != (char **)0 && செயலுருபுகள்_2[1] != (char *)0;
    if (passed) {
        while (expected[இடம்] != 0 && செயலுருபுகள்_2[1][இடம்] == expected[இடம்])
            இடம்++;
        passed = expected[இடம்] == 0 && செயலுருபுகள்_2[1][இடம்] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)எழுது(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)எழுது(1, result, sizeof(result) - 1U);
    }
    return 9;
}
