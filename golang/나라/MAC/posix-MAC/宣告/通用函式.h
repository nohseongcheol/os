#ifndef _宣告_通用函式
#define _宣告_通用函式
#include <基本定義.h>
typedef struct { int 商值; int 餘數; } 整數除法結果型別;
typedef struct { long 商值; long 餘數; } 長整數除法結果型別;
#define 成功結束 0
#define 失敗結束 1
void *配置記憶空間(大小型別 大小);
void *配置清零陣列空間(大小型別 數量, 大小型別 元素大小);
void *調整記憶空間大小(void *位址, 大小型別 大小);
void 釋放記憶空間(void *位址);
long 將字串讀為長整數(const char *字串, char **轉換末端位址, int 基數);
unsigned long 將字串讀為無號長整數(const char *字串, char **轉換末端位址, int 基數);
int 將十進字串讀為整數(const char *字串);
long 將十進字串讀為長整數(const char *字串);
int 取得整數絕對值(int 值);
long 取得長整數絕對值(long 值);
整數除法結果型別 取得整數商餘數(int 左值, int 右值);
長整數除法結果型別 取得長整數商餘數(long 左值, long 右值);
void 依比較規則排序(void *元素陣列, 大小型別 數量, 大小型別 元素大小,
           int (*比較函式)(const void *, const void *));
void *在有序陣列中二分搜尋(const void *來源位置, const void *元素陣列, 大小型別 數量,
              大小型別 元素大小, int (*比較函式)(const void *, const void *));
char *取得環境變數值(const char *系統資料);
#endif
