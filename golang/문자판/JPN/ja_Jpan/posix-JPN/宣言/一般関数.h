/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣言_一般関数
#define _宣言_一般関数
#include <基本定義.h>
typedef struct { int 商; int 余り; } 整数除算結果型;
typedef struct { long 商; long 余り; } 長整数除算結果型;
#define 成功終了 0
#define 失敗終了 1
void *記憶領域を確保する(大きさ型 大きさ);
void *零で満たした配列領域を確保する(大きさ型 数量, 大きさ型 要素の大きさ);
void *記憶領域の大きさを変える(void *番地, 大きさ型 大きさ);
void 記憶領域を返す(void *番地);
long 文字列を長整数として読む(const char *文字列, char **変換終端番地, int 基数);
unsigned long 文字列を符号なし長整数として読む(const char *文字列, char **変換終端番地, int 基数);
int 十進文字列を整数として読む(const char *文字列);
long 十進文字列を長整数として読む(const char *文字列);
int 整数の絶対値を得る(int 値);
long 長整数の絶対値を得る(long 値);
整数除算結果型 整数の商と余りを得る(int 左の値, int 右の値);
長整数除算結果型 長整数の商と余りを得る(long 左の値, long 右の値);
void 比較基準で整列する(void *要素配列, 大きさ型 数量, 大きさ型 要素の大きさ,
           int (*比較関数)(const void *, const void *));
void *整列済み配列を二分探索する(const void *読出元, const void *要素配列, 大きさ型 数量,
              大きさ型 要素の大きさ, int (*比較関数)(const void *, const void *));
char *環境変数の値を得る(const char *名前);
#endif
