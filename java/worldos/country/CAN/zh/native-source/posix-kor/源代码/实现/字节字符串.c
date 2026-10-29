#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *字符串) { size_t 长度 = 0; while (字符串[长度]) 长度++; return 长度; }
int strcmp(const char *前端值, const char *后端值) {
    while (*前端值 && *前端值 == *后端值) { 前端值++; 后端值++; }
    return (unsigned char)*前端值 - (unsigned char)*后端值;
}
int memcmp(const void *前端值, const void *后端值, size_t 字节个数) {
    const unsigned char *首位操作数 = 前端值, *第二操作数 = 后端值;
    for (size_t 槽条目 = 0; 槽条目 < 字节个数; 槽条目++) if (首位操作数[槽条目] != 第二操作数[槽条目]) return 首位操作数[槽条目] - 第二操作数[槽条目];
    return 0;
}
void *memcpy(void *目的地址值, const void *原始, size_t 字节个数) {
    unsigned char *首位操作数 = 目的地址值; const unsigned char *第二操作数 = 原始;
    for (size_t 槽条目 = 0; 槽条目 < 字节个数; 槽条目++) 首位操作数[槽条目] = 第二操作数[槽条目];
    return 目的地址值;
}
void *memset(void *目的地址值, int 值, size_t 字节个数) {
    unsigned char *数据 = 目的地址值;
    for (size_t 槽条目 = 0; 槽条目 < 字节个数; 槽条目++) 数据[槽条目] = 值;
    return 目的地址值;
}
int putchar(int 字符) { unsigned char 值 = 字符; return write(1, &值, 1) == 1 ? 值 : EOF; }
int puts(const char *字符串) {
    size_t 长度 = strlen(字符串), 位置 = 0;
    while (位置 < 长度) { ssize_t 结果 = write(1, 字符串 + 位置, 长度 - 位置); if (结果 <= 0) return EOF; 位置 += 结果; }
    return putchar('\n') == EOF ? EOF : 0;
}
