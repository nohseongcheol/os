/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <integer_types.h>
#include <ctype.h>

void *memcpy(void *destination, const void *source, object_size_type length)
{
    unsigned char *cursor = destination;
    const unsigned char *input = source;
    while (length--) *cursor++ = *input++;
    return destination;
}

void *memmove(void *destination, const void *source, object_size_type length)
{
    unsigned char *cursor = destination;
    const unsigned char *input = source;
    if ((pointer_sized_unsigned_integer)destination <= (pointer_sized_unsigned_integer)source)
        return memcpy(destination, source, length);
    while (length) { --length; cursor[length] = input[length]; }
    return destination;
}

void *memset(void *destination, int character, object_size_type length)
{
    unsigned char *cursor = destination;
    while (length--) *cursor++ = (unsigned char)character;
    return destination;
}

int memcmp(const void *left, const void *right, object_size_type length)
{
    const unsigned char *cursor = left, *input = right;
    while (length--) {
        if (*cursor != *input) return (int)*cursor - (int)*input;
        ++cursor; ++input;
    }
    return 0;
}

void *memchr(const void *source, int character, object_size_type length)
{
    const unsigned char *cursor = source;
    while (length--) {
        if (*cursor == (unsigned char)character) return (void *)cursor;
        ++cursor;
    }
    return null_pointer;
}

object_size_type strlen(const char *text)
{
    const char *cursor = text;
    while (*cursor) ++cursor;
    return (object_size_type)(cursor - text);
}

object_size_type strnlen(const char *text, object_size_type limit)
{
    object_size_type length = 0;
    while (length < limit && text[length]) ++length;
    return length;
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

char *stpncpy(char *destination, const char *source, object_size_type limit)
{
    object_size_type length = strnlen(source, limit);
    memcpy(destination, source, length);
    memset(destination + length, 0, limit - length);
    return destination + length;
}

char *strncpy(char *destination, const char *source, object_size_type limit)
{
    stpncpy(destination, source, limit);
    return destination;
}

char *strcat(char *destination, const char *source)
{
    stpcpy(destination + strlen(destination), source);
    return destination;
}

char *strncat(char *destination, const char *source, object_size_type limit)
{
    char *cursor = destination + strlen(destination);
    object_size_type length = strnlen(source, limit);
    memcpy(cursor, source, length);
    cursor[length] = 0;
    return destination;
}

int strcmp(const char *left, const char *right)
{
    while (*left && *left == *right) { ++left; ++right; }
    return (int)(unsigned char)*left - (int)(unsigned char)*right;
}

int strncmp(const char *left, const char *right, object_size_type limit)
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

object_size_type strxfrm(char *destination, const char *source, object_size_type limit)
{
    object_size_type length = strlen(source);
    if (limit) {
        object_size_type copy_length = length < limit ? length : limit;
        memcpy(destination, source, copy_length);
        if (length < limit) destination[length] = 0;
    }
    return length;
}

char *strchr(const char *text, int character)
{
    do {
        if (*text == (char)character) return (char *)text;
    } while (*text++);
    return null_pointer;
}

char *strrchr(const char *text, int character)
{
    char *found = null_pointer;
    do { if (*text == (char)character) found = (char *)text; } while (*text++);
    return found;
}

char *strstr(const char *text, const char *source)
{
    object_size_type length = strlen(source);
    if (!length) return (char *)text;
    while (*text) {
        if (strncmp(text, source, length) == 0) return (char *)text;
        ++text;
    }
    return null_pointer;
}

object_size_type strspn(const char *text, const char *delimiters)
{
    object_size_type length = 0;
    while (text[length] && strchr(delimiters, text[length])) ++length;
    return length;
}

object_size_type strcspn(const char *text, const char *delimiters)
{
    object_size_type length = 0;
    while (text[length] && !strchr(delimiters, text[length])) ++length;
    return length;
}

char *strpbrk(const char *text, const char *delimiters)
{
    const char *cursor = text + strcspn(text, delimiters);
    return *cursor ? (char *)cursor : null_pointer;
}

char *strtok_r(char *text, const char *delimiters, char **saved_state)
{
    char *cursor = text ? text : *saved_state;
    if (!cursor) return null_pointer;
    cursor += strspn(cursor, delimiters);
    if (!*cursor) { *saved_state = cursor; return null_pointer; }
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

char *strndup(const char *text, object_size_type limit)
{
    object_size_type length = strnlen(text, limit);
    char *destination = malloc(length + 1);
    if (destination) { memcpy(destination, text, length); destination[length] = 0; }
    return destination;
}

char *strdup(const char *text) { return strndup(text, strlen(text)); }

int strncasecmp(const char *left, const char *right, object_size_type limit)
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
