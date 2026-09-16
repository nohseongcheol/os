#include <通用函数.h>
#include <字符串与内存内容.h>
#include <字符分类.h>
#include <错误编号.h>
#include <整数极限.h>
#include <输入输出与执行.h>

static int 取得数字值(unsigned char 字符值)
{
    if (检查是否十进数字(字符值)) return 字符值 - '0';
    if (检查是否字母(字符值)) return 转换为小写(字符值) - 'a' + 10;
    return 36;
}

static unsigned long 解析无符号数(const char *字符串, char **转换末端地址,
                                    int 基数, int 无符号标志, int *负数标志, int *溢出标志)
{
    const char *当前位置 = 字符串, *首次匹配位置;
    unsigned long 数值大小 = 0, 最大值;
    int 数字值;
    if (转换末端地址) *转换末端地址 = (char *)字符串;
    *负数标志 = 0;
    *溢出标志 = 0;
    if (基数 && (基数 < 2 || 基数 > 36)) { 错误编号 = 错误参数无效; return 0; }
    while (检查是否空白字符((unsigned char)*当前位置)) ++当前位置;
    if (*当前位置 == '+' || *当前位置 == '-') { *负数标志 = *当前位置 == '-'; ++当前位置; }
    if ((基数 == 0 || 基数 == 16) && 当前位置[0] == '0' &&
        (当前位置[1] == 'x' || 当前位置[1] == 'X') && 取得数字值((unsigned char)当前位置[2]) < 16) {
        当前位置 += 2; 基数 = 16;
    }
    if (!基数) 基数 = *当前位置 == '0' ? 8 : 10;
    最大值 = 无符号标志 ? 无符号长整数最大值 : (unsigned long)长整数最大值 + (unsigned long)*负数标志;
    首次匹配位置 = 当前位置;
    while ((数字值 = 取得数字值((unsigned char)*当前位置)) < 基数) {
        if (数值大小 > (最大值 - (unsigned long)数字值) / (unsigned long)基数)
            *溢出标志 = 1;
        else if (!*溢出标志)
            数值大小 = 数值大小 * (unsigned long)基数 + (unsigned long)数字值;
        ++当前位置;
    }
    if (当前位置 == 首次匹配位置) return 0;
    if (转换末端地址) *转换末端地址 = (char *)当前位置;
    if (*溢出标志) { 错误编号 = 错误数值超出范围; return 最大值; }
    return 数值大小;
}

long 将字符串读为长整数(const char *字符串, char **转换末端地址, int 基数)
{
    int 负数标志, 溢出标志;
    unsigned long 数值大小 = 解析无符号数(字符串, 转换末端地址, 基数, 0, &负数标志, &溢出标志);
    if (!负数标志) return (long)数值大小;
    return 数值大小 == (unsigned long)长整数最大值 + 1UL ? 长整数最小值 : -(long)数值大小;
}

unsigned long 将字符串读为无符号长整数(const char *字符串, char **转换末端地址, int 基数)
{
    int 负数标志, 溢出标志;
    unsigned long 数值大小 = 解析无符号数(字符串, 转换末端地址, 基数, 1, &负数标志, &溢出标志);
    if (溢出标志) return 无符号长整数最大值;
    return 负数标志 ? 0UL - 数值大小 : 数值大小;
}

int 将十进字符串读为整数(const char *字符串) { return (int)将字符串读为长整数(字符串, 空地址, 10); }
long 将十进字符串读为长整数(const char *字符串) { return 将字符串读为长整数(字符串, 空地址, 10); }
int 取得整数绝对值(int 值) { return 值 < 0 ? -值 : 值; }
long 取得长整数绝对值(long 值) { return 值 < 0 ? -值 : 值; }
整数除法结果类型 取得整数商余数(int 左值, int 右值) { 整数除法结果类型 结果 = {左值 / 右值, 左值 % 右值}; return 结果; }
长整数除法结果类型 取得长整数商余数(long 左值, long 右值) { 长整数除法结果类型 结果 = {左值 / 右值, 左值 % 右值}; return 结果; }

static void 交换元素(unsigned char *左值, unsigned char *右值, 大小类型 元素大小)
{
    while (元素大小--) { unsigned char 临时值 = *左值; *左值++ = *右值; *右值++ = 临时值; }
}

static void 向下调整排序(unsigned char *元素数组, 大小类型 下沉位置, 大小类型 数量,
                      大小类型 元素大小, int (*比较函数)(const void *, const void *))
{
    while (下沉位置 < 数量 / 2) {
        大小类型 子项位置 = 下沉位置 * 2 + 1;
        if (子项位置 + 1 < 数量 && 比较函数(元素数组 + 子项位置 * 元素大小, 元素数组 + (子项位置 + 1) * 元素大小) < 0)
            ++子项位置;
        if (比较函数(元素数组 + 下沉位置 * 元素大小, 元素数组 + 子项位置 * 元素大小) >= 0) return;
        交换元素(元素数组 + 下沉位置 * 元素大小, 元素数组 + 子项位置 * 元素大小, 元素大小);
        下沉位置 = 子项位置;
    }
}

void 按比较规则排序(void *元素数组, 大小类型 数量, 大小类型 元素大小,
           int (*比较函数)(const void *, const void *))
{
    unsigned char *当前位置 = 元素数组;
    大小类型 索引;
    if (数量 < 2 || !元素大小 || 数量 > (大小类型)-1 / 元素大小) return;
    /* Heap sort: bounded stack, O(n log n), comparator receives array elements. */
    for (索引 = 数量 / 2; 索引; ) 向下调整排序(当前位置, --索引, 数量, 元素大小, 比较函数);
    for (索引 = 数量 - 1; 索引; --索引) {
        交换元素(当前位置, 当前位置 + 索引 * 元素大小, 元素大小);
        向下调整排序(当前位置, 0, 索引, 元素大小, 比较函数);
    }
}

void *在有序数组中二分查找(const void *来源位置, const void *元素数组, 大小类型 数量,
              大小类型 元素大小, int (*比较函数)(const void *, const void *))
{
    大小类型 下界 = 0, 上界 = 数量;
    const unsigned char *当前位置 = 元素数组;
    if (!元素大小 || 数量 > (大小类型)-1 / 元素大小) return 空地址;
    while (下界 < 上界) {
        大小类型 中间位置 = 下界 + (上界 - 下界) / 2;
        int 结果 = 比较函数(来源位置, 当前位置 + 中间位置 * 元素大小);
        if (!结果) return (void *)(当前位置 + 中间位置 * 元素大小);
        if (结果 < 0) 上界 = 中间位置;
        else 下界 = 中间位置 + 1;
    }
    return 空地址;
}

char *取得环境变量值(const char *系统资料)
{
    大小类型 长度 = 取得字符串字节数(系统资料);
    char **当前位置 = 环境变量列表;
    if (!长度 || 查找字符串首个值(系统资料, '=') || !当前位置) return 空地址;
    while (*当前位置) {
        if (!限长比较字符串(*当前位置, 系统资料, 长度) && (*当前位置)[长度] == '=') return *当前位置 + 长度 + 1;
        ++当前位置;
    }
    return 空地址;
}
