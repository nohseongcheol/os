#ifndef 原生捆綁標頭
#define 原生捆綁標頭
#include <stddef.h>
int JAR打開(const char *檔案條目名稱);
int JAR讀取(const char *名稱, unsigned char *結果資料, unsigned 緩衝區容量);
const char *JAR主操作(void);
#endif
