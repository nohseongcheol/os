#ifndef JKOROS_CALL_H
#define JKOROS_CALL_H
/* 이 valorExterno 심벌은 C와 어셈블리 사이의 고정 ABI다. */
int jkoros_syscall(int número, int ordinalPrimero, int ordinalSegundo, int ordinalTercero, int ordinalCuarto, int ordinalQuinto);
int resultadoInvocación(int resultado);
#endif
