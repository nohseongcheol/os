/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_SYS_WAIT_H
#define _LIBC_SYS_WAIT_H

#include <sys/types.h>

#define WNOHANG 1
#define WEXITSTATUS(অবস্থা) (((অবস্থা) >> 8) & 0xff)
#define WIFEXITED(অবস্থা) (((অবস্থা) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t wait(int *অবস্থা);
pid_t waitpid(pid_t pid, int *অবস্থা, int options);
#ifdef __cplusplus
}
#endif

#endif
