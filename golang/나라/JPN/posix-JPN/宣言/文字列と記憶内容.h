/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _宣言_文字列と記憶内容
#define _宣言_文字列と記憶内容
#include <基本定義.h>
void *記憶内容を複写する(void *書込先, const void *読出元, 大きさ型 長さ);
void *重なりを許して記憶内容を移す(void *書込先, const void *読出元, 大きさ型 長さ);
void *記憶領域を値で満たす(void *書込先, int 文字値, 大きさ型 長さ);
int 記憶内容を比較する(const void *左の値, const void *右の値, 大きさ型 長さ);
void *記憶領域から値を探す(const void *読出元, int 文字値, 大きさ型 長さ);
大きさ型 文字列の八桁組数を得る(const char *文字列);
大きさ型 上限内の文字列八桁組数を得る(const char *文字列, 大きさ型 上限);
char *文字列を複写する(char *書込先, const char *読出元);
char *上限まで埋めて文字列を複写する(char *書込先, const char *読出元, 大きさ型 上限);
char *文字列を複写して終端を得る(char *書込先, const char *読出元);
char *上限まで埋めて複写し終端を得る(char *書込先, const char *読出元, 大きさ型 上限);
char *文字列を付け足す(char *書込先, const char *読出元);
char *上限内で文字列を付け足す(char *書込先, const char *読出元, 大きさ型 上限);
int 文字列を比較する(const char *左の値, const char *右の値);
int 上限内で文字列を比較する(const char *左の値, const char *右の値, 大きさ型 上限);
int 整列規則で文字列を比較する(const char *左の値, const char *右の値);
大きさ型 文字列の整列鍵を作る(char *書込先, const char *読出元, 大きさ型 上限);
char *文字列から最初の値を探す(const char *文字列, int 文字値);
char *文字列から最後の値を探す(const char *文字列, int 文字値);
char *文字列から部分列を探す(const char *文字列, const char *読出元);
大きさ型 許容値からなる先頭長を得る(const char *文字列, const char *区切り値集合);
大きさ型 除外値のない先頭長を得る(const char *文字列, const char *区切り値集合);
char *文字列から集合の値を探す(const char *文字列, const char *区切り値集合);
char *文字列を語に分ける(char *文字列, const char *区切り値集合);
char *進行状態を指定して文字列を語に分ける(char *文字列, const char *区切り値集合, char **保存進行状態);
char *新しい領域に文字列を複製する(const char *文字列);
char *上限内で新しい領域に文字列を複製する(const char *文字列, 大きさ型 上限);
#endif
