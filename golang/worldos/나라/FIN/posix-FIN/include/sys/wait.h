#ifndef _LIBC_SYS_WAIT_H
#define _LIBC_SYS_WAIT_H

#include <sys/types.h>

#define WNOHANG 1
#define WEXITSTATUS(tila) (((tila) >> 8) & 0xff)
#define WIFEXITED(tila) (((tila) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t wait(int *tila);
pid_t waitpid(pid_t pid, int *tila, int options);
#ifdef __cplusplus
}
#endif

#endif
