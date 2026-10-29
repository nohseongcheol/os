#include "string.h"
size_t strlen(const char *文字列データ) { const char *データ位置 = 文字列データ; while (*データ位置) データ位置++; return データ位置 - 文字列データ; }
int memcmp(const void *先頭位置値, const void *第二値, size_t 項目個数) { const unsigned char *横座標 = 先頭位置値, *縦座標 = 第二値; while (項目個数--) { if (*横座標 != *縦座標) return (int)*横座標 - *縦座標; 横座標++; 縦座標++; } return 0; }
void *memmove(void *宛先データ, const void *文字列データ, size_t 項目個数) { unsigned char *横座標 = 宛先データ; const unsigned char *縦座標 = 文字列データ; if (横座標 < 縦座標) { for (size_t 序数添字 = 0; 序数添字 < 項目個数; 序数添字++) 横座標[序数添字] = 縦座標[序数添字]; } else { while (項目個数) { 項目個数--; 横座標[項目個数] = 縦座標[項目個数]; } } return 宛先データ; }
int strncmp(const char *先頭位置値, const char *第二値, size_t 項目個数) { while (項目個数--) { unsigned char 横座標 = *先頭位置値++, 縦座標 = *第二値++; if (横座標 != 縦座標) return (int)横座標-縦座標; if (!横座標) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *文字列データ, char **終端位置変位量, int 背景値) {
    const char *変位量開始処理 = 文字列データ; unsigned long 値 = 0; int 符号化状態値 = 1, 任意値 = 0;
    while (*文字列データ == ' ' || (*文字列データ >= 9 && *文字列データ <= 13)) 文字列データ++;
    if (*文字列データ == '-' || *文字列データ == '+') { if (*文字列データ == '-') 符号化状態値 = -1; 文字列データ++; }
    if (背景値 == 0) 背景値 = 10;
    while (*文字列データ >= '0' && *文字列データ <= '9' && *文字列データ - '0' < 背景値) {
        unsigned 桁値 = *文字列データ++ - '0'; 任意値 = 1;
        if (値 > (0x7ffffffffffffffful - 桁値) / (unsigned)背景値) 値 = 0x7ffffffffffffffful;
        else 値 = 値 * 背景値 + 桁値;
    }
    if (終端位置変位量) *終端位置変位量 = (char *)(任意値 ? 文字列データ : 変位量開始処理); return 符号化状態値 > 0 ? (long)値 : -(long)値;
}
int atoi(const char *文字列データ) { return (int)strtol(文字列データ, 0, 10); }
