#include <unistd.h>

int main(int argc, char **دلائل_2)
{
    const char expected[] = "argument with spaces";
    unsigned int مقام = 0;
    int passed = argc == 2 && دلائل_2 != (char **)0 && دلائل_2[1] != (char *)0;
    if (passed) {
        while (expected[مقام] != 0 && دلائل_2[1][مقام] == expected[مقام])
            مقام++;
        passed = expected[مقام] == 0 && دلائل_2[1][مقام] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)لکھنا(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)لکھنا(1, result, sizeof(result) - 1U);
    }
    return 9;
}
