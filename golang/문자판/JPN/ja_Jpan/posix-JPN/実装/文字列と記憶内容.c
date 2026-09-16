/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <文字列と記憶内容.h>
#include <文字列大小比較.h>
#include <一般関数.h>
#include <整数型.h>
#include <文字分類.h>

void *記憶内容を複写する(void *書込先, const void *読出元, 大きさ型 長さ)
{
    unsigned char *進行位置 = 書込先;
    const unsigned char *入力位置 = 読出元;
    while (長さ--) *進行位置++ = *入力位置++;
    return 書込先;
}

void *重なりを許して記憶内容を移す(void *書込先, const void *読出元, 大きさ型 長さ)
{
    unsigned char *進行位置 = 書込先;
    const unsigned char *入力位置 = 読出元;
    if ((番地幅符号なし整数)書込先 <= (番地幅符号なし整数)読出元)
        return 記憶内容を複写する(書込先, 読出元, 長さ);
    while (長さ) { --長さ; 進行位置[長さ] = 入力位置[長さ]; }
    return 書込先;
}

void *記憶領域を値で満たす(void *書込先, int 文字値, 大きさ型 長さ)
{
    unsigned char *進行位置 = 書込先;
    while (長さ--) *進行位置++ = (unsigned char)文字値;
    return 書込先;
}

int 記憶内容を比較する(const void *左の値, const void *右の値, 大きさ型 長さ)
{
    const unsigned char *進行位置 = 左の値, *入力位置 = 右の値;
    while (長さ--) {
        if (*進行位置 != *入力位置) return (int)*進行位置 - (int)*入力位置;
        ++進行位置; ++入力位置;
    }
    return 0;
}

void *記憶領域から値を探す(const void *読出元, int 文字値, 大きさ型 長さ)
{
    const unsigned char *進行位置 = 読出元;
    while (長さ--) {
        if (*進行位置 == (unsigned char)文字値) return (void *)進行位置;
        ++進行位置;
    }
    return 空番地;
}

大きさ型 文字列の八桁組数を得る(const char *文字列)
{
    const char *進行位置 = 文字列;
    while (*進行位置) ++進行位置;
    return (大きさ型)(進行位置 - 文字列);
}

大きさ型 上限内の文字列八桁組数を得る(const char *文字列, 大きさ型 上限)
{
    大きさ型 長さ = 0;
    while (長さ < 上限 && 文字列[長さ]) ++長さ;
    return 長さ;
}

char *文字列を複写して終端を得る(char *書込先, const char *読出元)
{
    while ((*書込先 = *読出元) != 0) { ++書込先; ++読出元; }
    return 書込先;
}

char *文字列を複写する(char *書込先, const char *読出元)
{
    文字列を複写して終端を得る(書込先, 読出元);
    return 書込先;
}

char *上限まで埋めて複写し終端を得る(char *書込先, const char *読出元, 大きさ型 上限)
{
    大きさ型 長さ = 上限内の文字列八桁組数を得る(読出元, 上限);
    記憶内容を複写する(書込先, 読出元, 長さ);
    記憶領域を値で満たす(書込先 + 長さ, 0, 上限 - 長さ);
    return 書込先 + 長さ;
}

char *上限まで埋めて文字列を複写する(char *書込先, const char *読出元, 大きさ型 上限)
{
    上限まで埋めて複写し終端を得る(書込先, 読出元, 上限);
    return 書込先;
}

char *文字列を付け足す(char *書込先, const char *読出元)
{
    文字列を複写して終端を得る(書込先 + 文字列の八桁組数を得る(書込先), 読出元);
    return 書込先;
}

char *上限内で文字列を付け足す(char *書込先, const char *読出元, 大きさ型 上限)
{
    char *進行位置 = 書込先 + 文字列の八桁組数を得る(書込先);
    大きさ型 長さ = 上限内の文字列八桁組数を得る(読出元, 上限);
    記憶内容を複写する(進行位置, 読出元, 長さ);
    進行位置[長さ] = 0;
    return 書込先;
}

int 文字列を比較する(const char *左の値, const char *右の値)
{
    while (*左の値 && *左の値 == *右の値) { ++左の値; ++右の値; }
    return (int)(unsigned char)*左の値 - (int)(unsigned char)*右の値;
}

int 上限内で文字列を比較する(const char *左の値, const char *右の値, 大きさ型 上限)
{
    while (上限--) {
        int 結果 = (int)(unsigned char)*左の値 - (int)(unsigned char)*右の値;
        if (結果 || !*左の値) return 結果;
        ++左の値; ++右の値;
    }
    return 0;
}

/* The only active locale in this runtime is the initial C/POSIX locale. */
int 整列規則で文字列を比較する(const char *左の値, const char *右の値) { return 文字列を比較する(左の値, 右の値); }

大きさ型 文字列の整列鍵を作る(char *書込先, const char *読出元, 大きさ型 上限)
{
    大きさ型 長さ = 文字列の八桁組数を得る(読出元);
    if (上限) {
        大きさ型 複写長 = 長さ < 上限 ? 長さ : 上限;
        記憶内容を複写する(書込先, 読出元, 複写長);
        if (長さ < 上限) 書込先[長さ] = 0;
    }
    return 長さ;
}

char *文字列から最初の値を探す(const char *文字列, int 文字値)
{
    do {
        if (*文字列 == (char)文字値) return (char *)文字列;
    } while (*文字列++);
    return 空番地;
}

char *文字列から最後の値を探す(const char *文字列, int 文字値)
{
    char *発見位置 = 空番地;
    do { if (*文字列 == (char)文字値) 発見位置 = (char *)文字列; } while (*文字列++);
    return 発見位置;
}

char *文字列から部分列を探す(const char *文字列, const char *読出元)
{
    大きさ型 長さ = 文字列の八桁組数を得る(読出元);
    if (!長さ) return (char *)文字列;
    while (*文字列) {
        if (上限内で文字列を比較する(文字列, 読出元, 長さ) == 0) return (char *)文字列;
        ++文字列;
    }
    return 空番地;
}

大きさ型 許容値からなる先頭長を得る(const char *文字列, const char *区切り値集合)
{
    大きさ型 長さ = 0;
    while (文字列[長さ] && 文字列から最初の値を探す(区切り値集合, 文字列[長さ])) ++長さ;
    return 長さ;
}

大きさ型 除外値のない先頭長を得る(const char *文字列, const char *区切り値集合)
{
    大きさ型 長さ = 0;
    while (文字列[長さ] && !文字列から最初の値を探す(区切り値集合, 文字列[長さ])) ++長さ;
    return 長さ;
}

char *文字列から集合の値を探す(const char *文字列, const char *区切り値集合)
{
    const char *進行位置 = 文字列 + 除外値のない先頭長を得る(文字列, 区切り値集合);
    return *進行位置 ? (char *)進行位置 : 空番地;
}

char *進行状態を指定して文字列を語に分ける(char *文字列, const char *区切り値集合, char **保存進行状態)
{
    char *進行位置 = 文字列 ? 文字列 : *保存進行状態;
    if (!進行位置) return 空番地;
    進行位置 += 許容値からなる先頭長を得る(進行位置, 区切り値集合);
    if (!*進行位置) { *保存進行状態 = 進行位置; return 空番地; }
    文字列 = 進行位置;
    進行位置 += 除外値のない先頭長を得る(進行位置, 区切り値集合);
    if (*進行位置) *進行位置++ = 0;
    *保存進行状態 = 進行位置;
    return 文字列;
}

char *文字列を語に分ける(char *文字列, const char *区切り値集合)
{
    static char *保存進行状態;
    return 進行状態を指定して文字列を語に分ける(文字列, 区切り値集合, &保存進行状態);
}

char *上限内で新しい領域に文字列を複製する(const char *文字列, 大きさ型 上限)
{
    大きさ型 長さ = 上限内の文字列八桁組数を得る(文字列, 上限);
    char *書込先 = 記憶領域を確保する(長さ + 1);
    if (書込先) { 記憶内容を複写する(書込先, 文字列, 長さ); 書込先[長さ] = 0; }
    return 書込先;
}

char *新しい領域に文字列を複製する(const char *文字列) { return 上限内で新しい領域に文字列を複製する(文字列, 文字列の八桁組数を得る(文字列)); }

int 上限内で大文字小文字を区別せず比較する(const char *左の値, const char *右の値, 大きさ型 上限)
{
    while (上限--) {
        int 結果 = 小文字に変える((unsigned char)*左の値) - 小文字に変える((unsigned char)*右の値);
        if (結果 || !*左の値) return 結果;
        ++左の値; ++右の値;
    }
    return 0;
}

int 大文字小文字を区別せず比較する(const char *左の値, const char *右の値)
{
    while (*左の値 && 小文字に変える((unsigned char)*左の値) == 小文字に変える((unsigned char)*右の値)) { ++左の値; ++右の値; }
    return 小文字に変える((unsigned char)*左の値) - 小文字に変える((unsigned char)*右の値);
}
