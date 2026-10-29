#ifndef 자체원격접속머리
#define 자체원격접속머리
#include "../명명/기계연결이름.h"
#include <stdint.h>
void 원격준비(void);
void 원격살피기(void);
void 원격출력(unsigned char);
int 원격입력(void);
int 원격입력넣기(const unsigned char *,unsigned);
uintptr_t Panel_vixilancia(uintptr_t,uintptr_t);
uintptr_t Panel_finalizar_remoto_comando(uintptr_t);
uintptr_t Panel_remoto_agarda(uintptr_t);
void 원격화면살피기(void);
int control_remoto_mostrar(unsigned);
#endif
