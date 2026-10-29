#ifndef 原生範例標頭
#define 原生範例標頭
#include <檔案ABI.h>
#include <屏幕ABI.h>
static int 文本長度(const char *文本) { int 長度=0;while(文本[長度])長度++;return 長度; }
static int 輸出(const char *文本) { int 長度=文本長度(文本);return 寫入檔案資料(1,文本,長度)==長度?0:1; }
#endif
