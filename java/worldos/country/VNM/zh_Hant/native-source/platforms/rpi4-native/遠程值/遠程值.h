#ifndef 原生遠程連接狀態標頭
#define 原生遠程連接狀態標頭
#include "../命名/計算機連接名稱列.h"
#include <stdint.h>
void 準備遠程(void);
void 審查遠程(void);
void 遠程輸出(unsigned char);
int 遠程輸入(void);
int 供給遠程輸入(const unsigned char *,unsigned);
uintptr_t 板遠程控制(uintptr_t,uintptr_t);
uintptr_t 板結束遠程命令(uintptr_t);
uintptr_t 板遠程等待狀態(uintptr_t);
void 審查遠程顯示操作(void);
int 控制遠程顯示操作(unsigned);
#endif
