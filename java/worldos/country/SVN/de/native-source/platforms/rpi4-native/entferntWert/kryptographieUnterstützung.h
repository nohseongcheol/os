#ifndef systemnahKryptographieKopf
#define systemnahKryptographieKopf
#include <stddef.h>
#include <stdint.h>
void *entferntZuteilen(size_t);
void entferntFreigeben(void *);
void *entferntNeuzuteilen(void *, size_t);
int entferntZufällig(unsigned char *, unsigned);
void entferntZusammenfassung(const void *, size_t, unsigned char [32]);
#endif
