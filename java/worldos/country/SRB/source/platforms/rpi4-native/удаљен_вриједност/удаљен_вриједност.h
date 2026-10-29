#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Припремити_удаљен(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t Табла_даљинска_контрола(uintptr_t,uintptr_t);
uintptr_t Табла_завршити_удаљен_команда(uintptr_t);
uintptr_t Табла_удаљен_чекај(uintptr_t);
void 원격화면살피기(void);
int контрола_удаљен_екран(unsigned);
#endif
