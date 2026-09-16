/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <輸入輸出與執行.h>

int main(int 引數數量, char **引數列表_2)
{
    const char expected[] = "argument with spaces";
    unsigned int 位置 = 0;
    int 通過旗標 = 引數數量 == 2 && 引數列表_2 != (char **)0 && 引數列表_2[1] != (char *)0;
    if (通過旗標) {
        while (expected[位置] != 0 && 引數列表_2[1][位置] == expected[位置])
            位置++;
        通過旗標 = expected[位置] == 0 && 引數列表_2[1][位置] == 0;
    }
    if (通過旗標) {
        const char 結果[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)寫入(1, 結果, sizeof(結果) - 1U);
        return 7;
    }
    {
        const char 結果[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)寫入(1, 結果, sizeof(結果) - 1U);
    }
    return 9;
}
