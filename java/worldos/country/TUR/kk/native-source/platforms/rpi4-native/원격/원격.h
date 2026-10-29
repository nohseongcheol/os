#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void 원격준비(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t Тақта_көлеңкелі_көшіру(uintptr_t,uintptr_t);
uintptr_t 보드원격명령끝(uintptr_t);
uintptr_t 보드원격대기(uintptr_t);
void 원격화면살피기(void);
int 원격화면제어(unsigned);
#endif
