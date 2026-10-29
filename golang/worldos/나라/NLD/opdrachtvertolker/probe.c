#include <unistd.h>

int main(int argc, char **argumenten_2)
{
    const char expected[] = "argument with spaces";
    unsigned int positie = 0;
    int passed = argc == 2 && argumenten_2 != (char **)0 && argumenten_2[1] != (char *)0;
    if (passed) {
        while (expected[positie] != 0 && argumenten_2[1][positie] == expected[positie])
            positie++;
        passed = expected[positie] == 0 && argumenten_2[1][positie] == 0;
    }
    if (passed) {
        const char result[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)Schrijven(1, result, sizeof(result) - 1U);
        return 7;
    }
    {
        const char result[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)Schrijven(1, result, sizeof(result) - 1U);
    }
    return 9;
}
