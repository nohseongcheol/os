#ifndef 自前暗号学ヘッダー
#define 自前暗号学ヘッダー
#include <stddef.h>
#include <stdint.h>
void *遠隔確保(size_t);
void 遠隔解放(void *);
void *遠隔再確保(void *, size_t);
int 遠隔乱数(unsigned char *, unsigned);
void 遠隔要約(const void *, size_t, unsigned char [32]);
#endif
