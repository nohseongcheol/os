#include "../命名/計算機連接名稱列.h"
#include "調用.h"
typedef void (*初始設定器方法)(void);
extern 初始設定器方法 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int 開始用戶程式(int);
int 用戶開始(int 已轉發值) {
    for (初始設定器方法 *資料位置 = __init_array_start; 資料位置 < __init_array_end; 資料位置++) (*資料位置)();
    int 結果 = 開始用戶程式(已轉發值);
    for (初始設定器方法 *資料位置 = __fini_array_end; 資料位置 != __fini_array_start;) (*--資料位置)();
    return 結果;
}
void *memset(void *資料位置, int 值, size_t 條目個數) { unsigned char *目的地址資料 = 資料位置; while (條目個數--) *目的地址資料++ = 值; return 資料位置; }
void *memcpy(void *目的地址資料, const void *字符串資料, size_t 條目個數) { unsigned char *首位值 = 目的地址資料; const unsigned char *第二值 = 字符串資料; while (條目個數--) *首位值++ = *第二值++; return 目的地址資料; }
