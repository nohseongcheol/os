#include <unistd.h>

int main(int argc, char **bağımsız_değişkenler_2)
{
    const char expected[] = "argument with spaces";
    unsigned int konum = 0;
    int passed = argc == 2 && bağımsız_değişkenler_2 != (char **)0 && bağımsız_değişkenler_2[1] != (char *)0;
    if (passed) {
        while (expected[konum] != 0 && bağımsız_değişkenler_2[1][konum] == expected[konum])
            konum++;
        passed = expected[konum] == 0 && bağımsız_değişkenler_2[1][konum] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)Yazma(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)Yazma(1, result, sizeof(result) - 1U);
    }
    return 9;
}
