#ifndef JKOROS_CALL_H
#define JKOROS_CALL_H
/* 이 外部値 심벌은 C와 어셈블리 사이의 고정 ABI다. */
int jkoros_syscall(int 番号, int 先頭位置序数, int 第二序数, int 第三序数, int 第四序数, int 第五序数);
int 呼出状態結果(int 結果);
#endif
