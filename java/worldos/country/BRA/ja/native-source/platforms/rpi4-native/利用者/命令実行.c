#include "../命名/機械連結名前一覧.h"
#include "呼出.h"
typedef void (*初期設定器メソッド)(void);
extern 初期設定器メソッド __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int 利用者プログラム開始処理(int);
int 利用者開始処理(int 転送済み値) {
    for (初期設定器メソッド *データ位置 = __init_array_start; データ位置 < __init_array_end; データ位置++) (*データ位置)();
    int 結果 = 利用者プログラム開始処理(転送済み値);
    for (初期設定器メソッド *データ位置 = __fini_array_end; データ位置 != __fini_array_start;) (*--データ位置)();
    return 結果;
}
void *memset(void *データ位置, int 値, size_t 入口個数) { unsigned char *宛先データ = データ位置; while (入口個数--) *宛先データ++ = 値; return データ位置; }
void *memcpy(void *宛先データ, const void *文字列データ, size_t 入口個数) { unsigned char *先頭位置値 = 宛先データ; const unsigned char *第二値 = 文字列データ; while (入口個数--) *先頭位置値++ = *第二値++; return 宛先データ; }
