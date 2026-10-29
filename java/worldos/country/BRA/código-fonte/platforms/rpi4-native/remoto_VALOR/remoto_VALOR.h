#ifndef nativo_conexão_remota_Cabeçalho
#define nativo_conexão_remota_Cabeçalho
#include "../명명/기계연결이름.h"
#include <stdint.h>
void Preparar_remoto(void);
void 원격살피기(void);
void remoto_saída(unsigned char);
int remoto_entrada(void);
int feed_remoto_entrada(const unsigned char *,unsigned);
uintptr_t Quadro_sombreamento(uintptr_t,uintptr_t);
uintptr_t Quadro_encerrar_remoto_comando(uintptr_t);
uintptr_t Quadro_remoto_aguarde(uintptr_t);
void 원격화면살피기(void);
int visual_remoto_visor(unsigned);
#endif
