/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <ニュウシュツリョクトジッコウ.h>

int main(int ヒキスウノカズ, char **ヒキスウイチラン)
{
    const char expected[] = "argument with spaces";
    unsigned int イチ = 0;
    int ゴウカクハンテイ = ヒキスウノカズ == 2 && ヒキスウイチラン != (char **)0 && ヒキスウイチラン[1] != (char *)0;
    if (ゴウカクハンテイ) {
        while (expected[イチ] != 0 && ヒキスウイチラン[1][イチ] == expected[イチ])
            イチ++;
        ゴウカクハンテイ = expected[イチ] == 0 && ヒキスウイチラン[1][イチ] == 0;
    }
    if (ゴウカクハンテイ) {
        const char ケッカ[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)カク(1, ケッカ, sizeof(ケッカ) - 1U);
        return 7;
    }
    {
        const char ケッカ[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)カク(1, ケッカ, sizeof(ケッカ) - 1U);
    }
    return 9;
}
