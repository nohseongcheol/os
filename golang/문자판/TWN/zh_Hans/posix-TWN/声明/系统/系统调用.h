/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _声明_系统_系统调用
#define _声明_系统_系统调用

long __syscall6(long 调用编号, long 第一参数, long 第二参数, long 第三参数,
                      long 第四参数, long 第五参数, long 第六参数);
long __syscall_result(long 结果);

#endif
