/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_SYS_WAIT_H
#define _LIBC_SYS_WAIT_H

#include <sys/types.h>

#define WNOHANG 1
#define WEXITSTATUS(حالت) (((حالت) >> 8) & 0xff)
#define WIFEXITED(حالت) (((حالت) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t wait(int *حالت);
pid_t waitpid(pid_t pid, int *حالت, int options);
#ifdef __cplusplus
}
#endif

#endif
