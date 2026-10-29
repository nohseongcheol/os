#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *виділяти_віддалений(size_t);
void випуск_віддалений(void *);
void *원격재할당(void *, size_t);
int віддалений_випадковий(unsigned char *, unsigned);
void віддалений_зведення(const void *, size_t, unsigned char [32]);
#endif
