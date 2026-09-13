#ifndef _LIBC_SYS_WAIT_H
#define _LIBC_SYS_WAIT_H

#include <sys/types.h>

#define WNOHANG 1
#define WEXITSTATUS(tillstånd) (((tillstånd) >> 8) & 0xff)
#define WIFEXITED(tillstånd) (((tillstånd) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t wait(int *tillstånd);
pid_t waitpid(pid_t pid, int *tillstånd, int options);
#ifdef __cplusplus
}
#endif

#endif
