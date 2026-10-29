#ifndef JKOROS_CALL_H
#define JKOROS_CALL_H
/* 이 外部值 심벌은 C와 어셈블리 사이의 고정 ABI다. */
int jkoros_syscall(int 编号, int 首位序数, int 第二序数, int 第三序数, int 第四序数, int 第五序数);
int 调用状态结果(int 结果);
#endif
