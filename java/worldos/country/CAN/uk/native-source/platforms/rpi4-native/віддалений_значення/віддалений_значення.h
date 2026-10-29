#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Готувати_віддалений(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t Дошка_віддалене_керування(uintptr_t,uintptr_t);
uintptr_t Дошка_завершити_виклик_віддалений_команда(uintptr_t);
uintptr_t Дошка_віддалений_хвилиноньку_панове(uintptr_t);
void 원격화면살피기(void);
int керування_віддалений_дисплей(unsigned);
#endif
