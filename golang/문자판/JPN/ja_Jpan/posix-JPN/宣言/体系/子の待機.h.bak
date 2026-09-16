#ifndef _宣言_体系_子の待機
#define _宣言_体系_子の待機

#include <体系/資料型.h>

#define 未準備なら待たない 1
#define 終了値取出し(終了状態) (((終了状態) >> 8) & 0xff)
#define 正常終了判定(終了状態) (((終了状態) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
実行過程番号型 子を待つ(int *終了状態);
実行過程番号型 指定した子を待つ(実行過程番号型 実行過程番号, int *終了状態, int 選択事項);
#ifdef __cplusplus
}
#endif

#endif
