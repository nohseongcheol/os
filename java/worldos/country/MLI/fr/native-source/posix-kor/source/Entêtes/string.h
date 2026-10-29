#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *Chaîne);
int strcmp(const char *valeurAvantCôté, const char *valeurRetourArrièreCôté);
int memcmp(const void *valeurAvantCôté, const void *valeurRetourArrièreCôté, size_t nombreÉlémentsOctet);
void *memcpy(void *valeurDestination, const void *original, size_t nombreÉlémentsOctet);
void *memset(void *valeurDestination, int valeur, size_t nombreÉlémentsOctet);
#endif
