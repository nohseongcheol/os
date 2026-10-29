#ifndef nativo_criptografia_Cabeçalho
#define nativo_criptografia_Cabeçalho
#include <stddef.h>
#include <stdint.h>
void *alocar_remoto(size_t);
void lançar_remoto(void *);
void *원격재할당(void *, size_t);
int remoto_aleatório(unsigned char *, unsigned);
void remoto_resumo(const void *, size_t, unsigned char [32]);
#endif
