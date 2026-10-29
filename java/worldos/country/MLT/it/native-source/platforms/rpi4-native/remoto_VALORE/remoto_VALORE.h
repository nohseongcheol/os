#ifndef nativo_connessione_remota_Intestazione
#define nativo_connessione_remota_Intestazione
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Prepara_remoto(void);
void 원격살피기(void);
void remoto_output(unsigned char);
int remoto_input(void);
int feed_remoto_input(const unsigned char *,unsigned);
uintptr_t scheda_shadowing(uintptr_t,uintptr_t);
uintptr_t scheda_chiudere_remoto_comando(uintptr_t);
uintptr_t scheda_remoto_aspetta(uintptr_t);
void 원격화면살피기(void);
int controllo_remoto_display(unsigned);
#endif
