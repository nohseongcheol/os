#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *низа_VALUE_6ca8363c) { size_t должина_VALUE = 0; while (низа_VALUE_6ca8363c[должина_VALUE]) должина_VALUE++; return должина_VALUE; }
int strcmp(const char *предна_VALUE, const char *Назад_VALUE) {
    while (*предна_VALUE && *предна_VALUE == *Назад_VALUE) { предна_VALUE++; Назад_VALUE++; }
    return (unsigned char)*предна_VALUE - (unsigned char)*Назад_VALUE;
}
int memcmp(const void *предна_VALUE, const void *Назад_VALUE, size_t бајт_COUNT) {
    const unsigned char *가 = предна_VALUE, *나 = Назад_VALUE;
    for (size_t отвор_внес = 0; отвор_внес < бајт_COUNT; отвор_внес++) if (가[отвор_внес] != 나[отвор_внес]) return 가[отвор_внес] - 나[отвор_внес];
    return 0;
}
void *memcpy(void *одредиште_VALUE, const void *원본, size_t бајт_COUNT) {
    unsigned char *가 = одредиште_VALUE; const unsigned char *나 = 원본;
    for (size_t отвор_внес = 0; отвор_внес < бајт_COUNT; отвор_внес++) 가[отвор_внес] = 나[отвор_внес];
    return одредиште_VALUE;
}
void *memset(void *одредиште_VALUE, int VALUE, size_t бајт_COUNT) {
    unsigned char *податоци = одредиште_VALUE;
    for (size_t отвор_внес = 0; отвор_внес < бајт_COUNT; отвор_внес++) податоци[отвор_внес] = VALUE;
    return одредиште_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *низа_VALUE_6ca8363c) {
    size_t должина_VALUE = strlen(низа_VALUE_6ca8363c), Позиција = 0;
    while (Позиција < должина_VALUE) { ssize_t мерка = write(1, низа_VALUE_6ca8363c + Позиција, должина_VALUE - Позиција); if (мерка <= 0) return EOF; Позиција += мерка; }
    return putchar('\n') == EOF ? EOF : 0;
}
