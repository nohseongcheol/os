#ifndef JKOROS_CALL_H
#define JKOROS_CALL_H
/* 이 valeurExtérieur 심벌은 C와 어셈블리 사이의 고정 ABI다. */
int jkoros_syscall(int numéro, int ordinalPremier, int ordinalDeuxième, int ordinalTroisième, int ordinalQuatrième, int ordinalCinquième);
int résultatInvocation(int résultat);
#endif
