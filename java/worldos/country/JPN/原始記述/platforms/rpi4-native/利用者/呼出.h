#ifndef 自前利用者呼出しヘッダー
#define 自前利用者呼出しヘッダー
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=呼出 番号, x0..x5=引数, x0=結果/負数値 エラー. Linux ABI 아님.
static inline intptr_t 利用者呼出(uintptr_t 番号, uintptr_t 先頭位置被演算子, uintptr_t 第二被演算子, uintptr_t 第三被演算子,
                                uintptr_t 第四被演算子, uintptr_t 第五被演算子, uintptr_t 第六被演算子) {
    register uintptr_t 零レジスタ __asm__("x0") = 先頭位置被演算子;
    register uintptr_t 一レジスタ __asm__("x1") = 第二被演算子;
    register uintptr_t 二レジスタ __asm__("x2") = 第三被演算子;
    register uintptr_t 三レジスタ __asm__("x3") = 第四被演算子;
    register uintptr_t 四レジスタ __asm__("x4") = 第五被演算子;
    register uintptr_t 五レジスタ __asm__("x5") = 第六被演算子;
    register uintptr_t 八レジスタ __asm__("x8") = 番号;
    __asm__ volatile("svc #0" : "+r"(零レジスタ) : "r"(一レジスタ), "r"(二レジスタ), "r"(三レジスタ), "r"(四レジスタ), "r"(五レジスタ), "r"(八レジスタ) : "memory", "cc");
    return (intptr_t)零レジスタ;
}
static inline intptr_t 画面矩形(unsigned 横座標, unsigned 縦座標, unsigned 要求済み幅値, unsigned 要求済み高さ値, unsigned RGB色) {
    return 利用者呼出(13, 横座標, 縦座標, RGB色, 要求済み幅値, 要求済み高さ値, 0);
}
static inline intptr_t 利用者記憶終端位置(uintptr_t 終端) { return 利用者呼出(8, 終端, 0, 0, 0, 0, 0); }
static inline intptr_t 画面幅読取(void) { return 利用者呼出(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t 画面高さ読取(void) { return 利用者呼出(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t 対象画面キー待合(void) {
    intptr_t 結果 = 利用者呼出(16, 0, 0, 0, 0, 0, 0);
    if (結果 < 0) return 結果;
    do { 結果 = 利用者呼出(16, 1, 0, 0, 0, 0, 0); } while (結果 == -11);
    利用者呼出(16, 2, 0, 0, 0, 0, 0);
    return 結果;
}
static inline intptr_t 利用者引数個数(void) { return 利用者呼出(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t 利用者引数(unsigned 番号, char *内容物値, size_t 容量) {
    return 利用者呼出(15, 番号, (uintptr_t)内容物値, 容量, 0, 0, 0);
}
#endif
