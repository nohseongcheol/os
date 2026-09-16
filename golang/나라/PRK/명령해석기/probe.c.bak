#include <입출력과실행.h>

int main(int 인수수, char **인수목록)
{
    const char expected[] = "argument with spaces";
    unsigned int 위치 = 0;
    int 통과여부 = 인수수 == 2 && 인수목록 != (char **)0 && 인수목록[1] != (char *)0;
    if (통과여부) {
        while (expected[위치] != 0 && 인수목록[1][위치] == expected[위치])
            위치++;
        통과여부 = expected[위치] == 0 && 인수목록[1][위치] == 0;
    }
    if (통과여부) {
        const char 결과[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)쓰기(1, 결과, sizeof(결과) - 1U);
        return 7;
    }
    {
        const char 결과[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)쓰기(1, 결과, sizeof(결과) - 1U);
    }
    return 9;
}
