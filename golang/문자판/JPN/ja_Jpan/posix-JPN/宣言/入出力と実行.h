/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣言_入出力と実行
#define _宣言_入出力と実行

#include <基本定義.h>
#include <体系/資料型.h>

#define 標準入力番号 0
#define 標準出力番号 1
#define 標準誤り出力番号 2
#define 存在確認 0
#define 実行権限確認 1
#define 書込権限確認 2
#define 読取権限確認 4
#define 先頭基準位置 0
#define 現在基準位置 1
#define 末尾基準位置 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **環境変数一覧;
void 直ちに終了する(int 終了状態) __attribute__((noreturn));
符号付き大きさ型 読む(int 文書記述番号, void *緩衝領域, 大きさ型 数量);
符号付き大きさ型 書く(int 文書記述番号, const void *緩衝領域, 大きさ型 数量);
int 閉じる(int 文書記述番号);
文書位置型 読み書き位置を移す(int 文書記述番号, 文書位置型 位置差, int 位置基準);
実行過程番号型 実行過程を分岐する(void);
int 実行内容を置き換える(const char *経路, char *const 引数一覧[], char *const 環境一覧[]);
実行過程番号型 実行過程番号を得る(void);
実行過程番号型 親実行過程番号を得る(void);
利用者番号型 利用者番号を得る(void);
利用者番号型 実効利用者番号を得る(void);
所属組番号型 所属組番号を得る(void);
所属組番号型 実効所属組番号を得る(void);
int 利用権限を調べる(const char *経路, int 利用方式);
int 作業目録を変える(const char *経路);
char *作業目録の経路を得る(char *緩衝領域, 大きさ型 大きさ);
int 開いた文書の参照を複製する(int 文書記述番号);
int 指定番号に文書参照を複製する(int 旧記述番号, int 新記述番号);
int 文書の記録を同期する(int 文書記述番号);
void 全ての記録を同期する(void);
int 端末か調べる(int 文書記述番号);
int 動的記憶の終端を定める(void *番地);
void *動的記憶の終端を移す(int 増分);
#ifdef __cplusplus
}
#endif

#endif
