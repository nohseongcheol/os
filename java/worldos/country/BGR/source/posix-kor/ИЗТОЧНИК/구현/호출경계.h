#ifndef JKOROS_CALL_H
#define JKOROS_CALL_H
/* 이 външен_стойност 심벌은 C와 어셈블리 사이의 고정 ABI다. */
int jkoros_syscall(int индекс, int 첫째, int 둘째, int 셋째, int 넷째, int 다섯째);
int 호출결과(int РЕЗУЛТАТ);
#endif
