#ifndef JKOROS_CALL_H
#define JKOROS_CALL_H
/* 이 外部值 심벌은 C와 어셈블리 사이의 고정 ABI다. */
int jkoros_syscall(int 編號, int 首位序數, int 第二序數, int 第三序數, int 第四序數, int 第五序數);
int 調用狀態結果(int 結果);
#endif
