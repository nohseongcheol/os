#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdint.h>
#include <ctype.h>

void *memcpy(void *destination, const void *source, size_t довжина)
{
    unsigned char *cursor = destination;
    const unsigned char *input = source;
    while (довжина--) *cursor++ = *input++;
    return destination;
}

void *memmove(void *destination, const void *source, size_t довжина)
{
    unsigned char *cursor = destination;
    const unsigned char *input = source;
    if ((uintptr_t)destination <= (uintptr_t)source)
        return memcpy(destination, source, довжина);
    while (довжина) { --довжина; cursor[довжина] = input[довжина]; }
    return destination;
}

void *memset(void *destination, int character, size_t довжина)
{
    unsigned char *cursor = destination;
    while (довжина--) *cursor++ = (unsigned char)character;
    return destination;
}

int memcmp(const void *left, const void *right, size_t довжина)
{
    const unsigned char *cursor = left, *input = right;
    while (довжина--) {
        if (*cursor != *input) return (int)*cursor - (int)*input;
        ++cursor; ++input;
    }
    return 0;
}

void *memchr(const void *source, int character, size_t довжина)
{
    const unsigned char *cursor = source;
    while (довжина--) {
        if (*cursor == (unsigned char)character) return (void *)cursor;
        ++cursor;
    }
    return NULL;
}

size_t strlen(const char *text)
{
    const char *cursor = text;
    while (*cursor) ++cursor;
    return (size_t)(cursor - text);
}

size_t strnlen(const char *text, size_t limit)
{
    size_t довжина = 0;
    while (довжина < limit && text[довжина]) ++довжина;
    return довжина;
}

char *stpcpy(char *destination, const char *source)
{
    while ((*destination = *source) != 0) { ++destination; ++source; }
    return destination;
}

char *strcpy(char *destination, const char *source)
{
    stpcpy(destination, source);
    return destination;
}

char *stpncpy(char *destination, const char *source, size_t limit)
{
    size_t довжина = strnlen(source, limit);
    memcpy(destination, source, довжина);
    memset(destination + довжина, 0, limit - довжина);
    return destination + довжина;
}

char *strncpy(char *destination, const char *source, size_t limit)
{
    stpncpy(destination, source, limit);
    return destination;
}

char *strcat(char *destination, const char *source)
{
    stpcpy(destination + strlen(destination), source);
    return destination;
}

char *strncat(char *destination, const char *source, size_t limit)
{
    char *cursor = destination + strlen(destination);
    size_t довжина = strnlen(source, limit);
    memcpy(cursor, source, довжина);
    cursor[довжина] = 0;
    return destination;
}

int strcmp(const char *left, const char *right)
{
    while (*left && *left == *right) { ++left; ++right; }
    return (int)(unsigned char)*left - (int)(unsigned char)*right;
}

int strncmp(const char *left, const char *right, size_t limit)
{
    while (limit--) {
        int result = (int)(unsigned char)*left - (int)(unsigned char)*right;
        if (result || !*left) return result;
        ++left; ++right;
    }
    return 0;
}

/* The only active locale in this runtime is the initial C/POSIX locale. */
int strcoll(const char *left, const char *right) { return strcmp(left, right); }

size_t strxfrm(char *destination, const char *source, size_t limit)
{
    size_t довжина = strlen(source);
    if (limit) {
        size_t copy_length = довжина < limit ? довжина : limit;
        memcpy(destination, source, copy_length);
        if (довжина < limit) destination[довжина] = 0;
    }
    return довжина;
}

char *strchr(const char *text, int character)
{
    do {
        if (*text == (char)character) return (char *)text;
    } while (*text++);
    return NULL;
}

char *strrchr(const char *text, int character)
{
    char *found = NULL;
    do { if (*text == (char)character) found = (char *)text; } while (*text++);
    return found;
}

char *strstr(const char *text, const char *source)
{
    size_t довжина = strlen(source);
    if (!довжина) return (char *)text;
    while (*text) {
        if (strncmp(text, source, довжина) == 0) return (char *)text;
        ++text;
    }
    return NULL;
}

size_t strspn(const char *text, const char *delimiters)
{
    size_t довжина = 0;
    while (text[довжина] && strchr(delimiters, text[довжина])) ++довжина;
    return довжина;
}

size_t strcspn(const char *text, const char *delimiters)
{
    size_t довжина = 0;
    while (text[довжина] && !strchr(delimiters, text[довжина])) ++довжина;
    return довжина;
}

char *strpbrk(const char *text, const char *delimiters)
{
    const char *cursor = text + strcspn(text, delimiters);
    return *cursor ? (char *)cursor : NULL;
}

char *strtok_r(char *text, const char *delimiters, char **saved_state)
{
    char *cursor = text ? text : *saved_state;
    if (!cursor) return NULL;
    cursor += strspn(cursor, delimiters);
    if (!*cursor) { *saved_state = cursor; return NULL; }
    text = cursor;
    cursor += strcspn(cursor, delimiters);
    if (*cursor) *cursor++ = 0;
    *saved_state = cursor;
    return text;
}

char *strtok(char *text, const char *delimiters)
{
    static char *saved_state;
    return strtok_r(text, delimiters, &saved_state);
}

char *strndup(const char *text, size_t limit)
{
    size_t довжина = strnlen(text, limit);
    char *destination = malloc(довжина + 1);
    if (destination) { memcpy(destination, text, довжина); destination[довжина] = 0; }
    return destination;
}

char *strdup(const char *text) { return strndup(text, strlen(text)); }

int strncasecmp(const char *left, const char *right, size_t limit)
{
    while (limit--) {
        int result = tolower((unsigned char)*left) - tolower((unsigned char)*right);
        if (result || !*left) return result;
        ++left; ++right;
    }
    return 0;
}

int strcasecmp(const char *left, const char *right)
{
    while (*left && tolower((unsigned char)*left) == tolower((unsigned char)*right)) { ++left; ++right; }
    return tolower((unsigned char)*left) - tolower((unsigned char)*right);
}
