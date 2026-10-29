#ifndef 自前画面情報ヘッダー
#define 自前画面情報ヘッダー
#include <stdint.h>
/* 초기화가 끝난 実際データ RGB32 画面 容量. 준비되지 않았으면 0이다. */
uintptr_t 基板画面幅(void);
uintptr_t 基板画面高さ(void);
/* 0: 隠蔽値, 1: 화살표, 2: 좌상↔우하, 3: 우상↔좌하. */
void 基板ポインタ(int 水平位置, int 垂直位置, unsigned 形状値);
/* 한 번에 32줄을 완성한 後端値, 달라진 화소만 実際データ 화면에 옮긴다. */
void 基板用意描画中(volatile uint32_t *データ, unsigned 幅跨域, unsigned 長さ, unsigned 行間隔値);
int 基板描画中境界(int *水平位置, int *垂直位置, int *幅跨域, int *長さ);
int 基板開始処理描画中(int 水平位置, int 垂直位置, int 幅跨域, int 長さ);
void 基板終了処理描画中(void);
void 基板矩形塗潰し(int 水平位置, int 垂直位置, int 幅跨域, int 長さ, uint32_t 色値);
/* 実際データ 値表示 메모리에 기록한 画素 数. ポインタ 갱신은 제외한다. */
uint64_t 基板描画中個数(void);
uint32_t 基板読取画面(unsigned 水平位置, unsigned 垂直位置);
#endif
