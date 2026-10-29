#ifndef nativo_USER_Intestazione
#define nativo_USER_Intestazione
#include <stdint.h>
#include <stddef.h>
#define USER_BASE 0x02000000ul
#define USER_foto_chiudere 0x02c00000ul
#define USER_heap_chiudere 0x02ed0000ul
#define USER_Pila_e_mail 0x02f00000ul
#define USER_chiudere 0x03000000ul
#define USER_pagina_CONTA_NUMERI ((USER_chiudere - USER_BASE) / 4096ul)
#define USER_eseguibile_errore (-8)
#define USER_dati_errore (-1001)
#define USER_esecuzione_errore (-1002)
#define USER_non_valida_istruzione (-1003)
#define USER_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registro_dati[31], comando_funzione, codice_di_stato, Pila_e_mail; } USER_frame;
void 사용자체계준비(void);
int eccezione_utente(USER_frame *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t scheda_USER_eseguire(uintptr_t);
uintptr_t scheda_USER_convalidare(void);
uintptr_t scheda_controllo_utente(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
