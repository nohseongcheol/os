#include "string.h"
size_t strlen(const char *字符串資料) { const char *資料位置 = 字符串資料; while (*資料位置) 資料位置++; return 資料位置 - 字符串資料; }
int memcmp(const void *首位值, const void *第二值, size_t 項目個數) { const unsigned char *橫座標座標 = 首位值, *Y_按鈕座標 = 第二值; while (項目個數--) { if (*橫座標座標 != *Y_按鈕座標) return (int)*橫座標座標 - *Y_按鈕座標; 橫座標座標++; Y_按鈕座標++; } return 0; }
void *memmove(void *目的地址資料, const void *字符串資料, size_t 項目個數) { unsigned char *橫座標座標 = 目的地址資料; const unsigned char *Y_按鈕座標 = 字符串資料; if (橫座標座標 < Y_按鈕座標) { for (size_t 序數索引 = 0; 序數索引 < 項目個數; 序數索引++) 橫座標座標[序數索引] = Y_按鈕座標[序數索引]; } else { while (項目個數) { 項目個數--; 橫座標座標[項目個數] = Y_按鈕座標[項目個數]; } } return 目的地址資料; }
int strncmp(const char *首位值, const char *第二值, size_t 項目個數) { while (項目個數--) { unsigned char 橫座標座標 = *首位值++, Y_按鈕座標 = *第二值++; if (橫座標座標 != Y_按鈕座標) return (int)橫座標座標-Y_按鈕座標; if (!橫座標座標) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *字符串資料, char **結束偏移, int 背景值) {
    const char *開始偏移 = 字符串資料; unsigned long 值 = 0; int 編碼狀態值 = 1, 任意值 = 0;
    while (*字符串資料 == ' ' || (*字符串資料 >= 9 && *字符串資料 <= 13)) 字符串資料++;
    if (*字符串資料 == '-' || *字符串資料 == '+') { if (*字符串資料 == '-') 編碼狀態值 = -1; 字符串資料++; }
    if (背景值 == 0) 背景值 = 10;
    while (*字符串資料 >= '0' && *字符串資料 <= '9' && *字符串資料 - '0' < 背景值) {
        unsigned 數字值 = *字符串資料++ - '0'; 任意值 = 1;
        if (值 > (0x7ffffffffffffffful - 數字值) / (unsigned)背景值) 值 = 0x7ffffffffffffffful;
        else 值 = 值 * 背景值 + 數字值;
    }
    if (結束偏移) *結束偏移 = (char *)(任意值 ? 字符串資料 : 開始偏移); return 編碼狀態值 > 0 ? (long)值 : -(long)值;
}
int atoi(const char *字符串資料) { return (int)strtol(字符串資料, 0, 10); }
