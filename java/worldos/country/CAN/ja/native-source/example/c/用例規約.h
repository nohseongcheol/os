#ifndef 自前例ヘッダー
#define 自前例ヘッダー
#include <ファイルABI.h>
#include <画面ABI.h>
static int 本文長さ(const char *文) { int 長さ=0;while(文[長さ])長さ++;return 長さ; }
static int 出力(const char *文) { int 長さ=本文長さ(文);return ファイルデータ書込(1,文,長さ)==長さ?0:1; }
#endif
