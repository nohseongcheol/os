/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <にゅうしゅつりょくとじっこう.h>

int main(int ひきすうのかず, char **ひきすういちらん)
{
    const char expected[] = "argument with spaces";
    unsigned int いち = 0;
    int ごうかくはんてい = ひきすうのかず == 2 && ひきすういちらん != (char **)0 && ひきすういちらん[1] != (char *)0;
    if (ごうかくはんてい) {
        while (expected[いち] != 0 && ひきすういちらん[1][いち] == expected[いち])
            いち++;
        ごうかくはんてい = expected[いち] == 0 && ひきすういちらん[1][いち] == 0;
    }
    if (ごうかくはんてい) {
        const char けっか[] = "WORLDOS-SHELL-PROBE:PASS\n";
        (void)かく(1, けっか, sizeof(けっか) - 1U);
        return 7;
    }
    {
        const char けっか[] = "WORLDOS-SHELL-PROBE:FAIL\n";
        (void)かく(1, けっか, sizeof(けっか) - 1U);
    }
    return 9;
}
