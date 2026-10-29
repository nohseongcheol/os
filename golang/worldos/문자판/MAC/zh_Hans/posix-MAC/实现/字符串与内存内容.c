#include <字符串与内存内容.h>
#include <字符串大小写比较.h>
#include <通用函数.h>
#include <整数类型.h>
#include <字符分类.h>

void *复制内存内容(void *目标位置, const void *来源位置, 大小类型 长度)
{
    unsigned char *当前位置 = 目标位置;
    const unsigned char *输入位置 = 来源位置;
    while (长度--) *当前位置++ = *输入位置++;
    return 目标位置;
}

void *允许重叠移动内存内容(void *目标位置, const void *来源位置, 大小类型 长度)
{
    unsigned char *当前位置 = 目标位置;
    const unsigned char *输入位置 = 来源位置;
    if ((地址宽度无符号整数)目标位置 <= (地址宽度无符号整数)来源位置)
        return 复制内存内容(目标位置, 来源位置, 长度);
    while (长度) { --长度; 当前位置[长度] = 输入位置[长度]; }
    return 目标位置;
}

void *用值填充内存区域(void *目标位置, int 字符值, 大小类型 长度)
{
    unsigned char *当前位置 = 目标位置;
    while (长度--) *当前位置++ = (unsigned char)字符值;
    return 目标位置;
}

int 比较内存内容(const void *左值, const void *右值, 大小类型 长度)
{
    const unsigned char *当前位置 = 左值, *输入位置 = 右值;
    while (长度--) {
        if (*当前位置 != *输入位置) return (int)*当前位置 - (int)*输入位置;
        ++当前位置; ++输入位置;
    }
    return 0;
}

void *在内存中查找值(const void *来源位置, int 字符值, 大小类型 长度)
{
    const unsigned char *当前位置 = 来源位置;
    while (长度--) {
        if (*当前位置 == (unsigned char)字符值) return (void *)当前位置;
        ++当前位置;
    }
    return 空地址;
}

大小类型 取得字符串字节数(const char *字符串)
{
    const char *当前位置 = 字符串;
    while (*当前位置) ++当前位置;
    return (大小类型)(当前位置 - 字符串);
}

大小类型 取得限长字符串字节数(const char *字符串, 大小类型 上限)
{
    大小类型 长度 = 0;
    while (长度 < 上限 && 字符串[长度]) ++长度;
    return 长度;
}

char *复制字符串并取得末端(char *目标位置, const char *来源位置)
{
    while ((*目标位置 = *来源位置) != 0) { ++目标位置; ++来源位置; }
    return 目标位置;
}

char *复制字符串(char *目标位置, const char *来源位置)
{
    复制字符串并取得末端(目标位置, 来源位置);
    return 目标位置;
}

char *定长填充复制并取得末端(char *目标位置, const char *来源位置, 大小类型 上限)
{
    大小类型 长度 = 取得限长字符串字节数(来源位置, 上限);
    复制内存内容(目标位置, 来源位置, 长度);
    用值填充内存区域(目标位置 + 长度, 0, 上限 - 长度);
    return 目标位置 + 长度;
}

char *定长填充复制字符串(char *目标位置, const char *来源位置, 大小类型 上限)
{
    定长填充复制并取得末端(目标位置, 来源位置, 上限);
    return 目标位置;
}

char *追加字符串(char *目标位置, const char *来源位置)
{
    复制字符串并取得末端(目标位置 + 取得字符串字节数(目标位置), 来源位置);
    return 目标位置;
}

char *限长追加字符串(char *目标位置, const char *来源位置, 大小类型 上限)
{
    char *当前位置 = 目标位置 + 取得字符串字节数(目标位置);
    大小类型 长度 = 取得限长字符串字节数(来源位置, 上限);
    复制内存内容(当前位置, 来源位置, 长度);
    当前位置[长度] = 0;
    return 目标位置;
}

int 比较字符串(const char *左值, const char *右值)
{
    while (*左值 && *左值 == *右值) { ++左值; ++右值; }
    return (int)(unsigned char)*左值 - (int)(unsigned char)*右值;
}

int 限长比较字符串(const char *左值, const char *右值, 大小类型 上限)
{
    while (上限--) {
        int 结果 = (int)(unsigned char)*左值 - (int)(unsigned char)*右值;
        if (结果 || !*左值) return 结果;
        ++左值; ++右值;
    }
    return 0;
}

/* The only active locale in this runtime is the initial C/POSIX locale. */
int 按排序规则比较字符串(const char *左值, const char *右值) { return 比较字符串(左值, 右值); }

大小类型 生成字符串排序键(char *目标位置, const char *来源位置, 大小类型 上限)
{
    大小类型 长度 = 取得字符串字节数(来源位置);
    if (上限) {
        大小类型 复制长度 = 长度 < 上限 ? 长度 : 上限;
        复制内存内容(目标位置, 来源位置, 复制长度);
        if (长度 < 上限) 目标位置[长度] = 0;
    }
    return 长度;
}

char *查找字符串首个值(const char *字符串, int 字符值)
{
    do {
        if (*字符串 == (char)字符值) return (char *)字符串;
    } while (*字符串++);
    return 空地址;
}

char *查找字符串最后值(const char *字符串, int 字符值)
{
    char *找到位置 = 空地址;
    do { if (*字符串 == (char)字符值) 找到位置 = (char *)字符串; } while (*字符串++);
    return 找到位置;
}

char *查找子字符串(const char *字符串, const char *来源位置)
{
    大小类型 长度 = 取得字符串字节数(来源位置);
    if (!长度) return (char *)字符串;
    while (*字符串) {
        if (限长比较字符串(字符串, 来源位置, 长度) == 0) return (char *)字符串;
        ++字符串;
    }
    return 空地址;
}

大小类型 取得允许值前缀长度(const char *字符串, const char *分隔值集合)
{
    大小类型 长度 = 0;
    while (字符串[长度] && 查找字符串首个值(分隔值集合, 字符串[长度])) ++长度;
    return 长度;
}

大小类型 取得无排除值前缀长度(const char *字符串, const char *分隔值集合)
{
    大小类型 长度 = 0;
    while (字符串[长度] && !查找字符串首个值(分隔值集合, 字符串[长度])) ++长度;
    return 长度;
}

char *查找字符串中的集合值(const char *字符串, const char *分隔值集合)
{
    const char *当前位置 = 字符串 + 取得无排除值前缀长度(字符串, 分隔值集合);
    return *当前位置 ? (char *)当前位置 : 空地址;
}

char *指定状态分割字符串词段(char *字符串, const char *分隔值集合, char **保存进度状态)
{
    char *当前位置 = 字符串 ? 字符串 : *保存进度状态;
    if (!当前位置) return 空地址;
    当前位置 += 取得允许值前缀长度(当前位置, 分隔值集合);
    if (!*当前位置) { *保存进度状态 = 当前位置; return 空地址; }
    字符串 = 当前位置;
    当前位置 += 取得无排除值前缀长度(当前位置, 分隔值集合);
    if (*当前位置) *当前位置++ = 0;
    *保存进度状态 = 当前位置;
    return 字符串;
}

char *分割字符串词段(char *字符串, const char *分隔值集合)
{
    static char *保存进度状态;
    return 指定状态分割字符串词段(字符串, 分隔值集合, &保存进度状态);
}

char *限长在新空间复制字符串(const char *字符串, 大小类型 上限)
{
    大小类型 长度 = 取得限长字符串字节数(字符串, 上限);
    char *目标位置 = 分配内存空间(长度 + 1);
    if (目标位置) { 复制内存内容(目标位置, 字符串, 长度); 目标位置[长度] = 0; }
    return 目标位置;
}

char *在新空间复制字符串(const char *字符串) { return 限长在新空间复制字符串(字符串, 取得字符串字节数(字符串)); }

int 限长忽略大小写比较字符串(const char *左值, const char *右值, 大小类型 上限)
{
    while (上限--) {
        int 结果 = 转换为小写((unsigned char)*左值) - 转换为小写((unsigned char)*右值);
        if (结果 || !*左值) return 结果;
        ++左值; ++右值;
    }
    return 0;
}

int 忽略大小写比较字符串(const char *左值, const char *右值)
{
    while (*左值 && 转换为小写((unsigned char)*左值) == 转换为小写((unsigned char)*右值)) { ++左值; ++右值; }
    return 转换为小写((unsigned char)*左值) - 转换为小写((unsigned char)*右值);
}
