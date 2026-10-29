#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *Zeichenkette);
int strcmp(const char *vorderseiteWert, const char *rückseiteWert);
int memcmp(const void *vorderseiteWert, const void *rückseiteWert, size_t byteAnzahl);
void *memcpy(void *zielWert, const void *ursprünglich, size_t byteAnzahl);
void *memset(void *zielWert, int Wert, size_t byteAnzahl);
#endif
