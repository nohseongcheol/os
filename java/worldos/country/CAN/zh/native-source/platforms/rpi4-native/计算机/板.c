#include "../命名/计算机连接名称列.h"
#include "屏幕信息.h"
#include <stdint.h>
#include <stddef.h>
#include "用户.h"
#include "../通信网络/通信网络.h"
typedef uintptr_t 计算机机器字;
#define 计算机寄存器(首位值) (*(volatile uint32_t *)(uintptr_t)(首位值))
#define 串行设备 0xfe201000u
#define 通用型用途输入输出 0xfe200000u
#define 邮箱地址 0xfe00b880u
static inline void 内存屏障(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t 时钟个数(void) { uint64_t 临时数据; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(临时数据)); return 临时数据; }
static uint64_t 频率;
static volatile uint32_t 邮箱数据[64] __attribute__((aligned(16)));
static unsigned 屏幕就绪;
static uint32_t ARM内存千二进制字节单位;

void *memset(void *数据位置, int 字符代码, size_t 项目个数) { unsigned char *下一偏移 = 数据位置; while (项目个数--) *下一偏移++ = 字符代码; return 数据位置; }
void *memcpy(void *目的地址数据, const void *字符串数据, size_t 项目个数) { unsigned char *首位值 = 目的地址数据; const unsigned char *第二值 = 字符串数据; while (项目个数--) *首位值++ = *第二值++; return 目的地址数据; }

static int 邮箱(void) {
    uint32_t 申请 = (uint32_t)(uintptr_t)邮箱数据 | 8;
    uint64_t 运行 = 时钟个数();
    内存屏障();
    while (计算机寄存器(邮箱地址 + 0x38) & 0x80000000u)
        if (时钟个数() - 运行 > 频率) return 0;
    计算机寄存器(邮箱地址 + 0x20) = 申请;
    for (;;) {
        if (!(计算机寄存器(邮箱地址 + 0x18) & 0x40000000u)) {
            uint32_t 回复 = 计算机寄存器(邮箱地址);
            if (回复 == 申请) { 内存屏障(); return 邮箱数据[1] == 0x80000000u; }
        }
        if (时钟个数() - 运行 > 频率) return 0;
    }
}

extern int32_t Java交互壳输出(int32_t, int32_t), Java交互壳输入(void);
extern void 终端字节(unsigned);
extern int 终端待处理(void);
extern void 终端指针(unsigned,int,int),终端热键(unsigned);
extern void 终端输入模式(unsigned);
#include "../远程值/远程值.h"
static int 数据流集;
static unsigned UART上一个;
计算机机器字 板数据流集(计算机机器字 是否已使用) { 数据流集=是否已使用!=0; return 0; }
计算机机器字 板信道(计算机机器字 信道, 计算机机器字 字符代码) {
    if(数据流集 && Java交互壳输出((int32_t)信道,(int32_t)(字符代码&255))) return 0;
    终端字节(字符代码&255);
    远程输出(字符代码&255);
    if ((字符代码&255)==10 && UART上一个!=13) {
        while (计算机寄存器(串行设备 + 0x18) & 0x20) __asm__ volatile("yield");
        计算机寄存器(串行设备)=13;
    }
    UART上一个=字符代码&255;
    while (计算机寄存器(串行设备 + 0x18) & 0x20) __asm__ volatile("yield");
    计算机寄存器(串行设备) = (uint32_t)字符代码 & 255;
    return 0;
}
计算机机器字 板写字符(计算机机器字 字符代码) { return 板信道(1,字符代码); }
计算机机器字 板原始数据取字符(void) {
    int 远程字符=远程输入();if(远程字符>=0)return 远程字符;
    if (计算机寄存器(串行设备 + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t 值 = 计算机寄存器(串行设备);
    if (值 & 0xf00) { 计算机寄存器(串行设备 + 4) = 0; return (uint32_t)-1; }
    return 值 & 255;
}
计算机机器字 板取字符(void) {
    network_poll();
    static unsigned 输入侧数据包,已使用容量; static unsigned char 数据包数据[6];
    if(终端待处理())return (uint32_t)-4096;
    if(数据流集){int32_t 字符代码=Java交互壳输入();if(字符代码!=-3)return (uint32_t)字符代码;}
    for(;;){
        int 字符代码=(int32_t)板原始数据取字符();if(字符代码<0)return (uint32_t)字符代码;
        if(!输入侧数据包){if(字符代码!=30)return 字符代码;输入侧数据包=1;已使用容量=0;continue;}
        数据包数据[已使用容量++]=字符代码;if(已使用容量<6)continue;输入侧数据包=0;
        if(数据包数据[0]==1)终端指针(数据包数据[1],数据包数据[2]+数据包数据[3]*256,数据包数据[4]+数据包数据[5]*256);
        if(数据包数据[0]==2)终端热键(数据包数据[1]);
        if(数据包数据[0]==3)终端输入模式(数据包数据[1]);
        if(终端待处理())return (uint32_t)-4096;
    }
}
计算机机器字 板经过毫秒(void) { return (uint32_t)(时钟个数() / (频率 / 1000)); }
计算机机器字 板当前异常级别(void) { uint64_t 临时数据; __asm__ volatile("mrs %0, CurrentEL" : "=r"(临时数据)); return 临时数据 >> 2; }
static void 输出行UART(const char *字符串数据) { while (*字符串数据) 板写字符((unsigned char)*字符串数据++); }
static void 十六进制UART(计算机机器字 项目个数) { const char *十六进制数位数 = "0123456789abcdef"; for (int 字符串数据 = 60; 字符串数据 >= 0; 字符串数据 -= 4) 板写字符(十六进制数位数[(项目个数 >> 字符串数据) & 15]); }
计算机机器字 板停止(计算机机器字 状态值) {
    输出行UART("\r\nHALTED "); 十六进制UART(状态值); 输出行UART("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void 内核致命停止(const char *原因值) __attribute__((noreturn));
void 内核致命停止(const char *原因值) { 输出行UART("\r\nPANIC: "); 输出行UART(原因值); 板停止(1); __builtin_unreachable(); }
void 板异常(计算机机器字 异常状态, 计算机机器字 命令位置, 计算机机器字 无效地址) {
    输出行UART("\r\nEXCEPTION ESR="); 十六进制UART(异常状态);
    输出行UART(" PC="); 十六进制UART(命令位置); 输出行UART(" FAR="); 十六进制UART(无效地址);
    板停止(2);
}
int 板物理硬件(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    邮箱数据[0]=32;邮箱数据[1]=0;邮箱数据[2]=0x10004;邮箱数据[3]=8;邮箱数据[4]=0;
    邮箱数据[5]=邮箱数据[6]=邮箱数据[7]=0;
    return 邮箱()&&邮箱数据[4]==0x80000008u&&(邮箱数据[5]||邮箱数据[6]);
}
int 板计算机地址(unsigned char *地址) {
    邮箱数据[0]=32;邮箱数据[1]=0;邮箱数据[2]=0x10003;邮箱数据[3]=8;邮箱数据[4]=0;
    邮箱数据[5]=邮箱数据[6]=邮箱数据[7]=0;
    if(!邮箱()||(邮箱数据[4]&0x80000000u)==0||(邮箱数据[4]&0xffff)!=6)return 0;
    const unsigned char *数据=(const unsigned char*)&邮箱数据[5];unsigned 总和值=0;
    for(unsigned 序数索引=0;序数索引<6;序数索引++){地址[序数索引]=数据[序数索引];总和值|=数据[序数索引];}return 总和值&&!(地址[0]&1);
}
void 板初始化操作(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(频率));
    计算机寄存器(串行设备 + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    计算机寄存器(通用型用途输入输出 + 4) = (计算机寄存器(通用型用途输入输出 + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    计算机寄存器(通用型用途输入输出 + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. 失败值 시 config.txt의 48MHz를 사용한다.
    邮箱数据[0] = 36; 邮箱数据[1] = 0; 邮箱数据[2] = 0x38002; 邮箱数据[3] = 12;
    邮箱数据[4] = 0; 邮箱数据[5] = 2; 邮箱数据[6] = 48000000; 邮箱数据[7] = 0; 邮箱数据[8] = 0;
    int 时钟正常 = 邮箱();
    uint32_t 速度值 = 时钟正常 && 邮箱数据[6] >= 1843200 ? 邮箱数据[6] : 48000000;
    邮箱数据[0]=32; 邮箱数据[1]=0; 邮箱数据[2]=0x10005; 邮箱数据[3]=8; 邮箱数据[4]=0;
    邮箱数据[5]=邮箱数据[6]=邮箱数据[7]=0;
    if (邮箱() && 邮箱数据[4]==0x80000008u) ARM内存千二进制字节单位=邮箱数据[6]/1024;
    uint32_t 除数64 = (uint32_t)(((uint64_t)速度值 * 4 + 57600) / 115200);
    计算机寄存器(串行设备 + 0x44) = 0x7ff;
    计算机寄存器(串行设备 + 0x24) = 除数64 / 64;
    计算机寄存器(串行设备 + 0x28) = 除数64 % 64;
    计算机寄存器(串行设备 + 0x2c) = (3u << 5) | (1u << 4);
    计算机寄存器(串行设备 + 0x38) = 0;
    计算机寄存器(串行设备 + 0x30) = 0x301;
    内存屏障();
    输出行UART("JKOROS AARCH64 BARE METAL\r\n");
    用户系统初始化操作();
    network_init();
}
计算机机器字 板FTP(计算机机器字 动作) { return (uint32_t)ftp_control((int)动作); }
计算机机器字 板网络运行状态(计算机机器字 条目值, 计算机机器字 编号) { return 读取网络运行状态(条目值, 编号); }
计算机机器字 板网络设置(计算机机器字 动作, 计算机机器字 地址, 计算机机器字 掩码值, 计算机机器字 网关值) { return (uint32_t)设定配置网络(动作, 地址, 掩码值, 网关值); }
计算机机器字 板发送响应(计算机机器字 地址, 计算机机器字 排序值) { return (uint32_t)开始响应测试(地址, 排序值); }
计算机机器字 板读取响应(计算机机器字 条目值) { return (uint32_t)读取响应测试(条目值); }
计算机机器字 板电源关闭侧(void) {
    ftp_control(0);
    for (unsigned 编号=0; 编号<32; 编号++) 关闭网络(编号);
    for (unsigned 编号=0; 编号<4; 编号++) 板用户控制(32+编号);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    输出行UART("\r\nPOWER OFF\r\n");
    while (计算机寄存器(串行设备+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    计算机寄存器(0xfe100020ul)=0x5a000000u | (计算机寄存器(0xfe100020ul)&~0xfffu) | 0x555;
    计算机寄存器(0xfe100024ul)=0x5a000000u | 10;
    计算机寄存器(0xfe10001cul)=0x5a000000u | (计算机寄存器(0xfe10001cul)&~0x30u) | 0x20;
    内存屏障();
    for (;;) __asm__ volatile("wfe");
}

计算机机器字 板帧缓冲(void) {
    if (屏幕就绪) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 当前项目 크기를 읽는다. */
    const uint32_t 查询值[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t 已请求宽度 = 640, 已请求高度 = 480;
    for (size_t 序数索引 = 0; 序数索引 < sizeof(查询值)/4; 序数索引++) 邮箱数据[序数索引] = 查询值[序数索引];
    if (邮箱() && 邮箱数据[4] == 0x80000008u &&
        邮箱数据[5] >= 640 && 邮箱数据[5] <= 1920 &&
        邮箱数据[6] >= 480 && 邮箱数据[6] <= 1080) {
        已请求宽度 = 邮箱数据[5]; 已请求高度 = 邮箱数据[6];
    }
    const uint32_t 申请[] = {
        35 * 4, 0,
        0x48003, 8, 0, 已请求宽度, 已请求高度,
        0x48004, 8, 0, 已请求宽度, 已请求高度,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t 序数索引 = 0; 序数索引 < sizeof(申请)/4; 序数索引++) 邮箱数据[序数索引] = 申请[序数索引];
    // 顶端值 메시지의 实际数据 길이를 使用值: 태그 追加条目 시 长度 불일치를 방지한다.
    邮箱数据[0] = sizeof(申请);
    if (!邮箱()) return 0;
    const unsigned 响应列[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned 响应长度[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned 序数索引 = 0; 序数索引 < sizeof(响应列)/sizeof(响应列[0]); 序数索引++)
        if (邮箱数据[响应列[序数索引]] != (0x80000000u | 响应长度[序数索引])) return 0;
    uint32_t 背景值 = 邮箱数据[28] & 0x3fffffffu;
    uint32_t 大小 = 邮箱数据[29];
    uint32_t 已接收宽度 = 邮箱数据[5], 已接收高度 = 邮箱数据[6], 已接收行间距 = 邮箱数据[33];
    if (邮箱数据[15] != 32 || 邮箱数据[19] != 1 ||
        已接收宽度 < 640 || 已接收宽度 > 1920 || 已接收高度 < 480 || 已接收高度 > 1080 ||
        邮箱数据[10] < 已接收宽度 || 邮箱数据[11] < 已接收高度 || 邮箱数据[23] || 邮箱数据[24] ||
        !背景值 || 背景值 < 0x1000000 || (背景值 & 3) || 已接收行间距 < 已接收宽度 * 4 || (已接收行间距 & 3) ||
        (uint64_t)已接收行间距 * 已接收高度 > 大小 || (uint64_t)背景值 + 大小 > 0x40000000u)
        return 0;
    板准备绘图((volatile uint32_t *)(uintptr_t)背景值, 已接收宽度, 已接收高度, 已接收行间距);
    屏幕就绪 = 1;
    return 1;
}

// 단일 코어의 협력식 线程值. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t 已保存[13]; } 上下文;
static 上下文 上下文列[3];
static unsigned char 栈集[2][65536] __attribute__((aligned(16)));
static int 是否运行中[3] = {1, 0, 0};
static int 当前任务;
extern void 上下文切换(上下文 *, 上下文 *);
extern void Java任务(int32_t);
计算机机器字 板挂起(void) {
    network_poll();
    int 上一个项目 = 当前任务, 下一项目 = (上一个项目 + 1) % 3;
    while (下一项目 != 上一个项目 && !是否运行中[下一项目]) 下一项目 = (下一项目 + 1) % 3;
    if (下一项目 != 上一个项目) {
        for (unsigned 序数索引 = 0; 序数索引 < 2; 序数索引++)
            if (是否运行中[序数索引 + 1] && *(uint64_t *)栈集[序数索引] != 0x6b6f726f7373746bull)
                内核致命停止("task stack guard");
        当前任务 = 下一项目;
        上下文切换(&上下文列[上一个项目], &上下文列[下一项目]);
    }
    return 0;
}
static void 任务引导(void) {
    Java任务(当前任务);
    是否运行中[当前任务] = 0;
    板挂起();
    内核致命停止("finished task resumed");
}
计算机机器字 板任务创建(计算机机器字 标识符值) {
    if (标识符值 < 1 || 标识符值 > 2 || 是否运行中[标识符值]) return (uint32_t)-1;
    memset(&上下文列[标识符值], 0, sizeof(上下文));
    *(uint64_t *)栈集[标识符值 - 1] = 0x6b6f726f7373746bull;
    上下文列[标识符值].已保存[11] = (uintptr_t)任务引导;
    上下文列[标识符值].已保存[12] = (uintptr_t)(栈集[标识符值 - 1] + sizeof(栈集[0]));
    是否运行中[标识符值] = 1;
    return 0;
}
计算机机器字 板任务状态(计算机机器字 标识符值) { return 标识符值 < 3 ? 是否运行中[标识符值] : (uint32_t)-1; }
extern 计算机机器字 提前编译内存查找(计算机机器字);
extern uint32_t 读取用户状态(unsigned, unsigned);
extern unsigned char 栈顶端[];
计算机机器字 板查询系统(计算机机器字 条目值, 计算机机器字 编号) {
    if (条目值==0) return ARM内存千二进制字节单位;
    if (条目值==1) return ((uintptr_t)栈顶端-0x80000+1023)/1024;
    if (条目值==2 || 条目值==3) return 提前编译内存查找(条目值==3);
    if (条目值==4) return 屏幕就绪 ? (板屏幕宽度()*板屏幕高度()*4+1023)/1024 : 0;
    if (条目值==5) return 80*1024; /* 执行命令 地址区域 16 MiB + 네 세션 保留值 地址区域. */
    if (条目值>=20) return 读取用户状态(条目值-20, 编号);
    return 0;
}
int *pk_errno_location(void) { static int 错误列[3]; return &错误列[当前任务]; }
