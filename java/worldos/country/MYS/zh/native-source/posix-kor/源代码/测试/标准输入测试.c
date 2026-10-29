#include <文件ABI.h>
#include <stdio.h>
#include <string.h>
int main(int 项目个数, char **条目列表) {
    (void)项目个数; (void)条目列表;
    char 数据[6]; int 长度 = 0;
    puts("POSIX INPUT READY");
    while (长度 < 6) {
        int 结果 = 读取文件数据(0, 数据 + 长度, 6 - 长度);
        if (结果 <= 0) return 1;
        长度 += 结果;
    }
    if (memcmp(数据, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
