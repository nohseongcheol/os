#include <unistd.h>

int main(int argc, char **аргументы_2)
{
    const char expected[] = "argument with spaces";
    unsigned int позиция = 0;
    int passed = argc == 2 && аргументы_2 != (char **)0 && аргументы_2[1] != (char *)0;
    if (passed) {
        while (expected[позиция] != 0 && аргументы_2[1][позиция] == expected[позиция])
            позиция++;
        passed = expected[позиция] == 0 && аргументы_2[1][позиция] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)писать(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)писать(1, result, sizeof(result) - 1U);
    }
    return 9;
}
