/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_SYS_WAIT_H
#define _LIBC_SYS_WAIT_H

#include <sys/types.h>

#define WNOHANG 1
#define WEXITSTATUS(trạng_thái) (((trạng_thái) >> 8) & 0xff)
#define WIFEXITED(trạng_thái) (((trạng_thái) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t wait(int *trạng_thái);
pid_t waitpid(pid_t pid, int *trạng_thái, int options);
#ifdef __cplusplus
}
#endif

#endif
