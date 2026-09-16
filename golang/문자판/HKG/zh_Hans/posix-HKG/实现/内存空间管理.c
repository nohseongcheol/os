/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <通用函数.h>
#include <字符串与内存内容.h>
#include <输入输出与执行.h>
#include <整数类型.h>
#include <整数极限.h>
#include <错误编号.h>

/* Single-thread runtime. Reuse and coalesce freed blocks; do not shrink brk.
 * A block header and every returned address are 16-byte aligned on i386.
 * Callers must not move brk backwards across live allocations. */
struct 内存区块 {
    大小类型 容量;
    struct 内存区块 *下一区块;
    int 可用标志;
    unsigned int 对齐填充长度;
};
static struct 内存区块 *首个区块;

void *分配内存空间(大小类型 大小)
{
    struct 内存区块 *当前位置 = 首个区块, *最后区块 = 空地址, *分配原地址;
    大小类型 总长度, 对齐填充长度;
    void *地址;
    if (!大小) 大小 = 1;
    if (大小 > (大小类型)整数最大值 - 2 * sizeof(struct 内存区块)) { 错误编号 = 错误内存不足; return 空地址; }
    大小 = (大小 + 15U) & ~15U;
    while (当前位置) {
        if (当前位置->可用标志 && 当前位置->容量 >= 大小) {
            if (当前位置->容量 - 大小 >= sizeof(struct 内存区块) + 16U) {
                分配原地址 = (struct 内存区块 *)((unsigned char *)(当前位置 + 1) + 大小);
                分配原地址->容量 = 当前位置->容量 - 大小 - sizeof(*分配原地址);
                分配原地址->下一区块 = 当前位置->下一区块;
                分配原地址->可用标志 = 1;
                当前位置->下一区块 = 分配原地址;
                当前位置->容量 = 大小;
            }
            当前位置->可用标志 = 0;
            return 当前位置 + 1;
        }
        最后区块 = 当前位置; 当前位置 = 当前位置->下一区块;
    }
    地址 = 移动动态存储末端(0);
    if (地址 == (void *)-1) return 空地址;
    对齐填充长度 = (0U - (地址宽度无符号整数)地址) & 15U;
    总长度 = 对齐填充长度 + sizeof(struct 内存区块) + 大小;
    if ((地址宽度无符号整数)地址 > (地址宽度无符号整数)整数最大值 - 总长度) { 错误编号 = 错误内存不足; return 空地址; }
    地址 = 移动动态存储末端((int)总长度);
    if (地址 == (void *)-1) return 空地址;
    分配原地址 = (struct 内存区块 *)((unsigned char *)地址 + 对齐填充长度);
    分配原地址->容量 = 大小; 分配原地址->下一区块 = 空地址; 分配原地址->可用标志 = 0;
    if (最后区块) 最后区块->下一区块 = 分配原地址;
    else 首个区块 = 分配原地址;
    return 分配原地址 + 1;
}

void 释放内存空间(void *地址)
{
    struct 内存区块 *当前位置;
    if (!地址) return;
    ((struct 内存区块 *)地址 - 1)->可用标志 = 1;
    当前位置 = 首个区块;
    while (当前位置 && 当前位置->下一区块) {
        struct 内存区块 *下一区块 = 当前位置->下一区块;
        if (当前位置->可用标志 && 下一区块->可用标志 &&
            (unsigned char *)(当前位置 + 1) + 当前位置->容量 == (unsigned char *)下一区块) {
            当前位置->容量 += sizeof(*下一区块) + 下一区块->容量;
            当前位置->下一区块 = 下一区块->下一区块;
        } else 当前位置 = 下一区块;
    }
}

void *分配清零数组空间(大小类型 数量, 大小类型 元素大小)
{
    void *地址;
    if (元素大小 && 数量 > (大小类型)-1 / 元素大小) { 错误编号 = 错误内存不足; return 空地址; }
    地址 = 分配内存空间(数量 * 元素大小);
    if (地址) 用值填充内存区域(地址, 0, 数量 * 元素大小);
    return 地址;
}

void *调整内存空间大小(void *地址, 大小类型 大小)
{
    void *目标位置;
    struct 内存区块 *当前位置;
    if (!地址) return 分配内存空间(大小);
    /* Documented zero-size choice: retain a valid, freeable minimum block. */
    if (!大小) 大小 = 1;
    当前位置 = (struct 内存区块 *)地址 - 1;
    if (大小 <= 当前位置->容量) return 地址;
    目标位置 = 分配内存空间(大小);
    if (!目标位置) return 空地址;
    复制内存内容(目标位置, 地址, 当前位置->容量);
    释放内存空间(地址);
    return 目标位置;
}
