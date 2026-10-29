#ifndef 原生用户调用头部
#define 原生用户调用头部
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=调用 编号, x0..x5=实参, x0=结果/负数值 错误. Linux ABI 아님.
static inline intptr_t 用户调用(uintptr_t 编号, uintptr_t 首位操作数, uintptr_t 第二操作数, uintptr_t 第三操作数,
                                uintptr_t 第四操作数, uintptr_t 第五操作数, uintptr_t 第六操作数) {
    register uintptr_t 寄存器零 __asm__("x0") = 首位操作数;
    register uintptr_t 寄存器一 __asm__("x1") = 第二操作数;
    register uintptr_t 寄存器二 __asm__("x2") = 第三操作数;
    register uintptr_t 寄存器三 __asm__("x3") = 第四操作数;
    register uintptr_t 寄存器四 __asm__("x4") = 第五操作数;
    register uintptr_t 寄存器五 __asm__("x5") = 第六操作数;
    register uintptr_t 寄存器八 __asm__("x8") = 编号;
    __asm__ volatile("svc #0" : "+r"(寄存器零) : "r"(寄存器一), "r"(寄存器二), "r"(寄存器三), "r"(寄存器四), "r"(寄存器五), "r"(寄存器八) : "memory", "cc");
    return (intptr_t)寄存器零;
}
static inline intptr_t 屏幕矩形(unsigned 横坐标坐标, unsigned Y_按钮坐标, unsigned 已请求宽度值, unsigned 已请求高度值, unsigned 红_绿_蓝颜色) {
    return 用户调用(13, 横坐标坐标, Y_按钮坐标, 红_绿_蓝颜色, 已请求宽度值, 已请求高度值, 0);
}
static inline intptr_t 用户内存结束(uintptr_t 结尾) { return 用户调用(8, 结尾, 0, 0, 0, 0, 0); }
static inline intptr_t 读取屏幕宽度(void) { return 用户调用(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 读取屏幕高度(void) { return 用户调用(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 等待状态用于屏幕键(void) {
    intptr_t 结果 = 用户调用(16, 0, 0, 0, 0, 0, 0);
    if (结果 < 0) return 结果;
    do { 结果 = 用户调用(16, 1, 0, 0, 0, 0, 0); } while (结果 == -11);
    用户调用(16, 2, 0, 0, 0, 0, 0);
    return 结果;
}
static inline intptr_t 用户参数个数(void) { return 用户调用(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t 用户参数(unsigned 编号, char *内容值, size_t 大小) {
    return 用户调用(15, 编号, (uintptr_t)内容值, 大小, 0, 0, 0);
}
#endif
