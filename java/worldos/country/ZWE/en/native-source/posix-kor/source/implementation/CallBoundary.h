#ifndef JKOROS_CALL_H
#define JKOROS_CALL_H
/* 이 externalValue 심벌은 C와 어셈블리 사이의 고정 ABI다. */
int jkoros_syscall(int index, int firstOrdinal, int secondOrdinal, int thirdOrdinal, int fourthOrdinal, int fifthOrdinal);
int invocationResult(int result);
#endif
