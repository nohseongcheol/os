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
