#ifndef nativo_usuário_Cabeçalho
#define nativo_usuário_Cabeçalho
#include <stdint.h>
#include <stddef.h>
#define usuário_BASE 0x02000000ul
#define usuário_foto_encerrar 0x02c00000ul
#define usuário_heap_encerrar 0x02ed0000ul
#define usuário_pilha_email 0x02f00000ul
#define usuário_encerrar 0x03000000ul
#define usuário_página_CONT_NÚM ((usuário_encerrar - usuário_BASE) / 4096ul)
#define usuário_executável_erro (-8)
#define usuário_dados_erro (-1001)
#define usuário_execução_erro (-1002)
#define usuário_inválido_instrução (-1003)
#define usuário_TEMPOLIMITE (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t registro_dados[31], comando_cargo, código_de_estado, pilha_email; } usuário_quadro;
void 사용자체계준비(void);
int exceção_de_usuário(usuário_quadro *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Quadro_usuário_executar(uintptr_t);
uintptr_t Quadro_usuário_validar(void);
uintptr_t Quadro_controle_de_usuário(uintptr_t);
uint32_t leitura_usuário_Estado(unsigned, unsigned);
#endif
