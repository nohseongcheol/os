/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <体系/子の待機.h>
#include <入出力と実行.h>

static void 電文を書く(const char *文字列, unsigned int 大きさ)
{
    (void)書く(標準出力番号, 文字列, 大きさ);
}

int main(void)
{
    volatile unsigned char *開始位置 = (volatile unsigned char *)動的記憶の終端を移す(0);
    volatile unsigned char *記憶領域;
    実行過程番号型 子の位置;
    int 終了状態;

    電文を書く("\nPOSIX-HEAP:START\n", 18);
    記憶領域 = (volatile unsigned char *)動的記憶の終端を移す(32);
    if (開始位置 == (void *)-1 || 記憶領域 != 開始位置 || 動的記憶の終端を移す(0) != (void *)(開始位置 + 32)) {
        電文を書く("PTEST:FAIL:sbrk-grow\n", 22);
        直ちに終了する(1);
    }
    電文を書く("PTEST:PASS:sbrk-grow\n", 22);
    記憶領域[0] = 0x5a;
    記憶領域[31] = 0xa5;
    if (記憶領域[0] != 0x5a || 記憶領域[31] != 0xa5) {
        電文を書く("PTEST:FAIL:sbrk-memory\n", 24);
        直ちに終了する(1);
    }
    電文を書く("PTEST:PASS:sbrk-memory\n", 24);
    if (動的記憶の終端を定める((void *)開始位置) != 0 || 動的記憶の終端を移す(0) != (void *)開始位置) {
        電文を書く("PTEST:FAIL:brk-restore\n", 24);
        直ちに終了する(1);
    }
    電文を書く("PTEST:PASS:brk-restore\n", 24);

    子の位置 = 実行過程を分岐する();
    if (子の位置 == 0) {
        if (動的記憶の終端を移す(64) != (void *)開始位置)
            直ちに終了する(2);
        直ちに終了する(0);
    }
    if (子の位置 < 0 || 指定した子を待つ(子の位置, &終了状態, 0) != 子の位置 ||
        !正常終了判定(終了状態) || 終了値取出し(終了状態) != 0 ||
        動的記憶の終端を移す(0) != (void *)開始位置) {
        電文を書く("PTEST:FAIL:brk-process-isolation\n", 33);
        直ちに終了する(1);
    }
    電文を書く("PTEST:PASS:brk-process-isolation\n", 33);
    電文を書く("POSIX-HEAP:PASS\n", 16);
    直ちに終了する(0);
}
