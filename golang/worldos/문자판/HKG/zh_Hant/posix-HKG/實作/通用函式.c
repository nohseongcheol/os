#include <通用函式.h>
#include <字串與記憶內容.h>
#include <字元分類.h>
#include <錯誤編號.h>
#include <整數極限.h>
#include <輸入輸出與執行.h>

static int 取得數字值(unsigned char 字元值)
{
    if (檢查是否十進數字(字元值)) return 字元值 - '0';
    if (檢查是否字母(字元值)) return 轉換為小寫(字元值) - 'a' + 10;
    return 36;
}

static unsigned long 解析無號數(const char *字串, char **轉換末端位址,
                                    int 基數, int 無號旗標, int *負數旗標, int *溢位旗標)
{
    const char *目前位置 = 字串, *首次匹配位置;
    unsigned long 數值大小 = 0, 最大值;
    int 數字值;
    if (轉換末端位址) *轉換末端位址 = (char *)字串;
    *負數旗標 = 0;
    *溢位旗標 = 0;
    if (基數 && (基數 < 2 || 基數 > 36)) { 錯誤編號 = 錯誤引數無效; return 0; }
    while (檢查是否空白字元((unsigned char)*目前位置)) ++目前位置;
    if (*目前位置 == '+' || *目前位置 == '-') { *負數旗標 = *目前位置 == '-'; ++目前位置; }
    if ((基數 == 0 || 基數 == 16) && 目前位置[0] == '0' &&
        (目前位置[1] == 'x' || 目前位置[1] == 'X') && 取得數字值((unsigned char)目前位置[2]) < 16) {
        目前位置 += 2; 基數 = 16;
    }
    if (!基數) 基數 = *目前位置 == '0' ? 8 : 10;
    最大值 = 無號旗標 ? 無號長整數最大值 : (unsigned long)長整數最大值 + (unsigned long)*負數旗標;
    首次匹配位置 = 目前位置;
    while ((數字值 = 取得數字值((unsigned char)*目前位置)) < 基數) {
        if (數值大小 > (最大值 - (unsigned long)數字值) / (unsigned long)基數)
            *溢位旗標 = 1;
        else if (!*溢位旗標)
            數值大小 = 數值大小 * (unsigned long)基數 + (unsigned long)數字值;
        ++目前位置;
    }
    if (目前位置 == 首次匹配位置) return 0;
    if (轉換末端位址) *轉換末端位址 = (char *)目前位置;
    if (*溢位旗標) { 錯誤編號 = 錯誤數值超出範圍; return 最大值; }
    return 數值大小;
}

long 將字串讀為長整數(const char *字串, char **轉換末端位址, int 基數)
{
    int 負數旗標, 溢位旗標;
    unsigned long 數值大小 = 解析無號數(字串, 轉換末端位址, 基數, 0, &負數旗標, &溢位旗標);
    if (!負數旗標) return (long)數值大小;
    return 數值大小 == (unsigned long)長整數最大值 + 1UL ? 長整數最小值 : -(long)數值大小;
}

unsigned long 將字串讀為無號長整數(const char *字串, char **轉換末端位址, int 基數)
{
    int 負數旗標, 溢位旗標;
    unsigned long 數值大小 = 解析無號數(字串, 轉換末端位址, 基數, 1, &負數旗標, &溢位旗標);
    if (溢位旗標) return 無號長整數最大值;
    return 負數旗標 ? 0UL - 數值大小 : 數值大小;
}

int 將十進字串讀為整數(const char *字串) { return (int)將字串讀為長整數(字串, 空位址, 10); }
long 將十進字串讀為長整數(const char *字串) { return 將字串讀為長整數(字串, 空位址, 10); }
int 取得整數絕對值(int 值) { return 值 < 0 ? -值 : 值; }
long 取得長整數絕對值(long 值) { return 值 < 0 ? -值 : 值; }
整數除法結果型別 取得整數商餘數(int 左值, int 右值) { 整數除法結果型別 結果 = {左值 / 右值, 左值 % 右值}; return 結果; }
長整數除法結果型別 取得長整數商餘數(long 左值, long 右值) { 長整數除法結果型別 結果 = {左值 / 右值, 左值 % 右值}; return 結果; }

static void 交換元素(unsigned char *左值, unsigned char *右值, 大小型別 元素大小)
{
    while (元素大小--) { unsigned char 暫存值 = *左值; *左值++ = *右值; *右值++ = 暫存值; }
}

static void 向下調整排序(unsigned char *元素陣列, 大小型別 下沉位置, 大小型別 數量,
                      大小型別 元素大小, int (*比較函式)(const void *, const void *))
{
    while (下沉位置 < 數量 / 2) {
        大小型別 子項位置 = 下沉位置 * 2 + 1;
        if (子項位置 + 1 < 數量 && 比較函式(元素陣列 + 子項位置 * 元素大小, 元素陣列 + (子項位置 + 1) * 元素大小) < 0)
            ++子項位置;
        if (比較函式(元素陣列 + 下沉位置 * 元素大小, 元素陣列 + 子項位置 * 元素大小) >= 0) return;
        交換元素(元素陣列 + 下沉位置 * 元素大小, 元素陣列 + 子項位置 * 元素大小, 元素大小);
        下沉位置 = 子項位置;
    }
}

void 依比較規則排序(void *元素陣列, 大小型別 數量, 大小型別 元素大小,
           int (*比較函式)(const void *, const void *))
{
    unsigned char *目前位置 = 元素陣列;
    大小型別 索引;
    if (數量 < 2 || !元素大小 || 數量 > (大小型別)-1 / 元素大小) return;
    /* Heap sort: bounded stack, O(n log n), comparator receives array elements. */
    for (索引 = 數量 / 2; 索引; ) 向下調整排序(目前位置, --索引, 數量, 元素大小, 比較函式);
    for (索引 = 數量 - 1; 索引; --索引) {
        交換元素(目前位置, 目前位置 + 索引 * 元素大小, 元素大小);
        向下調整排序(目前位置, 0, 索引, 元素大小, 比較函式);
    }
}

void *在有序陣列中二分搜尋(const void *來源位置, const void *元素陣列, 大小型別 數量,
              大小型別 元素大小, int (*比較函式)(const void *, const void *))
{
    大小型別 下界 = 0, 上界 = 數量;
    const unsigned char *目前位置 = 元素陣列;
    if (!元素大小 || 數量 > (大小型別)-1 / 元素大小) return 空位址;
    while (下界 < 上界) {
        大小型別 中間位置 = 下界 + (上界 - 下界) / 2;
        int 結果 = 比較函式(來源位置, 目前位置 + 中間位置 * 元素大小);
        if (!結果) return (void *)(目前位置 + 中間位置 * 元素大小);
        if (結果 < 0) 上界 = 中間位置;
        else 下界 = 中間位置 + 1;
    }
    return 空位址;
}

char *取得環境變數值(const char *系統資料)
{
    大小型別 長度 = 取得字串位元組數(系統資料);
    char **目前位置 = 環境變數列表;
    if (!長度 || 尋找字串首個值(系統資料, '=') || !目前位置) return 空位址;
    while (*目前位置) {
        if (!限長比較字串(*目前位置, 系統資料, 長度) && (*目前位置)[長度] == '=') return *目前位置 + 長度 + 1;
        ++目前位置;
    }
    return 空位址;
}
