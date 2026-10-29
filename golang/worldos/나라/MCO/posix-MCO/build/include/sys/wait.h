#ifndef _LIBC_SYS_WAIT_H
#define _LIBC_SYS_WAIT_H

#include <sys/types.h>

#define WNOHANG 1
#define WEXITSTATUS(status) (((status) >> 8) & 0xff)
#define WIFEXITED(status) (((status) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t wait(int *status);
pid_t waitpid(pid_t pid, int *status, int options);
#ifdef __cplusplus
}
#endif

#endif
