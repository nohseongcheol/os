#ifndef 原生用戶呼叫標頭
#define 原生用戶呼叫標頭
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=調用 編號, x0..x5=實參, x0=結果/負數值 錯誤. Linux ABI 아님.
static inline intptr_t 用戶調用(uintptr_t 編號, uintptr_t 首位操作數, uintptr_t 第二操作數, uintptr_t 第三操作數,
                                uintptr_t 第四操作數, uintptr_t 第五操作數, uintptr_t 第六操作數) {
    register uintptr_t 寄存器零 __asm__("x0") = 首位操作數;
    register uintptr_t 寄存器一 __asm__("x1") = 第二操作數;
    register uintptr_t 寄存器二 __asm__("x2") = 第三操作數;
    register uintptr_t 寄存器三 __asm__("x3") = 第四操作數;
    register uintptr_t 寄存器四 __asm__("x4") = 第五操作數;
    register uintptr_t 寄存器五 __asm__("x5") = 第六操作數;
    register uintptr_t 寄存器八 __asm__("x8") = 編號;
    __asm__ volatile("svc #0" : "+r"(寄存器零) : "r"(寄存器一), "r"(寄存器二), "r"(寄存器三), "r"(寄存器四), "r"(寄存器五), "r"(寄存器八) : "memory", "cc");
    return (intptr_t)寄存器零;
}
static inline intptr_t 屏幕矩形(unsigned 橫座標座標, unsigned Y_按鈕座標, unsigned 已請求寬度值, unsigned 已請求高度值, unsigned 紅_綠_藍顏色) {
    return 用戶調用(13, 橫座標座標, Y_按鈕座標, 紅_綠_藍顏色, 已請求寬度值, 已請求高度值, 0);
}
static inline intptr_t 用戶記憶體結束(uintptr_t 結尾) { return 用戶調用(8, 結尾, 0, 0, 0, 0, 0); }
static inline intptr_t 讀取屏幕寬度(void) { return 用戶調用(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 讀取屏幕高度(void) { return 用戶調用(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 等待狀態用於屏幕鍵(void) {
    intptr_t 結果 = 用戶調用(16, 0, 0, 0, 0, 0, 0);
    if (結果 < 0) return 結果;
    do { 結果 = 用戶調用(16, 1, 0, 0, 0, 0, 0); } while (結果 == -11);
    用戶調用(16, 2, 0, 0, 0, 0, 0);
    return 結果;
}
static inline intptr_t 用戶實際參數個數(void) { return 用戶調用(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t 用戶實際參數(unsigned 編號, char *內容值, size_t 大小) {
    return 用戶調用(15, 編號, (uintptr_t)內容值, 大小, 0, 0, 0);
}
#endif
