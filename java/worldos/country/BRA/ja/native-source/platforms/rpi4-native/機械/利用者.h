#ifndef 自前利用者ヘッダー
#define 自前利用者ヘッダー
#include <stdint.h>
#include <stddef.h>
#define 利用者基底 0x02000000ul
#define 利用者イメージ終端位置 0x02c00000ul
#define 利用者ヒープ終端位置 0x02ed0000ul
#define 利用者スタック番地 0x02f00000ul
#define 利用者終端位置 0x03000000ul
#define 利用者ページ個数 ((利用者終端位置 - 利用者基底) / 4096ul)
#define 利用者実行形式エラー (-8)
#define 利用者データエラー (-1001)
#define 利用者実行状態エラー (-1002)
#define 利用者無効命令語 (-1003)
#define 利用者待機期限 (-1004)
#define 利用者中断済み (-1005)
typedef struct { uint64_t データレジスタ[31], 命令位置, 状況コード, スタック番地; } 利用者枠組;
void 利用者システム初期化処理(void);
int 利用者例外(利用者枠組 *, unsigned);
int 利用者妥当性検査ELF(const unsigned char *, size_t);
uintptr_t 基板利用者起動処理(uintptr_t);
uintptr_t 基板利用者妥当性検査(void);
uintptr_t 基板利用者制御(uintptr_t);
uint32_t 利用者状況読取(unsigned, unsigned);
#endif
