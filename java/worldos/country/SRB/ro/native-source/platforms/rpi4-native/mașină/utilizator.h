#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define utilizator_BASE 0x02000000ul
#define utilizator_IMAGE_termina_un_apel 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define utilizator_Teanc_adresa 0x02f00000ul
#define utilizator_termina_un_apel 0x03000000ul
#define utilizator_pagina_COUNT ((utilizator_termina_un_apel - utilizator_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define utilizator_date_eroare (-1001)
#define utilizator_executare_eroare (-1002)
#define 사용자잘못된명령 (-1003)
#define utilizator_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registru_date[31], comandă_poziție, Stare_cod, Teanc_adresa; } utilizator_cadru;
void 사용자체계준비(void);
int excepție_utilizator(utilizator_cadru *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Avizier_utilizator_rula(uintptr_t);
uintptr_t Avizier_utilizator_valida(void);
uintptr_t Avizier_control_utilizator(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
