#include "../命名/计算机连接名称列.h"
#include "调用.h"
typedef void (*初始设定器方法)(void);
extern 初始设定器方法 __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int 开始用户程序(int);
int 用户开始(int 已转发值) {
    for (初始设定器方法 *数据位置 = __init_array_start; 数据位置 < __init_array_end; 数据位置++) (*数据位置)();
    int 结果 = 开始用户程序(已转发值);
    for (初始设定器方法 *数据位置 = __fini_array_end; 数据位置 != __fini_array_start;) (*--数据位置)();
    return 结果;
}
void *memset(void *数据位置, int 值, size_t 条目个数) { unsigned char *目的地址数据 = 数据位置; while (条目个数--) *目的地址数据++ = 值; return 数据位置; }
void *memcpy(void *目的地址数据, const void *字符串数据, size_t 条目个数) { unsigned char *首位值 = 目的地址数据; const unsigned char *第二值 = 字符串数据; while (条目个数--) *首位值++ = *第二值++; return 目的地址数据; }
