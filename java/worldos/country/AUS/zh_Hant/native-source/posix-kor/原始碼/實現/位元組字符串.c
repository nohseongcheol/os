#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *字符串) { size_t 長度 = 0; while (字符串[長度]) 長度++; return 長度; }
int strcmp(const char *前端值, const char *後端值) {
    while (*前端值 && *前端值 == *後端值) { 前端值++; 後端值++; }
    return (unsigned char)*前端值 - (unsigned char)*後端值;
}
int memcmp(const void *前端值, const void *後端值, size_t 位元組個數) {
    const unsigned char *首位操作數 = 前端值, *第二操作數 = 後端值;
    for (size_t 槽條目 = 0; 槽條目 < 位元組個數; 槽條目++) if (首位操作數[槽條目] != 第二操作數[槽條目]) return 首位操作數[槽條目] - 第二操作數[槽條目];
    return 0;
}
void *memcpy(void *目的地址值, const void *原始, size_t 位元組個數) {
    unsigned char *首位操作數 = 目的地址值; const unsigned char *第二操作數 = 原始;
    for (size_t 槽條目 = 0; 槽條目 < 位元組個數; 槽條目++) 首位操作數[槽條目] = 第二操作數[槽條目];
    return 目的地址值;
}
void *memset(void *目的地址值, int 值, size_t 位元組個數) {
    unsigned char *資料 = 目的地址值;
    for (size_t 槽條目 = 0; 槽條目 < 位元組個數; 槽條目++) 資料[槽條目] = 值;
    return 目的地址值;
}
int putchar(int 字元) { unsigned char 值 = 字元; return write(1, &值, 1) == 1 ? 值 : EOF; }
int puts(const char *字符串) {
    size_t 長度 = strlen(字符串), 位置 = 0;
    while (位置 < 長度) { ssize_t 結果 = write(1, 字符串 + 位置, 長度 - 位置); if (結果 <= 0) return EOF; 位置 += 結果; }
    return putchar('\n') == EOF ? EOF : 0;
}
