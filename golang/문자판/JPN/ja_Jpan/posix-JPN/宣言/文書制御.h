#ifndef _宣言_文書制御
#define _宣言_文書制御

#include <体系/資料型.h>

#define 読取専用で開く 0x0000
#define 書込専用で開く 0x0001
#define 読書両用で開く 0x0002
#define 利用方式抽出値 0x0003
#define 無ければ作る 0x0040
#define 新規文書のみ許す 0x0080
#define 既存内容を空にする 0x0200
#define 末尾へ追加する 0x0400
#define 目録のみ許す 0x10000

#define 記述番号複製 0
#define 記述番号標識取得 1
#define 記述番号標識設定 2
#define 文書状態標識取得 3
#define 文書状態標識設定 4
#define 実行内容置換時に閉じる 1

#ifdef __cplusplus
extern "C" {
#endif
int 開く(const char *経路, int 開く際の指定, ...);
int 文書を作る(const char *経路, 文書方式型 利用方式);
int 文書を制御する(int 文書記述番号, int 制御命令, ...);
#ifdef __cplusplus
}
#endif

#endif
