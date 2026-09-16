/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <unistd.h>

int main(int argc, char **तर्क_सूची_2)
{
    const char expected[] = "argument with spaces";
    unsigned int स्थान = 0;
    int passed = argc == 2 && तर्क_सूची_2 != (char **)0 && तर्क_सूची_2[1] != (char *)0;
    if (passed) {
        while (expected[स्थान] != 0 && तर्क_सूची_2[1][स्थान] == expected[स्थान])
            स्थान++;
        passed = expected[स्थान] == 0 && तर्क_सूची_2[1][स्थान] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)लिखना(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)लिखना(1, result, sizeof(result) - 1U);
    }
    return 9;
}
