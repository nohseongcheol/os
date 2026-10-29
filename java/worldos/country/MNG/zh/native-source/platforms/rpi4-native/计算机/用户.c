#include "../命名/计算机连接名称列.h"
#include "屏幕信息.h"
// EL0 执行命令 计算机 层值. 文件 数据/정책은 기존 AOT Java 커널에 위임한다.
#include "用户.h"
#include "文件ABI.h"
#include "网络ABI.h"
#include "../通信网络/通信网络.h"
extern int32_t Java网络远程(int32_t), Java流地址(int32_t);
#define 计算机寄存器(首位值) (*(volatile uint32_t *)(uintptr_t)(首位值))
#define 中断分发器 0xff841000ul
#define 中断CPU接口 0xff842000ul
#define 页大小 4096ul
#define 存取标记 (1ul << 10)
#define 无执行权限 (1ul << 53)
#define 用户无执行 (1ul << 54)
#define 常规内存 ((1ul << 2) | (3ul << 8) | 存取标记)
#define 内核页 (3ul | 常规内存 | 无执行权限 | 用户无执行)
#define 用户读取写入 (3ul | 常规内存 | (1ul << 6) | 无执行权限 | 用户无执行)
#define 用户读取仅用 (3ul | 常规内存 | (3ul << 6) | 无执行权限 | 用户无执行)
#define 用户读取执行 (3ul | 常规内存 | (3ul << 6) | 无执行权限)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t 板写字符(uintptr_t), 板取字符(void), 板经过毫秒(void);
extern uintptr_t 板像素(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t 板帧缓冲(void);
extern uintptr_t 板终端(uintptr_t);
extern int 终端待处理(void);
extern int32_t Java交互壳交互式(void);
extern int32_t Java路径开始(int32_t), Java路径字节(int32_t,int32_t);
extern int32_t Java创建目录(void), Java移除目录(void), Java条目种类(void);
extern int 调用屏幕(int,unsigned,int,int,int,int,int),屏幕文本(int,int,const uint32_t *,unsigned);
extern void 初始化屏幕(int),屏幕按下(int,unsigned);
extern int 用户恢复执行(用户帧 *,void *);
extern void 用户浮点保存(void *);
extern int 用户进入(uintptr_t 条目分, uintptr_t 栈存储装置, uintptr_t 已转发值);
extern void 用户发回(void);
extern void 内核致命停止(const char *) __attribute__((noreturn));
static uint64_t 根地址[512] __attribute__((aligned(4096)));
static uint64_t 中间[4][512] __attribute__((aligned(4096)));
static uint64_t 页列表[用户页个数] __attribute__((aligned(4096)));
static uint8_t 权限列列表[用户页个数];
static int 活跃, 文件列表[16], Linux调用约定;
static unsigned 套接字端点列[24];
extern int32_t Java网络套接字(int32_t, int32_t, int32_t), Java网络绑定(int32_t, int32_t, int32_t);
extern int32_t Java网络放入(int32_t, int32_t), Java网络获取(int32_t), Java网络发送(int32_t, int32_t, int32_t, int32_t);
extern int32_t Java网络接收操作(int32_t, int32_t), Java网络端口(int32_t), Java网络地址(int32_t), Java网络对端(int32_t), Java网络关闭(int32_t);
extern int32_t Java流创建(void),Java流绑定(int32_t,int32_t,int32_t),Java流侦听(int32_t,int32_t),Java流连接(int32_t,int32_t,int32_t),Java流接受(int32_t),Java流读取(int32_t,int32_t),Java流写入(int32_t,int32_t),Java流端口(int32_t),Java流对端(int32_t),Java流关闭(int32_t);
static int 关闭套接字端点(unsigned 文件句柄){return 文件句柄<40?Java网络关闭(文件句柄):Java流关闭(文件句柄);}
static uint64_t 频率, 截止时间时间;
static uintptr_t 堆结束;
// 内核值 셸이 준비한 UTF-8 实参. EL0에는 复制值 호출만 제공한다.
static unsigned 已转发参数个数, 已转发参数长度[8];
static unsigned char 已转发参数[8][256];
typedef struct {
    int 已暂停状态,交互式,Linux调用约定,文件列表[16]; unsigned 套接字端点列[24],参数列个数,参数长度[8];
    unsigned char 参数数组[8][256],权限列列表[用户页个数];
    uintptr_t 堆存储装置; 用户帧 执行状态帧;
    unsigned char 浮点型分状态[528] __attribute__((aligned(16)));
} 已保存进程;
static 已保存进程 已保存[4];
static int 所有者对象,交互式;
static uint32_t 用户编号[4], 用户开始时间[4], 用户累积时间[4], 用户执行状态时间[4], 下一用户编号=10;
static unsigned char 用户命令名称[4][288];
uint32_t 读取用户状态(unsigned 条目值, unsigned 编号) {
    unsigned 位置索引=编号&3;
    int 状态值=(活跃 && 所有者对象==(int)位置索引) ? 1 : 已保存[位置索引].已暂停状态 ? 2 : 0;
    if (条目值==0) return 状态值;
    if (!状态值) return 0;
    if (条目值==1) return 用户编号[位置索引];
    if (条目值==2) {
        unsigned char *页面列列表=状态值==1?权限列列表:已保存[位置索引].权限列列表;
        unsigned 页个数=0; for (unsigned 序数索引=0; 序数索引<用户页个数; 序数索引++) if(页面列列表[序数索引]) 页个数++;
        return 页个数*4;
    }
    if (条目值==3) return (uint32_t)板经过毫秒()-用户开始时间[位置索引];
    if (条目值==4) return 用户累积时间[位置索引]+(状态值==1?(uint32_t)板经过毫秒()-用户执行状态时间[位置索引]:0);
    if (条目值==5) return 编号/4<sizeof(用户命令名称[0])?用户命令名称[位置索引][编号/4]:0;
    return 0;
}
uintptr_t 板调用参数开始位置(uintptr_t 条目个数) {
    if (活跃 || 条目个数 > 8) return (uint32_t)-22;
    已转发参数个数 = 条目个数;
    memset(已转发参数长度, 0, sizeof(已转发参数长度));
    memset(已转发参数, 0, sizeof(已转发参数));
    return 0;
}
uintptr_t 板调用参数字节(uintptr_t 查找索引, uintptr_t 当前位置, uintptr_t 字节数据) {
    if (活跃 || 查找索引 >= 已转发参数个数 || 当前位置 >= 255 || 当前位置 != 已转发参数长度[查找索引] || !字节数据 || 字节数据 > 255)
        return (uint32_t)-22;
    已转发参数[查找索引][当前位置] = 字节数据;
    已转发参数长度[查找索引] = 当前位置 + 1;
    return 0;
}
static void 同步表列(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t 时钟值(void) { uint64_t 临时数据; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(临时数据)); return 临时数据; }
static void 停止超时(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    计算机寄存器(中断分发器 + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void 开始超时(void) {
    uint64_t 间距值 = 频率 * 2, 启用 = 1;
    截止时间时间 = 时钟值() + 间距值;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(间距值), "r"(启用) : "memory");
}
void 用户系统初始化操作(void) {
    for (unsigned 数据块 = 0; 数据块 < 4; 数据块++) {
        根地址[数据块] = (uintptr_t)中间[数据块] | 3;
        for (unsigned 序数索引 = 0; 序数索引 < 512; 序数索引++) {
            uintptr_t 地址 = ((uintptr_t)数据块 << 30) | ((uintptr_t)序数索引 << 21);
            中间[数据块][序数索引] = 地址 | 1 | 存取标记 | 用户无执行;
            if (地址 >= 0xfc000000ul) 中间[数据块][序数索引] |= 无执行权限; // Device-nGnRnE
            else 中间[数据块][序数索引] |= 常规内存; // Normal, non-cacheable
        }
    }
    for (unsigned 第二值 = 0; 第二值 < 用户页个数 / 512; 第二值++)
        中间[0][(用户基底 >> 21) + 第二值] = (uintptr_t)(页列表 + 第二值 * 512) | 3;
    for (unsigned 序数索引 = 0; 序数索引 < 用户页个数; 序数索引++) 页列表[序数索引] = (用户基底 + 序数索引 * 页大小) | 内核页;
    uint64_t 内存属性寄存器 = 0x4400, 地址翻译控制 = 32 | (3ul << 12) | (1ul << 23), 系统控制寄存器;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(内存属性寄存器), "r"(地址翻译控制), "r"((uintptr_t)根地址) : "memory");
    同步表列();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(系统控制寄存器));
    系统控制寄存器 = (系统控制寄存器 & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(系统控制寄存器) : "memory");
    uint64_t 浮点型分状态 = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(浮点型分状态) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(频率));
    停止超时();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 条目分值 때만 允许值.
    计算机寄存器(中断分发器) = 0;
    计算机寄存器(中断分发器 + 0x180) = 0xffffffff;
    计算机寄存器(中断分发器 + 0x80) = 0xffffffff;
    计算机寄存器(中断分发器 + 0x280) = 1u << 30;
    计算机寄存器(中断分发器 + 0x41c) = 0x80808080;
    计算机寄存器(中断分发器 + 0x100) = 1u << 30;
    计算机寄存器(中断CPU接口 + 4) = 0xff;
    计算机寄存器(中断CPU接口 + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 是否常规 확인할 数 있다.
    int 安全性 = (计算机寄存器(中断分发器 + 4) & (1u << 10)) != 0;
    计算机寄存器(中断分发器) = 安全性 ? 1 : 3;
    计算机寄存器(中断CPU接口) = 安全性 ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char 标识码[16]; uint16_t 类型分类, 计算机类型; uint32_t 版本编号;
    uint64_t 条目分, 程序头部偏移, 区段头部偏移; uint32_t 配置项位列;
    uint16_t 可执行文件头部大小, 程序头部条目大小, 程序头部个数, 区段头部条目大小, 区段头部个数, 区段名称表索引;
} ELF头部;
typedef struct { uint32_t 类型分类, 配置项位列; uint64_t 偏移值, 地址, 物理地址, 文件区域大小, 内存区大小, 对齐边界位置; } ELF程序;
_Static_assert(sizeof(ELF头部) == 64 && sizeof(ELF程序) == 56, "ELF layout");
_Static_assert(sizeof(用户帧) == 272, "exception assembly layout");
static int 已包含(uint64_t 偏移值, uint64_t 大小, uint64_t 结束偏移) {
    return 偏移值 <= 结束偏移 && 大小 <= 结束偏移 - 偏移值;
}
static int 检查辅助信息(const unsigned char *数据位置, size_t 大小) {
    size_t 当前位置 = 0;
    while (已包含(当前位置, 12, 大小)) {
        uint32_t 词法用单词列[3]; memcpy(词法用单词列, 数据位置 + 当前位置, 12); 当前位置 += 12;
        uint64_t 名称区域大小 = ((uint64_t)词法用单词列[0] + 3) & ~3ul;
        uint64_t 描述区大小 = ((uint64_t)词法用单词列[1] + 3) & ~3ul;
        if (!已包含(当前位置, 名称区域大小, 大小) || !已包含(当前位置 + 名称区域大小, 描述区大小, 大小)) return 0;
        const unsigned char 名称[] = {'J','K','O','R','O','S',0};
        int 是否相等 = 词法用单词列[0] == sizeof(名称) && 词法用单词列[1] == 4 && 词法用单词列[2] == 1;
        if (是否相等) for (unsigned 序数索引 = 0; 序数索引 < sizeof(名称); 序数索引++) if (数据位置[当前位置 + 序数索引] != 名称[序数索引]) 是否相等 = 0;
        uint32_t 版本编号 = 0;
        if (是否相等) memcpy(&版本编号, 数据位置 + 当前位置 + 名称区域大小, 4);
        if (是否相等 && 版本编号 == 1) return 1;
        当前位置 += 名称区域大小 + 描述区大小;
    }
    return 0;
}
static int 有效性校验ELF(const unsigned char *数据, size_t 大小, int Linux模式) {
    if (大小 < sizeof(ELF头部)) return 用户可执行文件错误;
    ELF头部 可执行文件头部; memcpy(&可执行文件头部, 数据, sizeof(可执行文件头部));
    if (可执行文件头部.标识码[0] != 127 || 可执行文件头部.标识码[1] != 'E' || 可执行文件头部.标识码[2] != 'L' || 可执行文件头部.标识码[3] != 'F' ||
        可执行文件头部.标识码[4] != 2 || 可执行文件头部.标识码[5] != 1 || 可执行文件头部.标识码[6] != 1 || (可执行文件头部.标识码[7] != 0 && (!Linux模式 || 可执行文件头部.标识码[7] != 3)) ||
        可执行文件头部.类型分类 != 2 || 可执行文件头部.计算机类型 != 183 || 可执行文件头部.版本编号 != 1 || 可执行文件头部.配置项位列 || 可执行文件头部.可执行文件头部大小 != sizeof(可执行文件头部) ||
        可执行文件头部.程序头部条目大小 != sizeof(ELF程序) || !可执行文件头部.程序头部个数 || 可执行文件头部.程序头部个数 > 16 ||
        可执行文件头部.程序头部偏移 < sizeof(可执行文件头部) || !已包含(可执行文件头部.程序头部偏移, (uint64_t)可执行文件头部.程序头部个数 * sizeof(ELF程序), 大小)) return 用户可执行文件错误;
    uint8_t 已使用容量[(用户映像结束 - 用户基底) / 页大小] = {0};
    int 有效条目分 = 0, ABI正常确认 = 0, 载入项 = 0;
    for (unsigned 序数索引 = 0; 序数索引 < 可执行文件头部.程序头部个数; 序数索引++) {
        ELF程序 数据位置; memcpy(&数据位置, 数据 + 可执行文件头部.程序头部偏移 + 序数索引 * sizeof(数据位置), sizeof(数据位置));
        if (数据位置.类型分类 == 4) {
            if (!已包含(数据位置.偏移值, 数据位置.文件区域大小, 大小)) return 用户可执行文件错误;
            if (检查辅助信息(数据 + 数据位置.偏移值, 数据位置.文件区域大小)) ABI正常确认 = 1;
            continue;
        }
        if (数据位置.类型分类 == 0 || 数据位置.类型分类 == 6 || (数据位置.类型分类 == 0x6474e551 && !(数据位置.配置项位列 & 1))) continue;
        if (数据位置.类型分类 != 1) return 用户可执行文件错误; // PT_INTERP, DYNAMIC, TLS 是否不支持
        if (!数据位置.内存区大小) continue;
        if (数据位置.配置项位列 & ~7u || !(数据位置.配置项位列 & 4) || (数据位置.配置项位列 & 3) == 3 || 数据位置.文件区域大小 > 数据位置.内存区大小 ||
            (数据位置.文件区域大小 && !已包含(数据位置.偏移值, 数据位置.文件区域大小, 大小)) || 数据位置.地址 < 用户基底 ||
            !已包含(数据位置.地址, 数据位置.内存区大小, 用户映像结束) ||
            (!Linux模式 && ((数据位置.地址 & (页大小 - 1)) || (数据位置.偏移值 & (页大小 - 1)) || 数据位置.对齐边界位置 != 页大小)) ||
            (Linux模式 && (((数据位置.地址 ^ 数据位置.偏移值) & (页大小 - 1)) || !数据位置.对齐边界位置 ||
                (数据位置.对齐边界位置 & (数据位置.对齐边界位置 - 1)) || 数据位置.对齐边界位置 > 0x200000 || ((数据位置.地址 ^ 数据位置.偏移值) & (数据位置.对齐边界位置 - 1))))) return 用户可执行文件错误;
        unsigned 首位条目 = (数据位置.地址 - 用户基底) / 页大小;
        unsigned 条目个数 = ((数据位置.地址 & (页大小 - 1)) + 数据位置.内存区大小 + 页大小 - 1) / 页大小;
        for (unsigned 页值 = 首位条目; 页值 < 首位条目 + 条目个数; 页值++) {
            if (已使用容量[页值]) return 用户可执行文件错误;
            已使用容量[页值] = 1;
        }
        if ((数据位置.配置项位列 & 1) && 可执行文件头部.条目分 >= 数据位置.地址 && 可执行文件头部.条目分 < 数据位置.地址 + 数据位置.文件区域大小 && !(可执行文件头部.条目分 & 3)) 有效条目分 = 1;
        载入项++;
    }
    return 有效条目分 && (Linux模式 ? !ABI正常确认 : ABI正常确认) && 载入项 ? 0 : 用户可执行文件错误;
}
int 用户有效性校验ELF(const unsigned char *数据, size_t 大小) { return 有效性校验ELF(数据, 大小, 0); }
static void 页导航(uintptr_t 地址, uint64_t 配置项位列, unsigned 存取权限列) {
    unsigned 查找索引 = (地址 - 用户基底) / 页大小;
    页列表[查找索引] = 地址 | 配置项位列;
    权限列列表[查找索引] = 存取权限列;
}
static int 用户范围(uintptr_t 地址, size_t 条目个数, int 写入中) {
    if (地址 < 用户基底 || !已包含(地址, 条目个数, 用户结束)) return 0;
    if (!条目个数) return 1;
    unsigned 首位条目 = (地址 - 用户基底) / 页大小, 最后项目 = (地址 + 条目个数 - 1 - 用户基底) / 页大小;
    for (unsigned 序数索引 = 首位条目; 序数索引 <= 最后项目; 序数索引++) if (!(权限列列表[序数索引] & (写入中 ? 2 : 1))) return 0;
    return 1;
}
static int 复制路径(uintptr_t 地址, char *路径) {
    for (unsigned 序数索引 = 0; 序数索引 < 65; 序数索引++) {
        if (!用户范围(地址, 1, 0)) return -14;
        路径[序数索引] = *(const char *)地址++;
        if (!路径[序数索引]) return 0;
    }
    return -36;
}
static intptr_t 内核结果(intptr_t 结果) { return 结果 < 0 ? -错误编号 : 结果; }
static int 已映射文件描述符(uint64_t 文件句柄) { return 文件句柄 >= 3 && 文件句柄 < 19 ? 文件列表[文件句柄 - 3] : -1; }
static int 套接字端点所有者(uint64_t 文件句柄) { return 文件句柄 >= 32 && 文件句柄 < 56 && 套接字端点列[文件句柄 - 32]; }
static int 地址输入(uintptr_t 指向中值, size_t 长度, struct pk_sockaddr_in *地址) {
    if (长度 != sizeof(*地址)) return -22;
    if (!用户范围(指向中值, 长度, 0)) return -14;
    memcpy(地址, (const void *)指向中值, sizeof(*地址));
    return 地址->sin_family == AF_INET ? 0 : -97;
}
static int 地址输出检查(uintptr_t 指向中值, uintptr_t 长度指针, pk_socklen_t *缓冲容量) {
    if (!用户范围(长度指针, sizeof(*缓冲容量), 1)) return -14;
    memcpy(缓冲容量, (const void *)长度指针, sizeof(*缓冲容量));
    if (*缓冲容量 > sizeof(struct pk_sockaddr_in)) *缓冲容量 = sizeof(struct pk_sockaddr_in);
    if (*缓冲容量 && !用户范围(指向中值, *缓冲容量, 1)) return -14;
    return 0;
}
static void 地址输出(uintptr_t 指向中值, uintptr_t 长度指针, pk_socklen_t 缓冲容量, int 地址, int 端口编号) {
    struct pk_sockaddr_in 值; memset(&值, 0, sizeof(值));
    值.sin_family = AF_INET; 值.sin_port = pk_htons(端口编号); 值.sin_addr.s_addr = pk_htonl(地址);
    if (缓冲容量) memcpy((void *)指向中值, &值, 缓冲容量);
    pk_socklen_t 长度 = sizeof(值); memcpy((void *)长度指针, &长度, sizeof(长度));
}
extern uintptr_t 板信道(uintptr_t, uintptr_t);
static intptr_t 原生系统调用(用户帧 *文件条目) {
    uintptr_t 首位值 = 文件条目->寄存器数据[0], 第二值 = 文件条目->寄存器数据[1], 字符代码 = 文件条目->寄存器数据[2];
    char 路径[65];
    int 文件句柄, 结果;
    switch (文件条目->寄存器数据[8]) {
    case 0: return 1; // 内置 ABI 버전
    case 1: // write: 指针 전체를 검사한 后端值 输出/文件 更改值
        if (字符代码 > 65536) return -22;
        if (!用户范围(第二值, 字符代码, 0)) return -14;
        if (首位值 == 1 || 首位值 == 2) {
            uint64_t 开始输出=时钟值();
            for (size_t 序数索引 = 0; 序数索引 < 字符代码; 序数索引++) 板信道(首位值, ((const unsigned char *)第二值)[序数索引]);
            /* 큰 tty를 그린 内核值 시간만 돌려준다. EL0 计算结果 기한은 늘리지 않는다. */
            if(交互式){
                截止时间时间+=时钟值()-开始输出;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(截止时间时间) : "memory");
            }
            return 字符代码;
        }
        if(首位值>=40&&套接字端点所有者(首位值)){
            size_t 项目个数=字符代码>512?512:字符代码;for(size_t 序数索引=0;序数索引<项目个数;序数索引++)Java网络放入(序数索引,((const unsigned char *)第二值)[序数索引]);return Java流写入(首位值,项目个数);
        }
        文件句柄 = 已映射文件描述符(首位值); if (文件句柄 < 0) return -9;
        return 内核结果(pk_write(文件句柄, (const void *)第二值, 字符代码));
    case 2:
        if (字符代码 > 65536) return -22;
        if (!用户范围(第二值, 字符代码, 1)) return -14;
        if (首位值 == 0) {
            size_t 项目个数 = 0;
            while (项目个数 < 字符代码) {
                int 字符值 = (int32_t)板取字符(); if (字符值 == -2) return 项目个数; if (字符值 < 0) break;
                ((unsigned char *)第二值)[项目个数++] = 字符值;
            }
            return 项目个数 ? (intptr_t)项目个数 : (字符代码 ? -11 : 0);
        }
        if(首位值>=40&&套接字端点所有者(首位值)){
            结果=Java流读取(首位值,字符代码>512?512:字符代码);if(结果>0)for(int 序数索引=0;序数索引<结果;序数索引++)((unsigned char *)第二值)[序数索引]=Java网络获取(序数索引);return 结果;
        }
        文件句柄 = 已映射文件描述符(首位值); if (文件句柄 < 0) return -9;
        return 内核结果(pk_read(文件句柄, (void *)第二值, 字符代码));
    case 3:
        结果 = 复制路径(首位值, 路径); if (结果) return 结果;
        if (第二值 > 0x7ff) return -22;
        for (unsigned 序数索引 = 0; 序数索引 < 16; 序数索引++) if (文件列表[序数索引] < 0) {
            文件句柄 = pk_open(路径, (int)第二值, 0600);
            if (文件句柄 < 0) return -错误编号;
            文件列表[序数索引] = 文件句柄; return 序数索引 + 3;
        }
        return -24;
    case 4:
        if (套接字端点所有者(首位值)) { 结果 = 关闭套接字端点(首位值); if (!结果) 套接字端点列[首位值 - 32] = 0; return 结果; }
        文件句柄 = 已映射文件描述符(首位值); if (文件句柄 < 0) return -9;
        结果 = pk_close(文件句柄); if (!结果) 文件列表[首位值 - 3] = -1;
        return 内核结果(结果);
    case 5:
        文件句柄 = 已映射文件描述符(首位值); if (文件句柄 < 0) return -9;
        if (字符代码 > 2) return -22;
        return 内核结果(pk_lseek(文件句柄, (int64_t)第二值, 字符代码));
    case 7: return 板经过毫秒();
    case 8: { // brk: 별도 用户 RW/NX 堆值, 새로 노출되는 페이지는 0으로 初始化
        if (!首位值) return 堆结束;
        if (首位值 < 用户映像结束 || 首位值 > 用户堆结束) return -12;
        uintptr_t 旧页面列 = (堆结束 + 页大小 - 1) & ~(页大小 - 1);
        uintptr_t 新建页面列 = (首位值 + 页大小 - 1) & ~(页大小 - 1);
        if (新建页面列 > 旧页面列) {
            for (uintptr_t 数据位置 = 旧页面列; 数据位置 < 新建页面列; 数据位置 += 页大小) 页导航(数据位置, 内核页, 0);
            同步表列();
            memset((void *)旧页面列, 0, 新建页面列 - 旧页面列);
            for (uintptr_t 数据位置 = 旧页面列; 数据位置 < 新建页面列; 数据位置 += 页大小) 页导航(数据位置, 用户读取写入, 3);
        } else {
            for (uintptr_t 数据位置 = 新建页面列; 数据位置 < 旧页面列; 数据位置 += 页大小) {
                页列表[(数据位置 - 用户基底) / 页大小] = 0; 权限列列表[(数据位置 - 用户基底) / 页大小] = 0;
            }
        }
        堆结束 = 首位值; 同步表列(); return 首位值;
    }
    case 9:
        文件句柄 = 已映射文件描述符(首位值); return 文件句柄 < 0 ? -9 : 内核结果(pk_size(文件句柄));
    case 10:
        文件句柄 = 已映射文件描述符(首位值); return 文件句柄 < 0 ? -9 : 内核结果(pk_ftruncate(文件句柄, (int64_t)第二值));
    case 11:
        结果 = 复制路径(首位值, 路径); return 结果 ? 结果 : 内核结果(pk_unlink(路径));
    case 12:
        文件句柄 = 已映射文件描述符(首位值); return 文件句柄 < 0 ? -9 : 内核结果(pk_fsync(文件句柄));
    case 13: { // 그래픽 기초 API: 用户 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t 已请求宽度值 = 文件条目->寄存器数据[3], 已请求高度值 = 文件条目->寄存器数据[4];
        if (!板帧缓冲()) return -19;
        uintptr_t 屏幕跨度 = 板屏幕宽度(), 屏幕长度 = 板屏幕高度();
        if (首位值 > 屏幕跨度 || 第二值 > 屏幕长度 || 已请求宽度值 > 屏幕跨度 - 首位值 || 已请求高度值 > 屏幕长度 - 第二值) return -22;
        for (uintptr_t Y_按钮坐标 = 第二值; Y_按钮坐标 < 第二值 + 已请求高度值; Y_按钮坐标++) for (uintptr_t 横坐标坐标 = 首位值; 横坐标坐标 < 首位值 + 已请求宽度值; 横坐标坐标++) 板像素(横坐标坐标, Y_按钮坐标, 字符代码);
        return 0;
    }
    case 14: return (int32_t)板取字符();
    case 15: // args(-1,0,0)=项目个数; args(index,buffer,capacity)=UTF-8 长度
        if (首位值 == UINTPTR_MAX) return 已转发参数个数;
        if (首位值 >= 已转发参数个数) return -22;
        if (字符代码 <= 已转发参数长度[首位值]) return -36;
        if (!用户范围(第二值, 已转发参数长度[首位值] + 1, 1)) return -14;
        memcpy((void *)第二值, 已转发参数[首位值], 已转发参数长度[首位值] + 1);
        return 已转发参数长度[首位值];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(首位值==0){if(!Java交互壳交互式())return -95;交互式=1;return 板终端(13);}
        if(首位值==2){交互式=0;return 0;}
        if(首位值==3)return 板终端(13);
        if(首位值!=1||!交互式)return -22;
        结果=(int32_t)板取字符();
        if(结果==-4096)return 结果;
        开始超时();return 结果<0?-11:结果;
    case 17: { // 유한한 협력 等待状态值: 通信 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (首位值 > 100) return -22;
        uint64_t 结束时间 = 时钟值() + 频率 * 首位值 / 1000;
        do { 审查网络(); 审查文件传送(); __asm__ volatile("yield"); } while (时钟值() < 结束时间);
        开始超时(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 父值·빈 폴더를 검사한다.
        if (第二值 > 2) return -22;
        结果 = 复制路径(首位值, 路径); if (结果) return 结果;
        unsigned 长度 = 0; while (路径[长度]) 长度++;
        结果 = Java路径开始(长度); if (结果 < 0) return 结果;
        for (unsigned 序数索引 = 0; 序数索引 < 长度; 序数索引++) Java路径字节(序数索引, (unsigned char)路径[序数索引]);
        return 第二值 == 0 ? Java条目种类() : 第二值 == 1 ? Java创建目录() : Java移除目录();
    }
    case 20:
        if(首位值==5){int 字符值=(int32_t)板取字符();if(字符值==-4096)return 字符值;if(字符值>=0)屏幕按下(所有者对象,字符值);开始超时();}
        if(首位值==3&&字符代码){if(!Java交互壳交互式())return -95;交互式=1;板终端(300);}
        return 调用屏幕(所有者对象,首位值,第二值,字符代码,文件条目->寄存器数据[3],文件条目->寄存器数据[4],文件条目->寄存器数据[5]);
    case 21:
        if(字符代码>127)return -22;if(!用户范围(第二值,字符代码*sizeof(uint32_t),0))return -14;
        return 屏幕文本(所有者对象,首位值,(const uint32_t *)第二值,字符代码);
    case 22: // 屏幕 大小 查询值: 0=宽度值, 1=高度值. 사용자에게 주소를 노출하지 않는다.
        if (首位值 > 1) return -22;
        if (!板帧缓冲()) return -19;
        return 首位值 == 0 ? 板屏幕宽度() : 板屏幕高度();
    case 32:
        if (首位值 != AF_INET) return -97;
        if(第二值==SOCK_STREAM&&(字符代码==0||字符代码==6))结果=Java流创建();
        else if(第二值==SOCK_DGRAM&&(字符代码==0||字符代码==IPPROTO_UDP))结果=Java网络套接字(首位值,第二值,字符代码);
        else return -93;
        if (结果 >= 32 && 结果 < 56) 套接字端点列[结果 - 32] = 1;
        return 结果;
    case 33: {
        if (!套接字端点所有者(首位值)) return -9;
        struct pk_sockaddr_in 地址;
        结果 = 地址输入(第二值, 字符代码, &地址); if (结果) return 结果;
        return 首位值>=40?Java流绑定(首位值,pk_htonl(地址.sin_addr.s_addr),pk_htons(地址.sin_port)):Java网络绑定(首位值, pk_htonl(地址.sin_addr.s_addr), pk_htons(地址.sin_port));
    }
    case 34: {
        if (!套接字端点所有者(首位值)) return -9;
        if(首位值>=40)return -95;
        if (文件条目->寄存器数据[3]) return -95;
        if (字符代码 > 512) return -90;
        if (字符代码 && !用户范围(第二值, 字符代码, 0)) return -14;
        struct pk_sockaddr_in 地址;
        结果 = 地址输入(文件条目->寄存器数据[4], 文件条目->寄存器数据[5], &地址); if (结果) return 结果;
        for (unsigned 序数索引 = 0; 序数索引 < 字符代码; 序数索引++) Java网络放入(序数索引, ((const unsigned char *)第二值)[序数索引]);
        return Java网络发送(首位值, pk_htonl(地址.sin_addr.s_addr), pk_htons(地址.sin_port), 字符代码);
    }
    case 35: {
        if (!套接字端点所有者(首位值)) return -9;
        if(首位值>=40)return -95;
        if (文件条目->寄存器数据[3]) return -95;
        if (字符代码 > 512) return -90;
        if (字符代码 && !用户范围(第二值, 字符代码, 1)) return -14;
        pk_socklen_t 缓冲容量 = 0;
        if (文件条目->寄存器数据[4]) { 结果 = 地址输出检查(文件条目->寄存器数据[4], 文件条目->寄存器数据[5], &缓冲容量); if (结果) return 结果; }
        结果 = Java网络接收操作(首位值, 字符代码); if (结果 < 0) return 结果;
        for (int 序数索引 = 0; 序数索引 < 结果; 序数索引++) ((unsigned char *)第二值)[序数索引] = Java网络获取(序数索引);
        if (文件条目->寄存器数据[4]) 地址输出(文件条目->寄存器数据[4], 文件条目->寄存器数据[5], 缓冲容量, Java网络远程(首位值), Java网络对端(首位值));
        return 结果;
    }
    case 36: {
        if (!套接字端点所有者(首位值)) return -9;
        pk_socklen_t 缓冲容量;
        结果 = 地址输出检查(第二值, 字符代码, &缓冲容量); if (结果) return 结果;
        地址输出(第二值,字符代码,缓冲容量,首位值>=40?Java流地址(首位值):Java网络地址(首位值),首位值>=40?Java流端口(首位值):Java网络端口(首位值)); return 0;
    }
    case 37: {
        if(首位值<40||!套接字端点所有者(首位值))return -9;struct pk_sockaddr_in 地址;
        结果=地址输入(第二值,字符代码,&地址);if(结果)return 结果;
        return Java流连接(首位值,pk_htonl(地址.sin_addr.s_addr),pk_htons(地址.sin_port));
    }
    case 38: return 首位值>=40&&套接字端点所有者(首位值)?Java流侦听(首位值,第二值):-9;
    case 39:
        if(首位值<40||!套接字端点所有者(首位值))return -9;
        if(第二值||字符代码)return -95;结果=Java流接受(首位值);if(结果>=40&&结果<56)套接字端点列[结果-32]=1;return 结果;
    case 40: return 首位值>=40&&套接字端点所有者(首位值)?Java流对端(首位值):-9;
    default: return -38; // 是否不支持 기능을 성공으로 가장하지 않음
    }
}
#include "Linux兼容性.inc"
static intptr_t 系统调用(用户帧 *文件条目) {
    network_poll();
    return Linux调用约定 ? Linux系统调用(文件条目) : 原生系统调用(文件条目);
}
static void 发回内核(用户帧 *文件条目, int 结果) {
    停止超时();
    文件条目->寄存器数据[0] = (uint64_t)(int64_t)结果;
    文件条目->命令位置 = (uintptr_t)用户发回;
    文件条目->状态代码 = 0x3c5; // EL1h, DAIF masked
}
int 用户异常(用户帧 *文件条目, unsigned 拦截) {
    if (!活跃 || (文件条目->状态代码 & 15) != 0) return 0;
    if (拦截) {
        uint32_t 确认应答值 = 计算机寄存器(中断CPU接口 + 0xc), 标识符值 = 确认应答值 & 1023;
        if (标识符值 == 30) { 发回内核(文件条目, 用户超时); 计算机寄存器(中断CPU接口 + 0x10) = 确认应答值; return 1; }
        if (标识符值 < 1020) 计算机寄存器(中断CPU接口 + 0x10) = 确认应答值;
        return 1;
    }
    uint64_t 异常状态; __asm__ volatile("mrs %0, esr_el1" : "=r"(异常状态));
    if (时钟值() >= 截止时间时间) { 发回内核(文件条目, 用户超时); return 1; }
    unsigned 异常分类 = 异常状态 >> 26;
    if (异常分类 == 0x15 && (异常状态 & 0xffff) == 0) {
        if (Linux调用约定 ? 文件条目->寄存器数据[8] == 93 || 文件条目->寄存器数据[8] == 94 : 文件条目->寄存器数据[8] == 6) 发回内核(文件条目, (int)(文件条目->寄存器数据[0] & 255));
        else {
            intptr_t 结果=系统调用(文件条目);
            if(结果==-4096&&交互式){
                已保存[所有者对象].执行状态帧=*文件条目;已保存[所有者对象].执行状态帧.命令位置-=4;
                用户浮点保存(已保存[所有者对象].浮点型分状态);发回内核(文件条目,用户已中断);
            }else 文件条目->寄存器数据[0]=(uint64_t)结果;
        }
    } else 发回内核(文件条目, 异常分类 == 0x24 ? 用户数据错误 : 异常分类 == 0x20 ? 用户执行状态错误 : 用户无效指令);
    return 1;
}

// 생성된 const ELF 组值: 실행은 반드시 程序 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *数据; size_t 大小; unsigned 已转发值; } 执行条目;
#include "programs.h"
static void *快照(unsigned 位置索引){return (void *)(0x04000000ul+位置索引*(用户结束-用户基底));}
static int 结束操作程序(int 结果){
    用户累积时间[所有者对象]+=(uint32_t)板经过毫秒()-用户执行状态时间[所有者对象];
    停止超时();活跃=0;
    if(结果==用户已中断){
        已保存进程 *字符串数据=&已保存[所有者对象];字符串数据->已暂停状态=1;字符串数据->交互式=交互式;字符串数据->Linux调用约定=Linux调用约定;字符串数据->堆存储装置=堆结束;字符串数据->参数列个数=已转发参数个数;
        memcpy(字符串数据->权限列列表,权限列列表,sizeof(权限列列表));memcpy(字符串数据->文件列表,文件列表,sizeof(文件列表));memcpy(字符串数据->套接字端点列,套接字端点列,sizeof(套接字端点列));
        memcpy(字符串数据->参数数组,已转发参数,sizeof(已转发参数));memcpy(字符串数据->参数长度,已转发参数长度,sizeof(已转发参数长度));
        for(unsigned 序数索引=0;序数索引<用户页个数;序数索引++)if(权限列列表[序数索引])memcpy((unsigned char *)快照(所有者对象)+序数索引*页大小,(void *)(用户基底+序数索引*页大小),页大小);
    }else{
        已保存[所有者对象].已暂停状态=0;初始化屏幕(所有者对象);
        for(unsigned 序数索引=0;序数索引<16;序数索引++)if(文件列表[序数索引]>=0)pk_close(文件列表[序数索引]);
        for(unsigned 序数索引=0;序数索引<24;序数索引++)if(套接字端点列[序数索引])关闭套接字端点(序数索引+32);
    }
    for(unsigned 序数索引=0;序数索引<用户页个数;序数索引++){页列表[序数索引]=0;权限列列表[序数索引]=0;}同步表列();return 结果;
}
uintptr_t 板用户控制(uintptr_t 动作){
    unsigned 位置索引=动作&15;if(位置索引>=4||活跃)return (uint32_t)-22;
    已保存进程 *字符串数据=&已保存[位置索引];
    if(动作>=32){if(字符串数据->已暂停状态){for(unsigned 序数索引=0;序数索引<16;序数索引++)if(字符串数据->文件列表[序数索引]>=0)pk_close(字符串数据->文件列表[序数索引]);for(unsigned 序数索引=0;序数索引<24;序数索引++)if(字符串数据->套接字端点列[序数索引])关闭套接字端点(序数索引+32);}字符串数据->已暂停状态=0;初始化屏幕(位置索引);return 0;}
    if(动作>=16)return 字符串数据->已暂停状态;
    if(!字符串数据->已暂停状态)return (uint32_t)-22;
    所有者对象=位置索引;交互式=字符串数据->交互式;Linux调用约定=字符串数据->Linux调用约定;堆结束=字符串数据->堆存储装置;已转发参数个数=字符串数据->参数列个数;
    memcpy(文件列表,字符串数据->文件列表,sizeof(文件列表));memcpy(套接字端点列,字符串数据->套接字端点列,sizeof(套接字端点列));memcpy(已转发参数,字符串数据->参数数组,sizeof(已转发参数));memcpy(已转发参数长度,字符串数据->参数长度,sizeof(已转发参数长度));
    for(unsigned 序数索引=0;序数索引<用户页个数;序数索引++)页列表[序数索引]=(用户基底+序数索引*页大小)|内核页;同步表列();
    memset((void *)用户基底,0,用户结束-用户基底);
    for(unsigned 序数索引=0;序数索引<用户页个数;序数索引++)if(字符串数据->权限列列表[序数索引])memcpy((void *)(用户基底+序数索引*页大小),(unsigned char *)快照(位置索引)+序数索引*页大小,页大小);
    memcpy(权限列列表,字符串数据->权限列列表,sizeof(权限列列表));
    for(unsigned 序数索引=0;序数索引<用户页个数;序数索引++){unsigned 数据位置=权限列列表[序数索引];页列表[序数索引]=数据位置?(用户基底+序数索引*页大小)|(数据位置==3?用户读取写入:数据位置==5?用户读取执行:用户读取仅用):0;}
    同步表列();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");活跃=1;字符串数据->已暂停状态=0;开始超时();
    用户执行状态时间[所有者对象]=板经过毫秒();
    return (uint32_t)结束操作程序(用户恢复执行(&字符串数据->执行状态帧,字符串数据->浮点型分状态));
}
static int 运行程序(const unsigned char *数据, size_t 大小, unsigned 已转发值, int Linux模式, const char *名称) {
    if (活跃) return -16;
    所有者对象=板终端(11);if(所有者对象<0||所有者对象>3||已保存[所有者对象].已暂停状态)return -16;交互式=0;
    int 有效 = 有效性校验ELF(数据, 大小, Linux模式); if (有效) return 有效;
    Linux调用约定 = Linux模式;
    unsigned 名称索引=0;
    while (*名称 && 名称索引<31) 用户命令名称[所有者对象][名称索引++]=(unsigned char)*名称++;
    if (已转发参数个数 && 已转发参数长度[0]) {
        if (名称索引) 用户命令名称[所有者对象][名称索引++]=' ';
        for (unsigned 位置索引=0; 位置索引<已转发参数长度[0]; 位置索引++) 用户命令名称[所有者对象][名称索引++]=已转发参数[0][位置索引];
    }
    用户命令名称[所有者对象][名称索引]=0; 用户编号[所有者对象]=下一用户编号++;
    if (下一用户编号>0x7fffffffu) 下一用户编号=10;
    用户开始时间[所有者对象]=板经过毫秒(); 用户累积时间[所有者对象]=0;
    for (unsigned 序数索引 = 0; 序数索引 < 用户页个数; 序数索引++) 页列表[序数索引] = (用户基底 + 序数索引 * 页大小) | 内核页;
    同步表列();
    memset((void *)用户基底, 0, 用户结束 - 用户基底);
    memset(权限列列表, 0, sizeof(权限列列表));
    ELF头部 可执行文件头部; memcpy(&可执行文件头部, 数据, sizeof(可执行文件头部));
    for (unsigned 序数索引 = 0; 序数索引 < 可执行文件头部.程序头部个数; 序数索引++) {
        ELF程序 数据位置; memcpy(&数据位置, 数据 + 可执行文件头部.程序头部偏移 + 序数索引 * sizeof(数据位置), sizeof(数据位置));
        if (数据位置.类型分类 != 1 || !数据位置.内存区大小) continue;
        if (数据位置.文件区域大小) memcpy((void *)(uintptr_t)数据位置.地址, 数据 + 数据位置.偏移值, 数据位置.文件区域大小);
        for (uintptr_t 当前位置 = 数据位置.地址 & ~(页大小 - 1); 当前位置 < 数据位置.地址 + 数据位置.内存区大小; 当前位置 += 页大小) {
            权限列列表[(当前位置 - 用户基底) / 页大小] = (数据位置.配置项位列 & 2) ? 3 : ((数据位置.配置项位列 & 1) ? 5 : 1);
        }
    }
    for (uintptr_t 当前位置 = 用户栈地址; 当前位置 < 用户结束; 当前位置 += 页大小) 权限列列表[(当前位置 - 用户基底) / 页大小] = 3;
    uintptr_t 初始栈 = Linux模式 ? Linux开始栈(可执行文件头部.条目分) : 用户结束;
    for (unsigned 序数索引 = 0; 序数索引 < 用户页个数; 序数索引++) {
        unsigned 存取权限列 = 权限列列表[序数索引];
        页列表[序数索引] = 存取权限列 ? (用户基底 + 序数索引 * 页大小) | (存取权限列 == 3 ? 用户读取写入 : 存取权限列 == 5 ? 用户读取执行 : 用户读取仅用) : 0;
    }
    同步表列();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned 序数索引 = 0; 序数索引 < 16; 序数索引++) 文件列表[序数索引] = -1;
    memset(套接字端点列, 0, sizeof(套接字端点列));
    堆结束 = 用户映像结束;
    活跃 = 1; 开始超时();
    用户执行状态时间[所有者对象]=板经过毫秒();
    int 结果 = 用户进入(可执行文件头部.条目分, 初始栈, 已转发值);
    return 结束操作程序(结果);
}
uintptr_t 板用户运行(uintptr_t 查找索引) {
    if (查找索引 >= sizeof(可执行文件条目列) / sizeof(可执行文件条目列[0])) return (uint32_t)-22;
    const char *名称=查找索引==10?"javac":查找索引==11?"java":查找索引==12?"python":查找索引==13?"vi":查找索引==14?"jar":查找索引==15?"cc":查找索引==16?"jaot":"ELF";
    return (uint32_t)运行程序(可执行文件条目列[查找索引].数据, 可执行文件条目列[查找索引].大小, 可执行文件条目列[查找索引].已转发值, 0, 名称);
}
static uintptr_t 执行文件(int Linux模式) {
    static unsigned char 映像[16384];
    if (活跃 || !已转发参数个数) return (uint32_t)-22;
    int 文件句柄 = pk_open((const char *)已转发参数[0], 读取仅用值, 0);
    if (文件句柄 < 0) return (uint32_t)-错误编号;
    int 大小 = pk_size(文件句柄);
    if (大小 < 0 || (unsigned)大小 > sizeof(映像)) { pk_close(文件句柄); return (uint32_t)-27; }
    int 已接收个数 = pk_read(文件句柄, 映像, 大小); pk_close(文件句柄);
    if (已接收个数 != 大小) return (uint32_t)-5;
    return (uint32_t)运行程序(映像, 大小, 0, Linux模式, "");
}
uintptr_t 板用户文件(void) { return 执行文件(0); }
uintptr_t 板用户Linux文件(void) { return 执行文件(1); }
uintptr_t 板用户有效性校验(void) {
    for (unsigned 序数索引 = 0; 序数索引 < sizeof(无效可执行项列) / sizeof(无效可执行项列[0]); 序数索引++)
        if (用户有效性校验ELF(无效可执行项列[序数索引].数据, 无效可执行项列[序数索引].大小) != 用户可执行文件错误) return 序数索引 + 1;
    return 0;
}
