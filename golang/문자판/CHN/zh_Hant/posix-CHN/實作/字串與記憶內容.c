/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <字串與記憶內容.h>
#include <字串大小寫比較.h>
#include <通用函式.h>
#include <整數型別.h>
#include <字元分類.h>

void *複製記憶內容(void *目標位置, const void *來源位置, 大小型別 長度)
{
    unsigned char *目前位置 = 目標位置;
    const unsigned char *輸入位置 = 來源位置;
    while (長度--) *目前位置++ = *輸入位置++;
    return 目標位置;
}

void *允許重疊移動記憶內容(void *目標位置, const void *來源位置, 大小型別 長度)
{
    unsigned char *目前位置 = 目標位置;
    const unsigned char *輸入位置 = 來源位置;
    if ((位址寬度無號整數)目標位置 <= (位址寬度無號整數)來源位置)
        return 複製記憶內容(目標位置, 來源位置, 長度);
    while (長度) { --長度; 目前位置[長度] = 輸入位置[長度]; }
    return 目標位置;
}

void *以值填滿記憶區域(void *目標位置, int 字元值, 大小型別 長度)
{
    unsigned char *目前位置 = 目標位置;
    while (長度--) *目前位置++ = (unsigned char)字元值;
    return 目標位置;
}

int 比較記憶內容(const void *左值, const void *右值, 大小型別 長度)
{
    const unsigned char *目前位置 = 左值, *輸入位置 = 右值;
    while (長度--) {
        if (*目前位置 != *輸入位置) return (int)*目前位置 - (int)*輸入位置;
        ++目前位置; ++輸入位置;
    }
    return 0;
}

void *在記憶中尋找值(const void *來源位置, int 字元值, 大小型別 長度)
{
    const unsigned char *目前位置 = 來源位置;
    while (長度--) {
        if (*目前位置 == (unsigned char)字元值) return (void *)目前位置;
        ++目前位置;
    }
    return 空位址;
}

大小型別 取得字串位元組數(const char *字串)
{
    const char *目前位置 = 字串;
    while (*目前位置) ++目前位置;
    return (大小型別)(目前位置 - 字串);
}

大小型別 取得限長字串位元組數(const char *字串, 大小型別 上限)
{
    大小型別 長度 = 0;
    while (長度 < 上限 && 字串[長度]) ++長度;
    return 長度;
}

char *複製字串並取得末端(char *目標位置, const char *來源位置)
{
    while ((*目標位置 = *來源位置) != 0) { ++目標位置; ++來源位置; }
    return 目標位置;
}

char *複製字串(char *目標位置, const char *來源位置)
{
    複製字串並取得末端(目標位置, 來源位置);
    return 目標位置;
}

char *定長填補複製並取得末端(char *目標位置, const char *來源位置, 大小型別 上限)
{
    大小型別 長度 = 取得限長字串位元組數(來源位置, 上限);
    複製記憶內容(目標位置, 來源位置, 長度);
    以值填滿記憶區域(目標位置 + 長度, 0, 上限 - 長度);
    return 目標位置 + 長度;
}

char *定長填補複製字串(char *目標位置, const char *來源位置, 大小型別 上限)
{
    定長填補複製並取得末端(目標位置, 來源位置, 上限);
    return 目標位置;
}

char *附加字串(char *目標位置, const char *來源位置)
{
    複製字串並取得末端(目標位置 + 取得字串位元組數(目標位置), 來源位置);
    return 目標位置;
}

char *限長附加字串(char *目標位置, const char *來源位置, 大小型別 上限)
{
    char *目前位置 = 目標位置 + 取得字串位元組數(目標位置);
    大小型別 長度 = 取得限長字串位元組數(來源位置, 上限);
    複製記憶內容(目前位置, 來源位置, 長度);
    目前位置[長度] = 0;
    return 目標位置;
}

int 比較字串(const char *左值, const char *右值)
{
    while (*左值 && *左值 == *右值) { ++左值; ++右值; }
    return (int)(unsigned char)*左值 - (int)(unsigned char)*右值;
}

int 限長比較字串(const char *左值, const char *右值, 大小型別 上限)
{
    while (上限--) {
        int 結果 = (int)(unsigned char)*左值 - (int)(unsigned char)*右值;
        if (結果 || !*左值) return 結果;
        ++左值; ++右值;
    }
    return 0;
}

/* The only active locale in this runtime is the initial C/POSIX locale. */
int 依排序規則比較字串(const char *左值, const char *右值) { return 比較字串(左值, 右值); }

大小型別 產生字串排序鍵(char *目標位置, const char *來源位置, 大小型別 上限)
{
    大小型別 長度 = 取得字串位元組數(來源位置);
    if (上限) {
        大小型別 複製長度 = 長度 < 上限 ? 長度 : 上限;
        複製記憶內容(目標位置, 來源位置, 複製長度);
        if (長度 < 上限) 目標位置[長度] = 0;
    }
    return 長度;
}

char *尋找字串首個值(const char *字串, int 字元值)
{
    do {
        if (*字串 == (char)字元值) return (char *)字串;
    } while (*字串++);
    return 空位址;
}

char *尋找字串最後值(const char *字串, int 字元值)
{
    char *找到位置 = 空位址;
    do { if (*字串 == (char)字元值) 找到位置 = (char *)字串; } while (*字串++);
    return 找到位置;
}

char *尋找子字串(const char *字串, const char *來源位置)
{
    大小型別 長度 = 取得字串位元組數(來源位置);
    if (!長度) return (char *)字串;
    while (*字串) {
        if (限長比較字串(字串, 來源位置, 長度) == 0) return (char *)字串;
        ++字串;
    }
    return 空位址;
}

大小型別 取得允許值前綴長度(const char *字串, const char *分隔值集合)
{
    大小型別 長度 = 0;
    while (字串[長度] && 尋找字串首個值(分隔值集合, 字串[長度])) ++長度;
    return 長度;
}

大小型別 取得無排除值前綴長度(const char *字串, const char *分隔值集合)
{
    大小型別 長度 = 0;
    while (字串[長度] && !尋找字串首個值(分隔值集合, 字串[長度])) ++長度;
    return 長度;
}

char *尋找字串中的集合值(const char *字串, const char *分隔值集合)
{
    const char *目前位置 = 字串 + 取得無排除值前綴長度(字串, 分隔值集合);
    return *目前位置 ? (char *)目前位置 : 空位址;
}

char *指定狀態分割字串詞段(char *字串, const char *分隔值集合, char **保存進度狀態)
{
    char *目前位置 = 字串 ? 字串 : *保存進度狀態;
    if (!目前位置) return 空位址;
    目前位置 += 取得允許值前綴長度(目前位置, 分隔值集合);
    if (!*目前位置) { *保存進度狀態 = 目前位置; return 空位址; }
    字串 = 目前位置;
    目前位置 += 取得無排除值前綴長度(目前位置, 分隔值集合);
    if (*目前位置) *目前位置++ = 0;
    *保存進度狀態 = 目前位置;
    return 字串;
}

char *分割字串詞段(char *字串, const char *分隔值集合)
{
    static char *保存進度狀態;
    return 指定狀態分割字串詞段(字串, 分隔值集合, &保存進度狀態);
}

char *限長在新空間複製字串(const char *字串, 大小型別 上限)
{
    大小型別 長度 = 取得限長字串位元組數(字串, 上限);
    char *目標位置 = 配置記憶空間(長度 + 1);
    if (目標位置) { 複製記憶內容(目標位置, 字串, 長度); 目標位置[長度] = 0; }
    return 目標位置;
}

char *在新空間複製字串(const char *字串) { return 限長在新空間複製字串(字串, 取得字串位元組數(字串)); }

int 限長忽略大小寫比較字串(const char *左值, const char *右值, 大小型別 上限)
{
    while (上限--) {
        int 結果 = 轉換為小寫((unsigned char)*左值) - 轉換為小寫((unsigned char)*右值);
        if (結果 || !*左值) return 結果;
        ++左值; ++右值;
    }
    return 0;
}

int 忽略大小寫比較字串(const char *左值, const char *右值)
{
    while (*左值 && 轉換為小寫((unsigned char)*左值) == 轉換為小寫((unsigned char)*右值)) { ++左值; ++右值; }
    return 轉換為小寫((unsigned char)*左值) - 轉換為小寫((unsigned char)*右值);
}
