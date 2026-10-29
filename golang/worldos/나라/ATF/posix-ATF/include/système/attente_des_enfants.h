#ifndef _include_système_attente_des_enfants
#define _include_système_attente_des_enfants

#include <système/types_de_données.h>

#define WNOHANG 1
#define WEXITSTATUS(état) (((état) >> 8) & 0xff)
#define WIFEXITED(état) (((état) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t attendre_un_enfant(int *état);
pid_t attendre_un_enfant_désigné(pid_t pid, int *état, int options);
#ifdef __cplusplus
}
#endif

#endif
