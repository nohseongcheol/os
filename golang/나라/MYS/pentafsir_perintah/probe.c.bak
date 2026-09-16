#include <unistd.h>

int main(int argc, char **argv)
{
    const char expected[] = "argument with spaces";
    unsigned int kedudukan = 0;
    int passed = argc == 2 && argv != (char **)0 && argv[1] != (char *)0;
    if (passed) {
        while (expected[kedudukan] != 0 && argv[1][kedudukan] == expected[kedudukan])
            kedudukan++;
        passed = expected[kedudukan] == 0 && argv[1][kedudukan] == 0;
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
