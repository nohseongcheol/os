#ifndef _LIBC_STRING_H
#define _LIBC_STRING_H
#include <Grunddefinitionen.h>
void *memcpy(void *destination, const void *source, size_t Länge);
void *memmove(void *destination, const void *source, size_t Länge);
void *memset(void *destination, int character, size_t Länge);
int memcmp(const void *left, const void *right, size_t Länge);
void *memchr(const void *source, int character, size_t Länge);
size_t strlen(const char *text);
size_t strnlen(const char *text, size_t limit);
char *strcpy(char *destination, const char *source);
char *strncpy(char *destination, const char *source, size_t limit);
char *stpcpy(char *destination, const char *source);
char *stpncpy(char *destination, const char *source, size_t limit);
char *strcat(char *destination, const char *source);
char *strncat(char *destination, const char *source, size_t limit);
int strcmp(const char *left, const char *right);
int strncmp(const char *left, const char *right, size_t limit);
int strcoll(const char *left, const char *right);
size_t strxfrm(char *destination, const char *source, size_t limit);
char *strchr(const char *text, int character);
char *strrchr(const char *text, int character);
char *strstr(const char *text, const char *source);
size_t strspn(const char *text, const char *delimiters);
size_t strcspn(const char *text, const char *delimiters);
char *strpbrk(const char *text, const char *delimiters);
char *strtok(char *text, const char *delimiters);
char *strtok_r(char *text, const char *delimiters, char **saved_state);
char *strdup(const char *text);
char *strndup(const char *text, size_t limit);
#endif
