#ifndef systemnahEntferntVerbindungKopf
#define systemnahEntferntVerbindungKopf
#include "../benennung/maschineBindenNamen.h"
#include <stdint.h>
void entferntVorbereiten(void);
void entferntUntersuchen(void);
void entferntAusgabe(unsigned char);
int entferntEingabe(void);
int zuführenEntferntEingabe(const unsigned char *,unsigned);
uintptr_t platineEntferntSteuerung(uintptr_t,uintptr_t);
uintptr_t platineEndeEntferntBefehl(uintptr_t);
uintptr_t platineEntferntWarten(uintptr_t);
void entferntDarstellenUntersuchen(void);
int steuerungEntferntDarstellen(unsigned);
#endif
