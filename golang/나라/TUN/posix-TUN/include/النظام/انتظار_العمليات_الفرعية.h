/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_النظام_انتظار_العمليات_الفرعية
#define _include_النظام_انتظار_العمليات_الفرعية

#include <النظام/أنواع_البيانات.h>

#define WNOHANG 1
#define WEXITSTATUS(الحالة) (((الحالة) >> 8) & 0xff)
#define WIFEXITED(الحالة) (((الحالة) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t انتظار_عملية_فرعية(int *الحالة);
pid_t انتظار_العملية_الفرعية_المحددة(pid_t pid, int *الحالة, int options);
#ifdef __cplusplus
}
#endif

#endif
