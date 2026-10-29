#ifndef JKOROS_CALL_H
#define JKOROS_CALL_H
/* 이 externWert 심벌은 C와 어셈블리 사이의 고정 ABI다. */
int jkoros_syscall(int Nummer, int ersterOrdnungszahl, int zweiterOrdnungszahl, int dritterOrdnungszahl, int vierterOrdnungszahl, int fünfterOrdnungszahl);
int aufrufErgebnis(int ergebnis);
#endif
