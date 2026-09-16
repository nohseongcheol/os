/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <入出力と実行.h>

int main(int 引数の数, char **引数一覧)
{
    const char expected[] = "argument with spaces";
    unsigned int 位置 = 0;
    int 合格判定 = 引数の数 == 2 && 引数一覧 != (char **)0 && 引数一覧[1] != (char *)0;
    if (合格判定) {
        while (expected[位置] != 0 && 引数一覧[1][位置] == expected[位置])
            位置++;
        合格判定 = expected[位置] == 0 && 引数一覧[1][位置] == 0;
    }
    if (合格判定) {
        const char 結果[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)書く(1, 結果, sizeof(結果) - 1U);
        return 7;
    }
    {
        const char 結果[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)書く(1, 結果, sizeof(結果) - 1U);
    }
    return 9;
}
