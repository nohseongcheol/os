/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_система_ожидание_потомков
#define _include_система_ожидание_потомков

#include <система/типы_данных.h>

#define WNOHANG 1
#define WEXITSTATUS(состояние) (((состояние) >> 8) & 0xff)
#define WIFEXITED(состояние) (((состояние) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t ждать_потомка(int *состояние);
pid_t ждать_указанного_потомка(pid_t pid, int *состояние, int options);
#ifdef __cplusplus
}
#endif

#endif
