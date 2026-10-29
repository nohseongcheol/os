#ifndef 原生用户头部
#define 原生用户头部
#include <stdint.h>
#include <stddef.h>
#define 用户基底 0x02000000ul
#define 用户映像结束 0x02c00000ul
#define 用户堆结束 0x02ed0000ul
#define 用户栈地址 0x02f00000ul
#define 用户结束 0x03000000ul
#define 用户页个数 ((用户结束 - 用户基底) / 4096ul)
#define 用户可执行文件错误 (-8)
#define 用户数据错误 (-1001)
#define 用户执行状态错误 (-1002)
#define 用户无效指令 (-1003)
#define 用户超时 (-1004)
#define 用户已中断 (-1005)
typedef struct { uint64_t 寄存器数据[31], 命令位置, 状态代码, 栈地址; } 用户帧;
void 用户系统初始化操作(void);
int 用户异常(用户帧 *, unsigned);
int 用户有效性校验ELF(const unsigned char *, size_t);
uintptr_t 板用户运行(uintptr_t);
uintptr_t 板用户有效性校验(void);
uintptr_t 板用户控制(uintptr_t);
uint32_t 读取用户状态(unsigned, unsigned);
#endif
