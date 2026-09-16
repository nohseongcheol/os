/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _声明_系统_子进程等待
#define _声明_系统_子进程等待

#include <系统/数据类型.h>

#define 未就绪则不等待 1
#define 提取退出值(结束状态) (((结束状态) >> 8) & 0xff)
#define 检查正常退出(结束状态) (((结束状态) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
进程编号类型 等待子进程(int *结束状态);
进程编号类型 等待指定子进程(进程编号类型 进程编号, int *结束状态, int 选项);
#ifdef __cplusplus
}
#endif

#endif
