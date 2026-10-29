#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *юл_VALUE_6ca8363c) { size_t озынлык_VALUE = 0; while (юл_VALUE_6ca8363c[озынлык_VALUE]) озынлык_VALUE++; return озынлык_VALUE; }
int strcmp(const char *앞, const char *Артка_VALUE) {
    while (*앞 && *앞 == *Артка_VALUE) { 앞++; Артка_VALUE++; }
    return (unsigned char)*앞 - (unsigned char)*Артка_VALUE;
}
int memcmp(const void *앞, const void *Артка_VALUE, size_t байт_COUNT) {
    const unsigned char *가 = 앞, *나 = Артка_VALUE;
    for (size_t оя_кертү = 0; оя_кертү < байт_COUNT; оя_кертү++) if (가[оя_кертү] != 나[оя_кертү]) return 가[оя_кертү] - 나[оя_кертү];
    return 0;
}
void *memcpy(void *күчерү_урыны_VALUE, const void *원본, size_t байт_COUNT) {
    unsigned char *가 = күчерү_урыны_VALUE; const unsigned char *나 = 원본;
    for (size_t оя_кертү = 0; оя_кертү < байт_COUNT; оя_кертү++) 가[оя_кертү] = 나[оя_кертү];
    return күчерү_урыны_VALUE;
}
void *memset(void *күчерү_урыны_VALUE, int VALUE, size_t байт_COUNT) {
    unsigned char *мәгълүмат = күчерү_урыны_VALUE;
    for (size_t оя_кертү = 0; оя_кертү < байт_COUNT; оя_кертү++) мәгълүмат[оя_кертү] = VALUE;
    return күчерү_урыны_VALUE;
}
int putchar(int 문자) { unsigned char VALUE = 문자; return write(1, &VALUE, 1) == 1 ? VALUE : EOF; }
int puts(const char *юл_VALUE_6ca8363c) {
    size_t озынлык_VALUE = strlen(юл_VALUE_6ca8363c), урнаштыру = 0;
    while (урнаштыру < озынлык_VALUE) { ssize_t үлчәм = write(1, юл_VALUE_6ca8363c + урнаштыру, озынлык_VALUE - урнаштыру); if (үлчәм <= 0) return EOF; урнаштыру += үлчәм; }
    return putchar('\n') == EOF ? EOF : 0;
}
