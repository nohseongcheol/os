#ifndef _LIBC_STRING_H
#define _LIBC_STRING_H
#include <basic_definitions.h>
void *memcpy(void *destination, const void *source, object_size_type length);
void *memmove(void *destination, const void *source, object_size_type length);
void *memset(void *destination, int character, object_size_type length);
int memcmp(const void *left, const void *right, object_size_type length);
void *memchr(const void *source, int character, object_size_type length);
object_size_type strlen(const char *text);
object_size_type strnlen(const char *text, object_size_type limit);
char *strcpy(char *destination, const char *source);
char *strncpy(char *destination, const char *source, object_size_type limit);
char *stpcpy(char *destination, const char *source);
char *stpncpy(char *destination, const char *source, object_size_type limit);
char *strcat(char *destination, const char *source);
char *strncat(char *destination, const char *source, object_size_type limit);
int strcmp(const char *left, const char *right);
int strncmp(const char *left, const char *right, object_size_type limit);
int strcoll(const char *left, const char *right);
object_size_type strxfrm(char *destination, const char *source, object_size_type limit);
char *strchr(const char *text, int character);
char *strrchr(const char *text, int character);
char *strstr(const char *text, const char *source);
object_size_type strspn(const char *text, const char *delimiters);
object_size_type strcspn(const char *text, const char *delimiters);
char *strpbrk(const char *text, const char *delimiters);
char *strtok(char *text, const char *delimiters);
char *strtok_r(char *text, const char *delimiters, char **saved_state);
char *strdup(const char *text);
char *strndup(const char *text, object_size_type limit);
#endif
