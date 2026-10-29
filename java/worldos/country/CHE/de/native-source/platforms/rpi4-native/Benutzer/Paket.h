#ifndef systemnahBündelKopf
#define systemnahBündelKopf
#include <stddef.h>
int jARÖffnen(const char *dateiEintragName);
int jARLesen(const char *Name, unsigned char *ergebnisDaten, unsigned pufferKapazität);
const char *jARHauptvorgang(void);
#endif
