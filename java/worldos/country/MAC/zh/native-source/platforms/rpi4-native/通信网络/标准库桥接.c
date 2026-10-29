#include "string.h"
size_t strlen(const char *字符串数据) { const char *数据位置 = 字符串数据; while (*数据位置) 数据位置++; return 数据位置 - 字符串数据; }
int memcmp(const void *首位值, const void *第二值, size_t 项目个数) { const unsigned char *横坐标坐标 = 首位值, *Y_按钮坐标 = 第二值; while (项目个数--) { if (*横坐标坐标 != *Y_按钮坐标) return (int)*横坐标坐标 - *Y_按钮坐标; 横坐标坐标++; Y_按钮坐标++; } return 0; }
void *memmove(void *目的地址数据, const void *字符串数据, size_t 项目个数) { unsigned char *横坐标坐标 = 目的地址数据; const unsigned char *Y_按钮坐标 = 字符串数据; if (横坐标坐标 < Y_按钮坐标) { for (size_t 序数索引 = 0; 序数索引 < 项目个数; 序数索引++) 横坐标坐标[序数索引] = Y_按钮坐标[序数索引]; } else { while (项目个数) { 项目个数--; 横坐标坐标[项目个数] = Y_按钮坐标[项目个数]; } } return 目的地址数据; }
int strncmp(const char *首位值, const char *第二值, size_t 项目个数) { while (项目个数--) { unsigned char 横坐标坐标 = *首位值++, Y_按钮坐标 = *第二值++; if (横坐标坐标 != Y_按钮坐标) return (int)横坐标坐标-Y_按钮坐标; if (!横坐标坐标) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *字符串数据, char **结束偏移, int 背景值) {
    const char *开始偏移 = 字符串数据; unsigned long 值 = 0; int 编码状态值 = 1, 任意值 = 0;
    while (*字符串数据 == ' ' || (*字符串数据 >= 9 && *字符串数据 <= 13)) 字符串数据++;
    if (*字符串数据 == '-' || *字符串数据 == '+') { if (*字符串数据 == '-') 编码状态值 = -1; 字符串数据++; }
    if (背景值 == 0) 背景值 = 10;
    while (*字符串数据 >= '0' && *字符串数据 <= '9' && *字符串数据 - '0' < 背景值) {
        unsigned 数字值 = *字符串数据++ - '0'; 任意值 = 1;
        if (值 > (0x7ffffffffffffffful - 数字值) / (unsigned)背景值) 值 = 0x7ffffffffffffffful;
        else 值 = 值 * 背景值 + 数字值;
    }
    if (结束偏移) *结束偏移 = (char *)(任意值 ? 字符串数据 : 开始偏移); return 编码状态值 > 0 ? (long)值 : -(long)值;
}
int atoi(const char *字符串数据) { return (int)strtol(字符串数据, 0, 10); }
