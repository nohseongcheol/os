/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <一般関数.h>
#include <文字列と記憶内容.h>
#include <入出力と実行.h>
#include <整数型.h>
#include <整数限界.h>
#include <誤り番号.h>

/* Single-thread runtime. Reuse and coalesce freed blocks; do not shrink brk.
 * A block header and every returned address are 16-byte aligned on i386.
 * Callers must not move brk backwards across live allocations. */
struct 記憶区画 {
    大きさ型 容量;
    struct 記憶区画 *次の区画;
    int 利用可能判定;
    unsigned int 整列埋込長;
};
static struct 記憶区画 *最初の区画;

void *記憶領域を確保する(大きさ型 大きさ)
{
    struct 記憶区画 *進行位置 = 最初の区画, *最後の区画 = 空番地, *確保元番地;
    大きさ型 全体長, 整列埋込長;
    void *番地;
    if (!大きさ) 大きさ = 1;
    if (大きさ > (大きさ型)整数最大値 - 2 * sizeof(struct 記憶区画)) { 誤り番号 = 誤り記憶不足; return 空番地; }
    大きさ = (大きさ + 15U) & ~15U;
    while (進行位置) {
        if (進行位置->利用可能判定 && 進行位置->容量 >= 大きさ) {
            if (進行位置->容量 - 大きさ >= sizeof(struct 記憶区画) + 16U) {
                確保元番地 = (struct 記憶区画 *)((unsigned char *)(進行位置 + 1) + 大きさ);
                確保元番地->容量 = 進行位置->容量 - 大きさ - sizeof(*確保元番地);
                確保元番地->次の区画 = 進行位置->次の区画;
                確保元番地->利用可能判定 = 1;
                進行位置->次の区画 = 確保元番地;
                進行位置->容量 = 大きさ;
            }
            進行位置->利用可能判定 = 0;
            return 進行位置 + 1;
        }
        最後の区画 = 進行位置; 進行位置 = 進行位置->次の区画;
    }
    番地 = 動的記憶の終端を移す(0);
    if (番地 == (void *)-1) return 空番地;
    整列埋込長 = (0U - (番地幅符号なし整数)番地) & 15U;
    全体長 = 整列埋込長 + sizeof(struct 記憶区画) + 大きさ;
    if ((番地幅符号なし整数)番地 > (番地幅符号なし整数)整数最大値 - 全体長) { 誤り番号 = 誤り記憶不足; return 空番地; }
    番地 = 動的記憶の終端を移す((int)全体長);
    if (番地 == (void *)-1) return 空番地;
    確保元番地 = (struct 記憶区画 *)((unsigned char *)番地 + 整列埋込長);
    確保元番地->容量 = 大きさ; 確保元番地->次の区画 = 空番地; 確保元番地->利用可能判定 = 0;
    if (最後の区画) 最後の区画->次の区画 = 確保元番地;
    else 最初の区画 = 確保元番地;
    return 確保元番地 + 1;
}

void 記憶領域を返す(void *番地)
{
    struct 記憶区画 *進行位置;
    if (!番地) return;
    ((struct 記憶区画 *)番地 - 1)->利用可能判定 = 1;
    進行位置 = 最初の区画;
    while (進行位置 && 進行位置->次の区画) {
        struct 記憶区画 *次の区画 = 進行位置->次の区画;
        if (進行位置->利用可能判定 && 次の区画->利用可能判定 &&
            (unsigned char *)(進行位置 + 1) + 進行位置->容量 == (unsigned char *)次の区画) {
            進行位置->容量 += sizeof(*次の区画) + 次の区画->容量;
            進行位置->次の区画 = 次の区画->次の区画;
        } else 進行位置 = 次の区画;
    }
}

void *零で満たした配列領域を確保する(大きさ型 数量, 大きさ型 要素の大きさ)
{
    void *番地;
    if (要素の大きさ && 数量 > (大きさ型)-1 / 要素の大きさ) { 誤り番号 = 誤り記憶不足; return 空番地; }
    番地 = 記憶領域を確保する(数量 * 要素の大きさ);
    if (番地) 記憶領域を値で満たす(番地, 0, 数量 * 要素の大きさ);
    return 番地;
}

void *記憶領域の大きさを変える(void *番地, 大きさ型 大きさ)
{
    void *書込先;
    struct 記憶区画 *進行位置;
    if (!番地) return 記憶領域を確保する(大きさ);
    /* Documented zero-size choice: retain a valid, freeable minimum block. */
    if (!大きさ) 大きさ = 1;
    進行位置 = (struct 記憶区画 *)番地 - 1;
    if (大きさ <= 進行位置->容量) return 番地;
    書込先 = 記憶領域を確保する(大きさ);
    if (!書込先) return 空番地;
    記憶内容を複写する(書込先, 番地, 進行位置->容量);
    記憶領域を返す(番地);
    return 書込先;
}
