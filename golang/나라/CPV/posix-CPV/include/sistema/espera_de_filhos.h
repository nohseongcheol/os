#ifndef _include_sistema_espera_de_filhos
#define _include_sistema_espera_de_filhos

#include <sistema/tipos_de_dados.h>

#define WNOHANG 1
#define WEXITSTATUS(estado) (((estado) >> 8) & 0xff)
#define WIFEXITED(estado) (((estado) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t aguardar_filho(int *estado);
pid_t aguardar_filho_indicado(pid_t pid, int *estado, int options);
#ifdef __cplusplus
}
#endif

#endif
