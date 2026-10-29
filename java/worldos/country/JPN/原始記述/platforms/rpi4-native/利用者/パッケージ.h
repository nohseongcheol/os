#ifndef 自前束ヘッダー
#define 自前束ヘッダー
#include <stddef.h>
int JAR開放(const char *ファイル入口名前);
int JAR読取(const char *名前, unsigned char *結果データ, unsigned 緩衝域容積);
const char *JAR主処理(void);
#endif
