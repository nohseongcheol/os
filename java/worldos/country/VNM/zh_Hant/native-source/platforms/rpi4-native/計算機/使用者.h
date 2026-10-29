#ifndef 原生用戶標頭
#define 原生用戶標頭
#include <stdint.h>
#include <stddef.h>
#define 用戶基底 0x02000000ul
#define 用戶映像結束 0x02c00000ul
#define 用戶堆結束 0x02ed0000ul
#define 用戶棧地址 0x02f00000ul
#define 用戶結束 0x03000000ul
#define 用戶頁個數 ((用戶結束 - 用戶基底) / 4096ul)
#define 用戶可執行文件錯誤 (-8)
#define 用戶資料錯誤 (-1001)
#define 用戶執行狀態錯誤 (-1002)
#define 用戶無效指令 (-1003)
#define 用戶超時 (-1004)
#define 用戶已中斷 (-1005)
typedef struct { uint64_t 寄存器資料[31], 命令位置, 狀態程式碼, 棧地址; } 用戶幀;
void 用戶系統初始化操作(void);
int 用戶異常(用戶幀 *, unsigned);
int 用戶有效性校驗ELF(const unsigned char *, size_t);
uintptr_t 板用戶運行(uintptr_t);
uintptr_t 板用戶有效性校驗(void);
uintptr_t 板用戶控制(uintptr_t);
uint32_t 讀取用戶狀態(unsigned, unsigned);
#endif
