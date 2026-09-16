#ifndef _include_sistema_espera_de_hijos
#define _include_sistema_espera_de_hijos

#include <sistema/tipos_de_datos.h>

#define WNOHANG 1
#define WEXITSTATUS(estado) (((estado) >> 8) & 0xff)
#define WIFEXITED(estado) (((estado) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t esperar_hijo(int *estado);
pid_t esperar_hijo_indicado(pid_t pid, int *estado, int options);
#ifdef __cplusplus
}
#endif

#endif
