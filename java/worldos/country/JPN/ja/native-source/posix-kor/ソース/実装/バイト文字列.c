#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *文字列) { size_t 長さ = 0; while (文字列[長さ]) 長さ++; return 長さ; }
int strcmp(const char *前面値, const char *後端値) {
    while (*前面値 && *前面値 == *後端値) { 前面値++; 後端値++; }
    return (unsigned char)*前面値 - (unsigned char)*後端値;
}
int memcmp(const void *前面値, const void *後端値, size_t バイト個数) {
    const unsigned char *先頭位置被演算子 = 前面値, *第二被演算子 = 後端値;
    for (size_t 槽入口 = 0; 槽入口 < バイト個数; 槽入口++) if (先頭位置被演算子[槽入口] != 第二被演算子[槽入口]) return 先頭位置被演算子[槽入口] - 第二被演算子[槽入口];
    return 0;
}
void *memcpy(void *宛先値, const void *原本, size_t バイト個数) {
    unsigned char *先頭位置被演算子 = 宛先値; const unsigned char *第二被演算子 = 原本;
    for (size_t 槽入口 = 0; 槽入口 < バイト個数; 槽入口++) 先頭位置被演算子[槽入口] = 第二被演算子[槽入口];
    return 宛先値;
}
void *memset(void *宛先値, int 値, size_t バイト個数) {
    unsigned char *データ = 宛先値;
    for (size_t 槽入口 = 0; 槽入口 < バイト個数; 槽入口++) データ[槽入口] = 値;
    return 宛先値;
}
int putchar(int 文字) { unsigned char 値 = 文字; return write(1, &値, 1) == 1 ? 値 : EOF; }
int puts(const char *文字列) {
    size_t 長さ = strlen(文字列), 位置 = 0;
    while (位置 < 長さ) { ssize_t 結果 = write(1, 文字列 + 位置, 長さ - 位置); if (結果 <= 0) return EOF; 位置 += 結果; }
    return putchar('\n') == EOF ? EOF : 0;
}
