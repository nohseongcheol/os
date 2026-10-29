#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdint.h>
#include <ctype.h>

void *memcpy(void *destination, const void *source, size_t độ_dài)
{
    unsigned char *cursor = destination;
    const unsigned char *input = source;
    while (độ_dài--) *cursor++ = *input++;
    return destination;
}

void *memmove(void *destination, const void *source, size_t độ_dài)
{
    unsigned char *cursor = destination;
    const unsigned char *input = source;
    if ((uintptr_t)destination <= (uintptr_t)source)
        return memcpy(destination, source, độ_dài);
    while (độ_dài) { --độ_dài; cursor[độ_dài] = input[độ_dài]; }
    return destination;
}

void *memset(void *destination, int character, size_t độ_dài)
{
    unsigned char *cursor = destination;
    while (độ_dài--) *cursor++ = (unsigned char)character;
    return destination;
}

int memcmp(const void *left, const void *right, size_t độ_dài)
{
    const unsigned char *cursor = left, *input = right;
    while (độ_dài--) {
        if (*cursor != *input) return (int)*cursor - (int)*input;
        ++cursor; ++input;
    }
    return 0;
}

void *memchr(const void *source, int character, size_t độ_dài)
{
    const unsigned char *cursor = source;
    while (độ_dài--) {
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
    size_t độ_dài = 0;
    while (độ_dài < limit && text[độ_dài]) ++độ_dài;
    return độ_dài;
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
    size_t độ_dài = strnlen(source, limit);
    memcpy(destination, source, độ_dài);
    memset(destination + độ_dài, 0, limit - độ_dài);
    return destination + độ_dài;
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
    size_t độ_dài = strnlen(source, limit);
    memcpy(cursor, source, độ_dài);
    cursor[độ_dài] = 0;
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
    size_t độ_dài = strlen(source);
    if (limit) {
        size_t copy_length = độ_dài < limit ? độ_dài : limit;
        memcpy(destination, source, copy_length);
        if (độ_dài < limit) destination[độ_dài] = 0;
    }
    return độ_dài;
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
    size_t độ_dài = strlen(source);
    if (!độ_dài) return (char *)text;
    while (*text) {
        if (strncmp(text, source, độ_dài) == 0) return (char *)text;
        ++text;
    }
    return NULL;
}

size_t strspn(const char *text, const char *delimiters)
{
    size_t độ_dài = 0;
    while (text[độ_dài] && strchr(delimiters, text[độ_dài])) ++độ_dài;
    return độ_dài;
}

size_t strcspn(const char *text, const char *delimiters)
{
    size_t độ_dài = 0;
    while (text[độ_dài] && !strchr(delimiters, text[độ_dài])) ++độ_dài;
    return độ_dài;
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
    size_t độ_dài = strnlen(text, limit);
    char *destination = malloc(độ_dài + 1);
    if (destination) { memcpy(destination, text, độ_dài); destination[độ_dài] = 0; }
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
