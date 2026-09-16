/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <アヤマリバンゴウ.h>
#include <タイケイ/タイケイヨビダシ.h>

int アヤマリバンゴウ;
char **カンキョウヘンスウイチラン;

long __syscall_result(long ケッカ)
{
    if ((unsigned long)ケッカ >= (unsigned long)-4095) {
        アヤマリバンゴウ = (int)-ケッカ;
        return -1;
    }
    return ケッカ;
}
