/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <输入输出与执行.h>

int main(int 参数数量, char **参数列表_2)
{
    const char expected[] = "argument with spaces";
    unsigned int 位置 = 0;
    int 通过标志 = 参数数量 == 2 && 参数列表_2 != (char **)0 && 参数列表_2[1] != (char *)0;
    if (通过标志) {
        while (expected[位置] != 0 && 参数列表_2[1][位置] == expected[位置])
            位置++;
        通过标志 = expected[位置] == 0 && 参数列表_2[1][位置] == 0;
    }
    if (通过标志) {
        const char 结果[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)写入(1, 结果, sizeof(结果) - 1U);
        return 7;
    }
    {
        const char 结果[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)写入(1, 结果, sizeof(结果) - 1U);
    }
    return 9;
}
